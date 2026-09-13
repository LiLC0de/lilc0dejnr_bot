"""
Telegram Bot @lilc0dejnr_bot
Главный файл запуска бота
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers import start, help, weather, crypto, ai, stats, inline, callbacks
from database.database import init_db
from utils.logger import setup_logger


async def main():
    """Запуск бота"""
    setup_logger()
    logger = logging.getLogger(__name__)
    
    await init_db()
    logger.info("База данных инициализирована")
    
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(weather.router)
    dp.include_router(crypto.router)
    dp.include_router(ai.router)
    dp.include_router(stats.router)
    dp.include_router(inline.router)
    dp.include_router(callbacks.router)
    
    logger.info("Бот запущен")
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")
