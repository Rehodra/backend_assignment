from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # MongoDB
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "backend_assignment"
    USE_MOCK_DB: bool = False  # Set to False to use the real MongoDB Atlas connection from .env

    # JWT
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Google OAuth
    GOOGLE_CLIENT_ID: str = "change-me-in-env"
    GOOGLE_CLIENT_SECRET: str = "change-me-in-env"
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/auth/google/callback"

    # CORS – comma-separated list of allowed origins
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:5174,http://localhost:5175,http://127.0.0.1:5173,http://127.0.0.1:5174,http://127.0.0.1:5175,http://localhost:3000"

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"
    }


settings = Settings()
