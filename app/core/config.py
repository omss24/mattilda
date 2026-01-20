from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # TODO: Move to environment variables or a secure vault in production
    database_url: str = "postgresql+psycopg2://mattilda_user:mattilda_password@db:5432/mattilda_db"
    api_key: str = "dev-api-key"
    redis_url: str = "redis://redis:6379/0"

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


settings = Settings()
