"""
Настройка логирования
Конфигурация формата и уровня логирования
"""
import logging
import sys
from config import LOG_LEVEL


def setup_logger():
    """
    Настройка логгера для всего приложения
    Формат: [ВРЕМЯ] УРОВЕНЬ: Сообщение
    """
    # Получение уровня логирования из конфига
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    
    # Настройка формата
    log_format = "[%(asctime)s] %(levelname)s: %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Создание formatter
    formatter = logging.Formatter(log_format, datefmt=date_format)
    
    # Настройка handler для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # Настройка root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # Уменьшение шума от библиотек
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    
    logging.info(f"Логирование настроено: уровень {LOG_LEVEL}")