import os
from dotenv import load_dotenv

load_dotenv() # cargar .env en variables de entorno

class Settings:
    APP_ENV: str = os.getenv("APP_ENV", "local")
    APP_NAME: str = os.getenv("APP_NAME", "app")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.0.0")

    DATABASE_URL: str = os.getenv("DATABASE_URL")

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")

settings = Settings()