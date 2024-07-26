# Project: luchoh.com refactoring
# File: backend/app/core/config.py

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "YOUR_SECRET_KEY_HERE"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database settings
    DATABASE_URL: str = "mysql+pymysql://luchoh@localhost/luchoh_photography"

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:3000",
    ]

    # Superuser settings
    FIRST_SUPERUSER: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "changethis"

    UPLOAD_DIRECTORY: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "./uploads")

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
