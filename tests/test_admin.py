from app.handlers.admin import is_admin


def test_admin_detection(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "test-token")
    monkeypatch.setenv("ADMIN_IDS", "10,20,30")
    assert is_admin(10) is True
    assert is_admin(99) is False
