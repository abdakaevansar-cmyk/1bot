from __future__ import annotations

from app.database.repository import UserRepository
from config import load_settings


class UserService:
    def __init__(self, repository: UserRepository | None = None) -> None:
        settings = load_settings()
        self.repository = repository or UserRepository(settings.database_url)

    async def ensure_user(self, telegram_id: int, username: str | None = None, first_name: str | None = None, last_name: str | None = None):
        await self.repository.init_db()
        return await self.repository.get_or_create_user(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
