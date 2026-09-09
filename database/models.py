"""
Модели базы данных SQLAlchemy
Описывают структуру таблиц для хранения пользователей и статистики
"""
from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


class Base(DeclarativeBase):
    """Базовый класс для всех моделей"""
    pass


class User(Base):
    """
    Модель пользователя бота
    Хранит информацию о зарегистрированных пользователях
    """
    __tablename__ = "users"
    
    # Telegram User ID (первичный ключ)
    user_id = Column(BigInteger, primary_key=True, index=True)
    
    # Username (может быть пустым)
    username = Column(String(255), nullable=True)
    
    # Имя пользователя
    first_name = Column(String(255), nullable=False)
    
    # Дата регистрации
    registered_at = Column(DateTime, default=datetime.utcnow)
    
    # Последняя активность
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Счётчик команд
    total_commands = Column(Integer, default=0)
    
    # Счётчики по типам команд
    weather_commands = Column(Integer, default=0)
    crypto_commands = Column(Integer, default=0)
    ai_commands = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<User {self.user_id} ({self.username})>"


class CommandLog(Base):
    """
    Модель логирования команд
    Хранит историю использования команд для аналитики
    """
    __tablename__ = "command_logs"
    
    # Уникальный ID записи
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # ID пользователя
    user_id = Column(BigInteger, index=True)
    
    # Название команды (weather, crypto, ai)
    command = Column(String(50), nullable=False)
    
    # Аргументы команды (город, монета, вопрос)
    arguments = Column(String(500), nullable=True)
    
    # Timestamp выполнения
    executed_at = Column(DateTime, default=datetime.utcnow)
    
    # Статус выполнения (success/error)
    status = Column(String(20), default="success")
    
    def __repr__(self):
        return f"<CommandLog {self.user_id}: {self.command}>"