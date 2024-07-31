# Project: luchoh.com refactoring
# File: backend/app/core/config.py

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import json

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the 'app' directory
app_dir = os.path.dirname(current_dir)
# Construct the path to the .env file
env_file_path = os.path.join(app_dir, ".env")


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "YOUR_SECRET_KEY_HERE"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database settings
    DATABASE_URL: str = "mysql+pymysql://luchoh@localhost/luchoh_photography"

    # CORS settings
    BACKEND_CORS_ORIGINS: str = "[]"

    # Superuser settings
    FIRST_SUPERUSER: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "changethis"

    UPLOAD_DIRECTORY: str = os.path.join(app_dir, "../uploads")

    DEFAULT_TAG: str = "sticky"

    model_config = SettingsConfigDict(env_file=env_file_path, case_sensitive=True)

    @property
    def BACKEND_CORS_ORIGINS_LIST(self) -> List[str]:
        return json.loads(self.BACKEND_CORS_ORIGINS)


settings = Settings()

print("Loaded BACKEND_CORS_ORIGINS:", settings.BACKEND_CORS_ORIGINS_LIST)
