#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR=${PROJECT_DIR:-/opt/ucheba}
REPO_URL=${REPO_URL:-https://example.com/your-repo.git}
DOMAIN=${DOMAIN:-example.com}
DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY:-change-me}
DATABASE_URL=${DATABASE_URL:-postgres://ucheba:ucheba@localhost:5432/ucheba}
REDIS_URL=${REDIS_URL:-redis://localhost:6379/0}
API_URL=${API_URL:-http://127.0.0.1:8000/api}
BOT_TOKEN=${BOT_TOKEN:-}
CREATE_DB=${CREATE_DB:-1}
POSTGRES_USER=${POSTGRES_USER:-ucheba}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-ucheba}
POSTGRES_DB=${POSTGRES_DB:-ucheba}

if [[ "$CREATE_DB" == "1" ]]; then
  DB_PASSWORD=$(python3 - <<'PY'
from urllib.parse import urlparse
import os

database_url = os.environ.get("DATABASE_URL", "")
parsed = urlparse(database_url)
print(parsed.password or "")
PY
)
  if [[ -n "$DB_PASSWORD" && "$DB_PASSWORD" != "$POSTGRES_PASSWORD" ]]; then
    echo "WARNING: DATABASE_URL password differs from POSTGRES_PASSWORD. Using POSTGRES_* values."
    DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}"
  fi
fi

if [[ $EUID -ne 0 ]]; then
  echo "Run as root (sudo)."
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get install -y python3 python3-venv python3-pip git nginx redis-server postgresql postgresql-contrib nodejs npm

if [[ ! -d "$PROJECT_DIR" ]]; then
  git clone "$REPO_URL" "$PROJECT_DIR"
fi

cd "$PROJECT_DIR"

chown -R www-data:www-data "$PROJECT_DIR"

if [[ "$CREATE_DB" == "1" ]]; then
  sudo -u postgres psql <<SQL
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
install -m 644 "$PROJECT_DIR/scripts/systemd/ucheba-gunicorn.service" /etc/systemd/system/ucheba-gunicorn.service
install -m 644 "$PROJECT_DIR/scripts/systemd/ucheba-celery.service" /etc/systemd/system/ucheba-celery.service

if [[ -n "$BOT_TOKEN" ]]; then
  install -m 644 "$PROJECT_DIR/scripts/systemd/ucheba-bot.service" /etc/systemd/system/ucheba-bot.service
fi

systemctl daemon-reload
systemctl enable --now ucheba-gunicorn.service
systemctl enable --now ucheba-celery.service
if [[ -n "$BOT_TOKEN" ]]; then
  systemctl enable --now ucheba-bot.service
fi

# Nginx
install -m 644 "$PROJECT_DIR/scripts/nginx/ucheba.conf" /etc/nginx/sites-available/ucheba.conf
ln -sf /etc/nginx/sites-available/ucheba.conf /etc/nginx/sites-enabled/ucheba.conf
nginx -t && systemctl reload nginx

echo "Done. Configure SSL with certbot if needed."
