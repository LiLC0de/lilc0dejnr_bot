"""
Конфигурация бота
Загрузка переменных окружения из .env файла
"""
import os
from dotenv import load_dotenv

# Загрузка .env файла
load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# API ключи
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CRYPTO_API_KEY = os.getenv("CRYPTO_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# База данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./bot.db")

# Настройки бота
BOT_USERNAME = "lilc0dejnr_bot"
ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]

# Логирование
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")