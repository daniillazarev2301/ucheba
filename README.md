# Ucheba Platform

Полный шаблон образовательной платформы в стиле Kampus.ai.

## Требования

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+

## Структура

- `backend/` — Django + DRF + Celery
- `ai_module/` — AI-модуль (заглушки + генерация DOCX/PPTX)
- `frontend/` — React (TypeScript)
- `bot/` — Telegram-бот

## Быстрый старт (Backend)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

## Автоустановщик для VDS (полная инструкция)

Скрипт `scripts/install_vds.sh` автоматизирует установку на Ubuntu (Gunicorn, Celery, Nginx, Redis, PostgreSQL, Node.js).

### 1. Подготовка VDS

```bash
sudo -i
apt-get update
apt-get install -y git curl
```

### 2. Настройка переменных окружения

```bash
export PROJECT_DIR=/opt/ucheba
export REPO_URL=https://example.com/your-repo.git
export DOMAIN=example.com
export DJANGO_SECRET_KEY=change-me
export DATABASE_URL=postgres://ucheba:ucheba@localhost:5432/ucheba
export REDIS_URL=redis://localhost:6379/0
export API_URL=http://127.0.0.1:8000/api
export BOT_TOKEN=your-telegram-token
```

### 3. Запуск автоустановщика

```bash
cd /opt
git clone "$REPO_URL" "$PROJECT_DIR"
cd "$PROJECT_DIR"
bash scripts/install_vds.sh
```

### 4. Создание базы и пользователя PostgreSQL

```bash
sudo -u postgres psql <<SQL
CREATE USER ucheba WITH PASSWORD 'ucheba';
CREATE DATABASE ucheba OWNER ucheba;
GRANT ALL PRIVILEGES ON DATABASE ucheba TO ucheba;
SQL
```

> Если вы используете другие значения в `DATABASE_URL`, измените их здесь и в переменной окружения.

### 5. Проверка сервисов

```bash
systemctl status ucheba-gunicorn
systemctl status ucheba-celery
systemctl status ucheba-bot
```

### 6. SSL (по желанию)

```bash
apt-get install -y certbot python3-certbot-nginx
certbot --nginx -d example.com
```

### 7. Где смотреть логирование

```bash
journalctl -u ucheba-gunicorn -f
journalctl -u ucheba-celery -f
journalctl -u ucheba-bot -f
```

Дополнительно: расширенная документация — `docs/INSTALL_VDS.md`.

### Celery

```bash
cd backend
celery -A config worker -l info
```

## Frontend

```bash
cd frontend
cp .env.example .env
npm install
npm start
```

## Telegram Bot

```bash
cd bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python bot.py
```

## Миграции

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

## Gunicorn

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

## Celery + Redis

`CELERY_BROKER_URL` и `CELERY_RESULT_BACKEND` используют Redis.

## Nginx (пример)

```nginx
server {
    listen 80;
    server_name example.com;

    location /static/ {
        alias /srv/ucheba/backend/staticfiles/;
    }

    location /media/ {
        alias /srv/ucheba/backend/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Домен и SSL

Используйте Certbot:

```bash
sudo certbot --nginx -d example.com
```

## Оплата

Webhook доступен по адресу `POST /api/subscription/webhook`. Подключите YooKassa или PayMaster и передавайте `payment_id`, `plan_id`, `user_id`.

## Локализация

Интерфейс отображает русский язык. Комментарии и идентификаторы — на английском.

## Тесты

```bash
cd backend
pytest
```
