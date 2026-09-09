"""
Обработчик команды /start
Регистрация пользователя и приветствие
"""
import logging
from aiogram import Router, types
from aiogram.filters import Command
from database.database import get_session
from database.models import User
from datetime import datetime

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработка команды /start"""
    user_id = message.from_user.id
    username = message.from_user.username or ""
    first_name = message.from_user.first_name or "Пользователь"
    
    # Проверка: существует ли пользователь в БД
    async with get_session() as session:
        existing_user = await session.get(User, user_id)
        
        if not existing_user:
            # Регистрация нового пользователя
            new_user = User(
                user_id=user_id,
                username=username,
                first_name=first_name,
                registered_at=datetime.utcnow()
            )
            session.add(new_user)
            await session.commit()
            logger.info(f"Новый пользователь: {user_id} (@{username})")
        else:
            # Обновление last_active
            existing_user.last_active = datetime.utcnow()
            await session.commit()
    
    # Приветственное сообщение
    welcome_text = (
        f"Привет, <b>{first_name}</b>! 🤙\n\n"
        f"Я бот-помощник <b>@lilc0dejnr_bot</b>.\n\n"
        f"<b>Что я умею:</b>\n"
        f"🌤 /weather <code>город</code> — погода\n"
        f"💰 /crypto <code>монета</code> — курс крипты\n"
        f"🤖 /ai <code>вопрос</code> — спроси AI\n"
        f"📊 /stats — статистика\n"
        f"❓ /help — все команды\n\n"
        f"Выбирай команду и погнали! 🚀"
    )
    
    await message.answer(welcome_text)