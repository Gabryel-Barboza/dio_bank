from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_PATH = Path(__file__).parent.parent


class Settings(BaseSettings):
    database_url: str
    environment: str = 'production'
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    debug_mode: bool = False

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
        env_file_encoding='utf-8',
        env_ignore_empty=True,
    )


settings = Settings()
