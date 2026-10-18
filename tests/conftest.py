import pytest

from config import load_settings


@pytest.fixture(autouse=True)
def clear_settings_cache():
    load_settings.cache_clear()
    yield
    load_settings.cache_clear()
