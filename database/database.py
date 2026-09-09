"""
Модуль работы с базой данных
Инициализация, сессии, вспомогательные функции
"""
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select, func
from config import DATABASE_URL
from database.models import Base, User, CommandLog
from datetime import datetime

logger = logging.getLogger(__name__)

# Создание асинхронного движка
engine = create_async_engine(DATABASE_URL, echo=False)

# Создание фабрики сессий
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """
    Инициализация базы данных
    Создаёт все таблицы, если их нет
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Таблицы базы данных созданы/проверены")


async def get_session():
    """
    Контекстный менеджер для работы с сессией БД
    
    Usage:
        async with get_session() as session:
            user = await session.get(User, user_id)
    """
    return async_session()


async def update_user_stats(user_id: int, command_type: str):
    """
    Обновление статистики пользователя
    
    Args:
        user_id: Telegram User ID
        command_type: Тип команды (weather, crypto, ai)
    """
    async with async_session() as session:
        # Получение пользователя
        user = await session.get(User, user_id)
        
        if user:
            # Обновление общего счётчика
            user.total_commands += 1
            
            # Обновление счётчика по типу команды
            if command_type == "weather":
                user.weather_commands += 1
            elif command_type == "crypto":
                user.crypto_commands += 1
            elif command_type == "ai":
                user.ai_commands += 1
            
            # Обновление last_active
            user.last_active = datetime.utcnow()
            
            await session.commit()
            logger.debug(f"Статистика обновлена: user={user_id}, command={command_type}")


async def get_user_stats(user_id: int) -> dict:
    """
    Получение статистики пользователя
    
    Args:
        user_id: Telegram User ID
    
    Returns:
        Словарь со статистикой
    """
    async with async_session() as session:
        user = await session.get(User, user_id)
        
        if not user:
            return {
                "total_commands": 0,
                "weather": 0,
                "crypto": 0,
                "ai": 0
            }
        
        return {
            "total_commands": user.total_commands,
            "weather": user.weather_commands,
            "crypto": user.crypto_commands,
            "ai": user.ai_commands
        }


async def get_total_stats() -> dict:
    """
    Получение общей статистики бота
    
    Returns:
        Словарь с общей статистикой
    """
    async with async_session() as session:
        # Количество пользователей
        result = await session.execute(select(func.count(User.user_id)))
        total_users = result.scalar() or 0
        
        # Общее количество команд
        result = await session.execute(select(func.sum(User.total_commands)))
        total_commands = result.scalar() or 0
        
        return {
            "total_users": total_users,
            "total_commands": total_commands
        }