"""
Сервис для работы с OpenWeatherMap API
Получение текущей погоды и прогноза
"""
import aiohttp
import logging
from config import WEATHER_API_KEY

logger = logging.getLogger(__name__)

BASE_URL = "https://api.openweathermap.org/data/2.5"


async def get_weather(city: str) -> str:
    """
    Получение текущей погоды для города
    
    Args:
        city: Название города
    
    Returns:
        Строка с информацией о погоде или None при ошибке
    """
    if not WEATHER_API_KEY:
        logger.error("WEATHER_API_KEY не установлен")
        return None
    
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}/weather", params=params) as response:
                if response.status != 200:
                    logger.error(f"Ошибка API погоды: {response.status}")
                    return None
                
                data = await response.json()
                
                # Форматирование ответа
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                description = data["weather"][0]["description"]
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]
                city_name = data["name"]
                country = data["sys"]["country"]
                
                # Эмодзи для погоды
                weather_emoji = get_weather_emoji(data["weather"][0]["main"])
                
                result = (
                    f"{weather_emoji} <b>Погода в {city_name}, {country}</b>\n\n"
                    f"🌡 Температура: <b>{temp:.1f}°C</b>\n"
                    f"🤔 Ощущается: <b>{feels_like:.1f}°C</b>\n"
                    f"☁️ {description.capitalize()}\n"
                    f"💧 Влажность: <b>{humidity}%</b>\n"
                    f"💨 Ветер: <b>{wind_speed} м/с</b>"
                )
                
                return result
    
    except Exception as e:
        logger.error(f"Ошибка получения погоды: {e}")
        return None


async def get_forecast(city: str) -> str:
    """
    Получение прогноза погоды на 5 дней
    
    Args:
        city: Название города
    
    Returns:
        Строка с прогнозом или None при ошибке
    """
    if not WEATHER_API_KEY:
        logger.error("WEATHER_API_KEY не установлен")
        return None
    
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "ru",
        "cnt": 5  # 5 прогнозов (каждые 3 часа)
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}/forecast", params=params) as response:
                if response.status != 200:
                    logger.error(f"Ошибка API прогноза: {response.status}")
                    return None
                
                data = await response.json()
                city_name = data["city"]["name"]
                country = data["city"]["country"]
                
                forecast_lines = [f"📅 <b>Прогноз для {city_name}, {country}:</b>\n"]
                
                for item in data["list"]:
                    dt = item["dt_txt"]
                    temp = item["main"]["temp"]
                    description = item["weather"][0]["description"]
                    weather_emoji = get_weather_emoji(item["weather"][0]["main"])
                    
                    # Форматирование даты
                    date_part = dt.split()[0][5:]  # MM-DD
                    time_part = dt.split()[1][:5]  # HH:MM
                    
                    forecast_lines.append(
                        f"{weather_emoji} <b>{date_part} {time_part}</b>\n"
                        f"   🌡 {temp:.1f}°C — {description.capitalize()}\n"
                    )
                
                return "\n".join(forecast_lines)
    
    except Exception as e:
        logger.error(f"Ошибка получения прогноза: {e}")
        return None


def get_weather_emoji(condition: str) -> str:
    """Возвращает эмодзи для типа погоды"""
    emoji_map = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧",
        "Drizzle": "🌦",
        "Thunderstorm": "⛈",
        "Snow": "🌨",
        "Mist": "🌫",
        "Fog": "🌫",
        "Haze": "🌫"
    }
    return emoji_map.get(condition, "🌤")