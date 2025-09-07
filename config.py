from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import FrozenSet

class Settings(BaseSettings):
    bot_token: str
    admin_ids: FrozenSet[int] = frozenset()

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",   # указываем, что значения брать из .env
    )

settings = Settings()
