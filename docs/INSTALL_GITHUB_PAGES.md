# Автоустановщик через GitHub Pages

Этот вариант позволяет запускать установку одной командой с хостинга GitHub Pages.

## 1. Подготовка артефакта

Соберите архив репозитория и опубликуйте его на GitHub Pages, например в `docs/` репозитория:

```bash
tar -czf ucheba.tar.gz --exclude='.git' .
```

Загрузите `ucheba.tar.gz` и файл `scripts/install_from_pages.sh` (переименуйте в `install_from_pages.sh`)
в ветку `gh-pages` или в папку `docs/` (если GitHub Pages настроен на ветку `main` + `/docs`).

## 2. Запуск установки на сервере

```bash
sudo -i
export PAGES_URL=https://example.github.io/ucheba
export ARCHIVE_NAME=ucheba.tar.gz
export PROJECT_DIR=/opt/ucheba

curl -fsSL https://example.github.io/ucheba/install_from_pages.sh | bash
```

Скрипт скачает архив, распакует его в `PROJECT_DIR` и вызовет `scripts/install_vds.sh`.

## 3. Переменные установки

Скрипт `install_from_pages.sh` передает управление `install_vds.sh`, поэтому используйте те же переменные:

```bash
export DOMAIN=example.com
export DJANGO_SECRET_KEY=change-me
export DATABASE_URL=postgres://ucheba:ucheba@localhost:5432/ucheba
export REDIS_URL=redis://localhost:6379/0
export API_URL=http://127.0.0.1:8000/api
export BOT_TOKEN=your-telegram-token
export CREATE_DB=1
export POSTGRES_USER=ucheba
export POSTGRES_PASSWORD=ucheba
export POSTGRES_DB=ucheba
```
