from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database.models import Base, User


class UserRepository:
    def __init__(self, database_url: str | None = None) -> None:
        self.database_url = database_url or "sqlite+aiosqlite:///./bot.db"
        self.engine = create_async_engine(self.database_url, future=True)
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False)

    async def init_db(self) -> None:
        async with self.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def get_or_create_user(
        self,
        telegram_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> User:
        async with self.session_factory() as session:
            result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            user = result.scalar_one_or_none()
            if user is None:
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    is_deleted=False,
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user

            updates: dict[str, Any] = {}
            if username is not None and username != user.username:
                updates["username"] = username
            if first_name is not None and first_name != user.first_name:
                updates["first_name"] = first_name
            if last_name is not None and last_name != user.last_name:
                updates["last_name"] = last_name

            if updates:
                for key, value in updates.items():
                    setattr(user, key, value)
                await session.commit()
                await session.refresh(user)

            return user

    async def update_user_profile(
        self,
        telegram_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> User:
        async with self.session_factory() as session:
            result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            user = result.scalar_one_or_none()
            if user is None:
                raise ValueError(f"User with telegram_id={telegram_id} does not exist.")

            if username is not None:
                user.username = username
            if first_name is not None:
                user.first_name = first_name
            if last_name is not None:
                user.last_name = last_name

            await session.commit()
            await session.refresh(user)
            return user

    async def get_user_by_id(self, telegram_id: int) -> User | None:
        async with self.session_factory() as session:
            result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            return result.scalar_one_or_none()

    async def count_users(self) -> int:
        async with self.session_factory() as session:
            result = await session.execute(select(User).where(User.is_deleted.is_(False)))
            return len(result.scalars().all())

    async def list_users(self, limit: int = 20, offset: int = 0) -> list[User]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(User)
                .where(User.is_deleted.is_(False))
                .order_by(User.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
            return list(result.scalars().all())

    async def delete_user_data(self, telegram_id: int) -> bool:
        async with self.session_factory() as session:
            result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            user = result.scalar_one_or_none()
            if user is None:
                return False
            user.is_deleted = True
            user.username = None
            user.first_name = None
            user.last_name = None
            await session.commit()
            return True

    async def close(self) -> None:
        await self.engine.dispose()
