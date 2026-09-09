"""
Обработчик команд криптовалют
/crypto <монета> — курс
/top — топ-10 криптовалют
"""
import logging
from aiogram import Router, types
from aiogram.filters import Command
from services.crypto_api import get_crypto_price, get_top_cryptos
from database.database import update_user_stats

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("crypto"))
async def cmd_crypto(message: types.Message):
    """Обработка команды /crypto"""
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.answer(
            "💰 Укажи криптовалюту:\n"
            "<code>/crypto bitcoin</code>\n"
            "<code>/crypto ethereum</code>\n"
            "<code>/crypto ton</code>"
        )
        return
    
    coin = args[1].strip().lower()
    
    await message.answer("⏳ Загружаю курс...")
    
    try:
        result = await get_crypto_price(coin)
        
        if result:
            await message.answer(result, parse_mode="HTML")
        else:
            await message.answer(f"❌ Не удалось найти <b>{coin}</b>")
    
    except Exception as e:
        logger.error(f"Ошибка крипты: {e}")
        await message.answer("❌ Ошибка при получении данных. Попробуй позже.")
    
    await update_user_stats(message.from_user.id, "crypto")


@router.message(Command("top"))
async def cmd_top(message: types.Message):
    """Обработка команды /top — топ-10 криптовалют"""
    await message.answer("⏳ Загружаю топ криптовалют...")
    
    try:
        result = await get_top_cryptos()
        
        if result:
            await message.answer(result, parse_mode="HTML")
        else:
            await message.answer("❌ Не удалось загрузить топ")
    
    except Exception as e:
        logger.error(f"Ошибка топ крипты: {e}")
        await message.answer("❌ Ошибка при получении данных.")
    
    await update_user_stats(message.from_user.id, "crypto")