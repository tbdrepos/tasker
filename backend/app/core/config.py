from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_name: str = "Tasker API"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    database_url: str = "sqlite+aiosqlite:///./tasker.db"

    secret_key: str = "e665c0932dc3356c4db3207710f607dac1607c466ad21ef2c69b3eb3202810c3"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    ai_model: str = "qwen3.5:9b"


@lru_cache
def get_settings() -> Settings:
    return Settings()
