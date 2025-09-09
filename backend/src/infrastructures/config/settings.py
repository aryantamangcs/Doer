from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = (
    Path(__file__).resolve().parent.parent.parent
)  # becuase settings.py is inside src/infrastructure/config
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    """
    All configurations
    """

    SYNC_DATABASE_URL: str
    ASYNC_DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    """
    Returns the cached instance of settings
    """
    return (
        Settings()
    )  # type:ignore #because the Settings will pick the data from .env file
