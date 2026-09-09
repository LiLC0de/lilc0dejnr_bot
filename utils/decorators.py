"""
Декораторы для обработчиков команд
Rate limiting, логирование, обработка ошибок
"""
import logging
import time
from functools import wraps
from typing import Callable
from aiogram import types

logger = logging.getLogger(__name__)

# Словарь для хранения последнего использования команд пользователями
_user_last_command = {}


def rate_limit(seconds: int = 3):
    """
    Декоратор для ограничения частоты вызовов команд
    
    Args:
        seconds: Минимальный интервал между вызовами (в секундах)
    
    Usage:
        @rate_limit(5)
        async def cmd_weather(message: types.Message):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(message: types.Message, *args, **kwargs):
            user_id = message.from_user.id
            current_time = time.time()
            
            # Проверка: прошло ли достаточно времени
            last_time = _user_last_command.get(user_id, 0)
            if current_time - last_time < seconds:
                await message.answer(
                    f"⏳ Подожди {seconds} сек перед следующей командой"
                )
                return
            
            # Обновление времени последнего вызова
            _user_last_command[user_id] = current_time
            
            # Выполнение функции
            return await func(message, *args, **kwargs)
        
        return wrapper
    return decorator


def log_command(func: Callable):
    """
    Декоратор для логирования вызовов команд
    
    Usage:
        @log_command
        async def cmd_weather(message: types.Message):
            ...
    """
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        user_id = message.from_user.id
        username = message.from_user.username or "unknown"
        command = message.text.split()[0] if message.text else "unknown"
        
        logger.info(f"Команда: {command} от user={user_id} (@{username})")
        
        try:
            result = await func(message, *args, **kwargs)
            logger.info(f"Команда {command} выполнена успешно")
            return result
        except Exception as e:
            logger.error(f"Ошибка в команде {command}: {e}")
            raise
    
    return wrapper


def error_handler(func: Callable):
    """
    Декоратор для обработки ошибок в командах
    
    Usage:
        @error_handler
        async def cmd_weather(message: types.Message):
            ...
    """
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        try:
            return await func(message, *args, **kwargs)
        except Exception as e:
            logger.error(f"Необработанная ошибка: {e}", exc_info=True)
            await message.answer(
                "❌ Произошла ошибка. Попробуй позже или обратись к админу."
            )
    
    return wrapper