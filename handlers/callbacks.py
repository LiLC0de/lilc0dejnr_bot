"""
Callback Query Handler
Обработка нажатий на inline-кнопки
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from services.weather_api import get_weather, get_forecast
from services.crypto_api import get_crypto_price

router = Router()


@router.callback_query(F.data.startswith("weather_"))
async def weather_callback(callback: CallbackQuery):
    """Обработка callback'ов для погоды"""
    parts = callback.data.split("_")
    action = parts[1]
    city = " ".join(parts[2:])
    
    if action == "forecast":
        forecast = await get_forecast(city)
        if forecast:
            await callback.message.edit_text(forecast)
            await callback.answer("Прогноз загружен ✓")
        else:
            await callback.answer("❌ Не удалось получить прогноз", show_alert=True)
    
    elif action == "refresh":
        weather = await get_weather(city)
        if weather:
            await callback.message.edit_text(weather)
            await callback.answer("Данные обновлены ✓")
        else:
            await callback.answer("❌ Не удалось обновить", show_alert=True)
    
    elif action == "details":
        details = await get_weather(city, detailed=True)
        if details:
            await callback.message.edit_text(details)
            await callback.answer("Детали загружены ✓")
        else:
            await callback.answer("❌ Детали недоступны", show_alert=True)


@router.callback_query(F.data.startswith("crypto_"))
async def crypto_callback(callback: CallbackQuery):
    """Обработка callback'ов для криптовалют"""
    parts = callback.data.split("_")
    action = parts[1]
    coin = parts[2] if len(parts) > 2 else "bitcoin"
    
    if action == "refresh":
        price = await get_crypto_price(coin)
        if price:
            await callback.message.edit_text(price)
            await callback.answer("Курс обновлён ✓")
        else:
            await callback.answer("❌ Не удалось обновить", show_alert=True)
    
    elif action == "chart":
        await callback.answer("📊 График скоро будет доступен", show_alert=True)
    
    elif action == "info":
        info = await get_crypto_price(coin, detailed=True)
        if info:
            await callback.message.edit_text(info)
            await callback.answer("Информация загружена ✓")
        else:
            await callback.answer("❌ Информация недоступна", show_alert=True)
