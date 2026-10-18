from types import SimpleNamespace

from app.handlers.user import handle_start_command


async def test_handle_start_command_creates_user_and_message(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "test-token")
    monkeypatch.setenv("ADMIN_IDS", "")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

    answers = []

    async def answer(text, **kwargs):
        answers.append((text, kwargs))

    message = SimpleNamespace(
        from_user=SimpleNamespace(id=42, username="tester", first_name="Test", last_name="User"),
        answer=answer,
        bot=SimpleNamespace(),
    )

    result = await handle_start_command(message)

    assert result is True
    assert message.from_user.id == 42
    assert len(answers) == 1
