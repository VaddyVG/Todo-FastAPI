from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    POSTGRES_URL: Optional[str] = None
    SQLITE_URL: str = "sqlite:///./todo_lite.db"

    @property
    def database_url(self):
        """Возвращает Postgres URL если он есть, иначе SQLite URL"""
        return self.POSTGRES_URL if self.POSTGRES_URL else self.SQLITE_URL

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
