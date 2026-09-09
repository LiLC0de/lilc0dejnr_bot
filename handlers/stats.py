"""
Обработчик команды /stats
Показывает статистику использования бота
"""
import logging
from aiogram import Router, types
from aiogram.filters import Command
from database.database import get_session, get_user_stats, get_total_stats
from database.models import User

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    """Обработка команды /stats"""
    user_id = message.from_user.id
    
    # Статистика пользователя
    user_stats = await get_user_stats(user_id)
    
    # Общая статистика
    total_stats = await get_total_stats()
    
    stats_text = (
        "📊 <b>Твоя статистика:</b>\n\n"
        f"📨 Команд использовано: <b>{user_stats.get('total_commands', 0)}</b>\n"
        f"🌤 Погода: <b>{user_stats.get('weather', 0)}</b>\n"
        f"💰 Крипта: <b>{user_stats.get('crypto', 0)}</b>\n"
        f"🤖 AI: <b>{user_stats.get('ai', 0)}</b>\n\n"
        f"👥 <b>Всего пользователей:</b> {total_stats.get('total_users', 0)}\n"
        f"📨 <b>Всего команд:</b> {total_stats.get('total_commands', 0)}"
    )
    
    await message.answer(stats_text)