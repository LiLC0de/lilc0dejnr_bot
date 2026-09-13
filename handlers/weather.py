"""
Weather Handler
Команды для получения погоды
"""
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from services.weather_api import get_weather

router = Router()


@router.message(Command("weather"))
async def cmd_weather(message: Message):
    """Команда /weather <город>"""
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.answer(
            "🌤 <b>Использование:</b>\n\n"
            "<code>/weather Москва</code>\n"
            "<code>/weather Киев</code>\n\n"
            "Или используй inline: <code>@lilc0dejnr_bot погода Киев</code>"
        )
        return
    
    city = args[1]
    weather_data = await get_weather(city)
    
    if weather_data:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📅 Прогноз",
                    callback_data=f"weather_forecast_{city}"
                ),
                InlineKeyboardButton(
                    text="💨 Детали",
                    callback_data=f"weather_details_{city}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Обновить",
                    callback_data=f"weather_refresh_{city}"
                )
            ]
        ])
        
        await message.answer(weather_data, reply_markup=keyboard)
    else:
        await message.answer(
            f"❌ Не удалось получить погоду для <b>{city}</b>\n\n"
            "Проверь название города или попробуй другой."
        )
