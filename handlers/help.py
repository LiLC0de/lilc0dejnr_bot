"""
Обработчик команды /help
Список всех доступных команд с описаниями
"""
from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Обработка команды /help"""
    help_text = (
        "📋 <b>Доступные команды:</b>\n\n"
        "🚀 <b>Основные:</b>\n"
        "/start — Приветствие и регистрация\n"
        "/help — Список команд (ты здесь)\n\n"
        "🌤 <b>Погода:</b>\n"
        "/weather <code>Москва</code> — погода сейчас\n"
        "/weather <code>Киев</code> forecast — прогноз\n\n"
        "💰 <b>Криптовалюты:</b>\n"
        "/crypto <code>bitcoin</code> — курс BTC\n"
        "/crypto <code>ethereum</code> — курс ETH\n"
        "/top — топ-10 криптовалют\n\n"
        "🤖 <b>AI-помощник:</b>\n"
        "/ai <code>твой вопрос</code> — спроси ChatGPT\n\n"
        "📊 <b>Статистика:</b>\n"
        "/stats — твоя статистика\n\n"
        "💡 <i>Совет: команды можно писать без / в личных сообщениях</i>"
    )
    
    await message.answer(help_text)