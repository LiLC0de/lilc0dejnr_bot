"""
Обработчик команд погоды
/weather <город> — текущая погода
/weather <город> forecast — прогноз
"""
import logging
from aiogram import Router, types
from aiogram.filters import Command
from services.weather_api import get_weather, get_forecast
from database.database import update_user_stats

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("weather"))
async def cmd_weather(message: types.Message):
    """Обработка команды /weather"""
    # Извлечение аргументов
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.answer(
            "🌤 Укажи город:\n"
            "<code>/weather Москва</code>\n"
            "<code>/weather Киев forecast</code> — прогноз"
        )
        return
    
    parts = args[1].strip().split()
    city = parts[0]
    is_forecast = len(parts) > 1 and parts[1].lower() in ("forecast", "прогноз", "прогноз")
    
    await message.answer("⏳ Загружаю данные о погоде...")
    
    try:
        if is_forecast:
            # Прогноз на 5 дней
            result = await get_forecast(city)
        else:
            # Текущая погода
            result = await get_weather(city)
        
        if result:
            await message.answer(result, parse_mode="HTML")
        else:
            await message.answer(f"❌ Не удалось найти погоду для <b>{city}</b>")
    
    except Exception as e:
        logger.error(f"Ошибка погоды: {e}")
        await message.answer("❌ Ошибка при получении данных. Попробуй позже.")
    
    # Обновление статистики
    await update_user_stats(message.from_user.id, "weather")