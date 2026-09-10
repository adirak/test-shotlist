from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str
    env: str = "dev"
    cors_origins: str = "*"


@lru_cache
def get_settings() -> Settings:
    return Settings()
