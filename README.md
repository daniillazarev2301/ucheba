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

## Автоустановщик для VDS

Скрипт `scripts/install_vds.sh` автоматизирует установку на Ubuntu (Gunicorn, Celery, Nginx, Redis, PostgreSQL, Node.js).
Подробности: `docs/INSTALL_VDS.md`.

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
