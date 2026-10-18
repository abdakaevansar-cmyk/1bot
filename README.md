# Telegram Bot Foundation

A production-ready Telegram bot foundation built with Python, aiogram 3, SQLAlchemy, and SQLite by default.

## Features

- `/start`, `/help`, `/menu`, `/profile`, `/settings`, `/cancel`, and `/admin`
- Inline keyboard interactions with callback data handling
- Persistent user storage with SQLite by default
- Admin authorization via `ADMIN_IDS`
- Structured logging and environment-based configuration
- Docker and Render deployment support
- Automated tests for config, database, and handlers

## Project structure

```text
.
├── app/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── repository.py
│   ├── handlers/
│   │   ├── admin.py
│   │   ├── user.py
│   │   └── __init__.py
│   ├── keyboards/
│   │   ├── __init__.py
│   │   └── main_menu.py
│   └── __init__.py
├── tests/
│   ├── test_admin.py
│   ├── test_config.py
│   ├── test_database.py
│   └── test_handlers.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── bot.py
├── config.py
├── docker-compose.yml
├── render.yaml
├── requirements.txt
└── .github/workflows/tests.yml
```

## Quick start

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and configure your secrets:

```bash
cp .env.example .env
```

Example `.env`:

```dotenv
BOT_TOKEN=your_telegram_bot_token
ADMIN_IDS=123456789,987654321
DATABASE_URL=sqlite+aiosqlite:///./bot.db
LOG_LEVEL=INFO
```

4. Run the bot:

```bash
python bot.py
```

## BotFather setup

1. Open Telegram and message `@BotFather`.
2. Run `/newbot`.
3. Choose a name and username.
4. Copy the HTTP API token.
5. Paste it into `BOT_TOKEN` in your `.env` file.
6. Add your Telegram user ID to `ADMIN_IDS`.

To get your Telegram user ID, use the `@userinfobot` service or other known methods.

## Configuration

All environment variables are read from the OS environment at startup. The application fails fast if `BOT_TOKEN` is missing or empty.

### Required variables

- `BOT_TOKEN`: Telegram bot token from BotFather.
- `ADMIN_IDS`: comma-separated Telegram user IDs with access to admin commands.
- `DATABASE_URL`: SQLAlchemy database URL. SQLite is used by default.
- `LOG_LEVEL`: Optional logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`).

## Running with Docker

Build and run locally:

```bash
docker build -t telegram-bot .
docker run --env-file .env -d --name telegram-bot telegram-bot
```

Or use Docker Compose:

```bash
docker compose up --build
```

## Deployment

### Render

The included `render.yaml` is configured for a simple web service using a PostgreSQL database. Update the values before deployment.

### Railway or VPS

1. Push the code to GitHub.
2. Create a new service on Railway or a VPS.
3. Set the environment variables from `.env`.
4. Install dependencies and start the bot process with:

```bash
python bot.py
```

For web-hosted platforms, keep the process alive using a service manager like `systemd`, `supervisord`, or a platform-managed worker process.

## Testing

Run the test suite:

```bash
pytest -q
```

## Logging and diagnosis

- Check bot logs with `docker logs <container_name>` or your hosting platform logs.
- Ensure `BOT_TOKEN` is set correctly.
- Confirm `ADMIN_IDS` contains valid numeric Telegram IDs.
- If database error occurs, verify the `DATABASE_URL` is correct and the filesystem is writable.

## Notes

- SQLite is fine for a single-instance app.
- For production with multiple instances or persistence requirements, use PostgreSQL.
- Do not commit `.env` files or real secrets into source control.
