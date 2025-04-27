from functools import lru_cache
from app.core.settings import settings as _settings

@lru_cache
def get_settings():
    return _settings

settings = get_settings()
