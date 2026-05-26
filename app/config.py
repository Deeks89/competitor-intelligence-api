from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    ANTHROPIC_API_KEY: str
    FIRECRAWL_API_KEY: str
    APP_NAME: str = "Competitor Intelligence API"

    class Config:
        env_file = ".env"

settings = Settings()
