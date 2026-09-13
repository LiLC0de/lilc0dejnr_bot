"""
Crypto Handler
Команды для получения курса криптовалют
"""
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from services.crypto_api import get_crypto_price

router = Router()


@router.message(Command("crypto"))
async def cmd_crypto(message: Message):
    """Команда /crypto <монета>"""
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.answer(
            "💰 <b>Использование:</b>\n\n"
            "<code>/crypto bitcoin</code>\n"
            "<code>/crypto ethereum</code>\n"
            "<code>/crypto toncoin</code>\n\n"
            "Или используй inline: <code>@lilc0dejnr_bot crypto bitcoin</code>"
        )
        return
    
    coin = args[1].lower()
    crypto_data = await get_crypto_price(coin)
    
    if crypto_data:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📊 График",
                    callback_data=f"crypto_chart_{coin}"
                ),
                InlineKeyboardButton(
                    text="ℹ️ Инфо",
                    callback_data=f"crypto_info_{coin}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Обновить курс",
                    callback_data=f"crypto_refresh_{coin}"
                )
            ]
        ])
        
        await message.answer(crypto_data, reply_markup=keyboard)
    else:
        await message.answer(
            f"❌ Не удалось получить курс для <b>{coin}</b>\n\n"
            "Проверь название криптовалюты."
        )
