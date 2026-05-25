# config.py — Reads your .env file and makes settings available across the app
# pydantic-settings automatically reads from environment variables / .env file

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # These names must exactly match the keys in your .env file
    DATABASE_URL: str
    ANTHROPIC_API_KEY: str
    FIRECRAWL_API_KEY: str
    APP_NAME: str = "Competitor Intelligence API"
    DEBUG: bool = True

    class Config:
        # Tells pydantic-settings where to find the .env file
        env_file = ".env"


# Create a single instance to import everywhere else in the app
# Usage in other files: from app.config import settings
settings = Settings()
