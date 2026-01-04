# Установка на VDS (автоустановщик)

## Требования

- Ubuntu 22.04+
- Доступ root/sudo
- Домен и DNS (A-запись)

## Быстрый запуск

```bash
sudo -i
export PROJECT_DIR=/opt/ucheba
export REPO_URL=https://example.com/your-repo.git
export DOMAIN=example.com
export DJANGO_SECRET_KEY=change-me
export DATABASE_URL=postgres://ucheba:ucheba@localhost:5432/ucheba
export REDIS_URL=redis://localhost:6379/0
export API_URL=http://127.0.0.1:8000/api
export BOT_TOKEN=your-telegram-token

bash scripts/install_vds.sh
```

## Что делает скрипт

- Устанавливает зависимости (Python, Postgres, Redis, Nginx, Node)
- Разворачивает backend и frontend
- Создает `.env` файлы
- Запускает Gunicorn, Celery и Telegram-бота через systemd
- Настраивает Nginx

> Примечание: убедитесь, что в PostgreSQL создана база и пользователь из `DATABASE_URL`.
> Если `CREATE_DB=1`, установщик будет использовать `POSTGRES_*` значения и при несовпадении
> перезапишет пароль в `DATABASE_URL`.

## После установки

1. Обновите `server_name` в `/etc/nginx/sites-available/ucheba.conf`.
2. Установите SSL:

```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d example.com
```

3. Проверьте статус сервисов:

```bash
systemctl status ucheba-gunicorn
systemctl status ucheba-celery
systemctl status ucheba-bot
```
