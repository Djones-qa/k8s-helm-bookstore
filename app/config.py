from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "Bookstore API"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()
