# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # Anthropic
    ANTHROPIC_API_KEY: str

    # App
    APP_NAME: str = "PropChat API"
    DEBUG: bool = True
    API_VERSION: str = "v1"

    # CORS
    FRONTEND_URL: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()