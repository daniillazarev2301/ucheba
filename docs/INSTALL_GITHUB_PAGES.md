# Автоустановщик через GitHub Pages

Этот вариант позволяет запускать установку одной командой с хостинга GitHub Pages.

## 1. Подготовка артефакта

Соберите архив репозитория и опубликуйте его на GitHub Pages, например в `docs/` репозитория:

```bash
tar -czf ucheba.tar.gz --exclude='.git' .
```

Загрузите `ucheba.tar.gz` и файл `scripts/install_from_pages.sh` (переименуйте в `install_from_pages.sh`)
в ветку `gh-pages` или в папку `docs/` (если GitHub Pages настроен на ветку `main` + `/docs`).

### Вариант через GitHub Actions

В репозитории есть workflow `.github/workflows/pages.yml`, который публикует:

- `docs/install-site/index.html` как сайт установки
- `install_from_pages.sh` в корне Pages
- `ucheba.tar.gz` (архив репозитория)

Достаточно включить GitHub Pages в настройках репозитория и выбрать источник `GitHub Actions`.

### Деплой на VDS через GitHub Actions

Добавлен workflow `.github/workflows/deploy_vds.yml`, который подключается к серверу по SSH и запускает
`scripts/install_vds.sh` с параметрами из GitHub Secrets.

Необходимые Secrets:

- `VDS_HOST`, `VDS_USER`, `VDS_SSH_KEY`, `VDS_PORT`
- `VDS_SSH_PASSPHRASE` (если ключ защищен паролем)
- `REPO_URL`, `DOMAIN`, `DJANGO_SECRET_KEY`, `REDIS_URL`, `API_URL`
- `BOT_TOKEN` (опционально)
- `CREATE_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`

`DATABASE_URL` необязателен, если `CREATE_DB=1` — он будет собран автоматически из `POSTGRES_*`.
- `PROJECT_DIR` (опционально, по умолчанию `/opt/ucheba`)
- `INSTALL_USER` (опционально, по умолчанию пользователь SSH)

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
