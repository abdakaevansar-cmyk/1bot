import pytest

from config import Settings, load_settings, parse_admin_ids


def test_parse_admin_ids_valid(monkeypatch):
    monkeypatch.setenv("ADMIN_IDS", "123,456, 789")
    assert parse_admin_ids() == [123, 456, 789]


def test_parse_admin_ids_invalid_raises():
    with pytest.raises(ValueError, match="ADMIN_IDS"):
        parse_admin_ids("abc")


def test_load_settings_missing_bot_token(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "")
    monkeypatch.setenv("ADMIN_IDS", "123")
    with pytest.raises(ValueError, match="BOT_TOKEN"):
        load_settings()


def test_settings_model(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token123")
    monkeypatch.setenv("ADMIN_IDS", "1,2,3")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./bot.db")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    settings = load_settings()

    assert isinstance(settings, Settings)
    assert settings.bot_token == "token123"
    assert settings.admin_ids == [1, 2, 3]
    assert settings.database_url.endswith("bot.db")
    assert settings.log_level == "DEBUG"
