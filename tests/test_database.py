import pytest

from app.database.repository import UserRepository


@pytest.mark.asyncio
async def test_create_and_update_user():
    repo = UserRepository(database_url="sqlite+aiosqlite:///:memory:")
    await repo.init_db()

    user = await repo.get_or_create_user(
        telegram_id=1001,
        username="alice",
        first_name="Alice",
        last_name="Example",
    )

    assert user.telegram_id == 1001
    assert user.username == "alice"

    updated = await repo.update_user_profile(
        telegram_id=1001,
        username="alice_2",
        first_name="Alice",
        last_name="Updated",
    )

    assert updated.username == "alice_2"
    assert updated.last_name == "Updated"

    count = await repo.count_users()
    assert count == 1

    deleted = await repo.delete_user_data(1001)
    assert deleted is True
