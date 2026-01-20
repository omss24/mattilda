import os

from pydantic_settings import BaseSettings, SettingsConfigDict


def _get_api_key() -> str:
    """Get API key from environment, with fallback for development only."""
    key = os.getenv("API_KEY")
    if not key:
        # Allow default only in development/testing
        if os.getenv("ENVIRONMENT", "development") == "production":
            raise ValueError("API_KEY environment variable is required in production")
        return "dev-api-key"
    return key


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://mattilda_user:mattilda_password@db:5432/mattilda_db"
    api_key: str = _get_api_key()
    redis_url: str = "redis://redis:6379/0"
    environment: str = "development"

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


settings = Settings()
