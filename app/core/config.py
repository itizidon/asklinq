from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    ENVIRONMENT: str
    PORT: int
    DATABASE_URL: str
    OPENAI_API_KEY: str
    LINQ_API_KEY: str
    LINQ_FROM_NUMBER: str
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

settings.DATABASE_URL = settings.DATABASE_URL.replace(
    "postgresql://",
    "postgresql+asyncpg://"
)