#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR=${PROJECT_DIR:-/opt/ucheba}
REPO_URL=${REPO_URL:-https://example.com/your-repo.git}
DOMAIN=${DOMAIN:-example.com}
DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY:-change-me}
DATABASE_URL=${DATABASE_URL:-}
REDIS_URL=${REDIS_URL:-redis://localhost:6379/0}
API_URL=${API_URL:-http://127.0.0.1:8000/api}
BOT_TOKEN=${BOT_TOKEN:-}
CREATE_DB=${CREATE_DB:-1}
POSTGRES_USER=${POSTGRES_USER:-ucheba}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-ucheba}
POSTGRES_DB=${POSTGRES_DB:-ucheba}
INSTALL_USER=${INSTALL_USER:-${USER}}

if [[ "$CREATE_DB" == "1" ]]; then
  DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}"
fi

if [[ $EUID -ne 0 ]]; then
  if command -v sudo >/dev/null 2>&1; then
    SUDO="sudo"
  else
    echo "Run as root (sudo)."
    exit 1
  fi
else
  SUDO=""
fi

export DEBIAN_FRONTEND=noninteractive

install_nodejs() {
  local version
  if command -v node >/dev/null 2>&1; then
    version=$(node -v | sed 's/^v//')
  else
    version="0"
  fi
  if [[ "${version%%.*}" -lt 18 ]]; then
    ${SUDO} apt-get install -y ca-certificates curl gnupg
    ${SUDO} mkdir -p /etc/apt/keyrings
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | ${SUDO} gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_18.x nodistro main" | ${SUDO} tee /etc/apt/sources.list.d/nodesource.list > /dev/null
    ${SUDO} apt-get update
    ${SUDO} apt-get install -y nodejs
  fi
}

${SUDO} apt-get update
${SUDO} apt-get install -y python3 python3-venv python3-pip git nginx redis-server postgresql postgresql-contrib
install_nodejs

${SUDO} systemctl enable --now postgresql
${SUDO} systemctl enable --now redis-server

if [[ ! -d "$PROJECT_DIR" ]]; then
  ${SUDO} mkdir -p "$(dirname "$PROJECT_DIR")"
  ${SUDO} chown -R "${INSTALL_USER}:${INSTALL_USER}" "$(dirname "$PROJECT_DIR")"
  git clone "$REPO_URL" "$PROJECT_DIR"
fi

cd "$PROJECT_DIR"

if [[ "$CREATE_DB" == "1" ]]; then
  ${SUDO} -u postgres psql <<SQL
DO
$$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '${POSTGRES_USER}') THEN
    CREATE ROLE ${POSTGRES_USER} LOGIN PASSWORD '${POSTGRES_PASSWORD}';
  END IF;
END
$$;
ALTER ROLE ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';
DO
$$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = '${POSTGRES_DB}') THEN
    CREATE DATABASE ${POSTGRES_DB} OWNER ${POSTGRES_USER};
  END IF;
END
$$;
SQL
fi

# Backend setup
python3 -m venv "$PROJECT_DIR/backend/.venv"
"$PROJECT_DIR/backend/.venv/bin/pip" install --upgrade pip
"$PROJECT_DIR/backend/.venv/bin/pip" install -r "$PROJECT_DIR/backend/requirements.txt"

cat > "$PROJECT_DIR/backend/.env" <<ENV
DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=${DOMAIN}
DATABASE_URL=${DATABASE_URL}
REDIS_URL=${REDIS_URL}
ENV

"$PROJECT_DIR/backend/.venv/bin/python" "$PROJECT_DIR/backend/manage.py" migrate
"$PROJECT_DIR/backend/.venv/bin/python" "$PROJECT_DIR/backend/manage.py" collectstatic --noinput

# Frontend setup
if [[ -d "$PROJECT_DIR/frontend" ]]; then
  if [[ ! -f "$PROJECT_DIR/frontend/.env" ]]; then
    cat > "$PROJECT_DIR/frontend/.env" <<ENV
REACT_APP_API_URL=${API_URL}
ENV
  fi
  npm --prefix "$PROJECT_DIR/frontend" install
  npm --prefix "$PROJECT_DIR/frontend" run build
fi

# Bot setup
if [[ -n "$BOT_TOKEN" ]]; then
  python3 -m venv "$PROJECT_DIR/bot/.venv"
  "$PROJECT_DIR/bot/.venv/bin/pip" install --upgrade pip
  "$PROJECT_DIR/bot/.venv/bin/pip" install -r "$PROJECT_DIR/bot/requirements.txt"
  if [[ ! -f "$PROJECT_DIR/bot/.env" ]]; then
    cat > "$PROJECT_DIR/bot/.env" <<ENV
BOT_TOKEN=${BOT_TOKEN}
API_URL=${API_URL}
ENV
  fi
fi

# Systemd services
${SUDO} install -m 644 "$PROJECT_DIR/scripts/systemd/ucheba-gunicorn.service" /etc/systemd/system/ucheba-gunicorn.service
${SUDO} install -m 644 "$PROJECT_DIR/scripts/systemd/ucheba-celery.service" /etc/systemd/system/ucheba-celery.service

if [[ -n "$BOT_TOKEN" ]]; then
  ${SUDO} install -m 644 "$PROJECT_DIR/scripts/systemd/ucheba-bot.service" /etc/systemd/system/ucheba-bot.service
fi

${SUDO} systemctl daemon-reload
${SUDO} systemctl enable --now ucheba-gunicorn.service
${SUDO} systemctl enable --now ucheba-celery.service
if [[ -n "$BOT_TOKEN" ]]; then
  ${SUDO} systemctl enable --now ucheba-bot.service
fi

# Nginx
${SUDO} install -m 644 "$PROJECT_DIR/scripts/nginx/ucheba.conf" /etc/nginx/sites-available/ucheba.conf
${SUDO} ln -sf /etc/nginx/sites-available/ucheba.conf /etc/nginx/sites-enabled/ucheba.conf
${SUDO} nginx -t && ${SUDO} systemctl reload nginx

${SUDO} chown -R www-data:www-data "$PROJECT_DIR"

echo "Done. Configure SSL with certbot if needed."
