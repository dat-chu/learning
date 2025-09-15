from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from enum import Enum

class DatabaseType(str, Enum):
    POSTGRES = "postgres"
    DYNAMODB = "dynamodb"

class Settings(BaseSettings):
    DATABASE_TYPE: DatabaseType = DatabaseType.POSTGRES # Default to postgres

    # --------------------------------------------------------------------
    # Postgres settings
    POSTGRES_DATABASE_URL: str = "postgresql+asyncpg://user:password@postgresql:5432/my_db"
    POSTGRES_DATABASE_URL_FOR_TESTING: str = "postgresql+asyncpg://postgres:password@postgresql:5432/my_db"
    # --------------------------------------------------------------------
    model_config = SettingsConfigDict(
        env_file = ".env",
        case_sensitive = True
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()