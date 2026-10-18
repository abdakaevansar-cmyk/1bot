from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_ids: list[int]
    database_url: str = "sqlite+aiosqlite:///./bot.db"
    log_level: str = "INFO"


def parse_admin_ids(raw_ids: str | None = None) -> list[int]:
    values = (raw_ids or os.getenv("ADMIN_IDS", "")).split(",")
    admin_ids: list[int] = []

    for value in values:
        candidate = value.strip()
        if not candidate:
            continue
        try:
            admin_ids.append(int(candidate))
        except ValueError as exc:
            raise ValueError(f"ADMIN_IDS contains invalid value '{candidate}'. Use comma-separated Telegram user IDs.") from exc

    return admin_ids


@lru_cache
def load_settings() -> Settings:
    bot_token = os.getenv("BOT_TOKEN", "").strip()
    if not bot_token:
        raise ValueError("BOT_TOKEN environment variable is missing or empty.")

    database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./bot.db").strip() or "sqlite+aiosqlite:///./bot.db"
    log_level = os.getenv("LOG_LEVEL", "INFO").strip().upper() or "INFO"

    return Settings(
        bot_token=bot_token,
        admin_ids=parse_admin_ids(os.getenv("ADMIN_IDS", "")),
        database_url=database_url,
        log_level=log_level,
    )
