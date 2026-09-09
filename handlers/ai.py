"""
Обработчик AI-команд
/ai <вопрос> — вопрос к ChatGPT
"""
import logging
from aiogram import Router, types
from aiogram.filters import Command
from services.ai_service import ask_ai
from database.database import update_user_stats

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("ai"))
async def cmd_ai(message: types.Message):
    """Обработка команды /ai"""
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.answer(
            "🤖 Задай мне вопрос:\n"
            "<code>/ai Как написать Telegram бота?</code>\n"
            "<code>/ai Объясни async/await в Python</code>"
        )
        return
    
    question = args[1].strip()
    
    await message.answer("🤔 Думаю...")
    
    try:
        answer = await ask_ai(question)
        
        if answer:
            # Telegram ограничивает сообщения до 4096 символов
            if len(answer) > 4000:
                answer = answer[:4000] + "\n\n... (обрезано)"
            
            await message.answer(answer, parse_mode="HTML")
        else:
            await message.answer("❌ Не удалось получить ответ. Попробуй позже.")
    
    except Exception as e:
        logger.error(f"Ошибка AI: {e}")
        await message.answer("❌ Ошибка при обработке запроса.")
    
    await update_user_stats(message.from_user.id, "ai")