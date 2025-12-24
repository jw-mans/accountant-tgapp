import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "tgapp_tasks")
POSTGRES_USER = os.getenv("POSTGRES_USER", "tgapp_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")

TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN', 'token')
APP_URL = os.getenv("APP_URL", "app_url")

DB_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
APP_URL = 