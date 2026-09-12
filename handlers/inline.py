"""
Inline Mode Handler
Позволяет использовать бота в любом чате через @lilc0dejnr_bot
Пример: @lilc0dejnr_bot погода Киев
"""
import logging
from aiogram import Router, types
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent
)
from services.weather_api import get_weather
from services.crypto_api import get_crypto_price

router = Router()
logger = logging.getLogger(__name__)


@router.inline_query()
async def inline_query(query: InlineQuery):
    """Обработка inline-запросов"""
    text = query.query.strip()
    
    if not text:
        # Подсказка при пустом запросе
        await query.answer([
            InlineQueryResultArticle(
                id="help",
                title="🤖 Помощь",
                description="Напиши: погода Киев, crypto bitcoin",
                input_message_content=InputTextMessageContent(
                    message_text=(
                        "📋 <b>Inline команды:</b>\n\n"
                        "• <code>погода Киев</code> — погода в городе\n"
                        "• <code>weather Moscow</code> — погода (EN)\n"
                        "• <code>crypto bitcoin</code> — курс BTC\n"
                        "• <code>crypto ethereum</code> — курс ETH\n\n"
                        "💡 <i>Работает в любом чате!</i>"
                    )
                )
            )
        ], cache_time=1)
        return
    
    # Парсинг команды
    parts = text.split(maxsplit=1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""
    
    results = []
    
    # Погода
    if command in ("погода", "weather", "weather") and args:
        weather_data = await get_weather(args)
        if weather_data:
            results.append(
                InlineQueryResultArticle(
                    id=f"weather_{args}",
                    title=f"🌤 Погода: {args}",
                    description="Нажми для отправки",
                    input_message_content=InputTextMessageContent(
                        message_text=weather_data
                    )
                )
            )
        else:
            results.append(
                InlineQueryResultArticle(
                    id=f"weather_error_{args}",
                    title=f"❌ Не удалось найти погоду для {args}",
                    description="Проверь название города",
                    input_message_content=InputTextMessageContent(
                        message_text=f"❌ Не удалось найти погоду для <b>{args}</b>"
                    )
                )
            )
    
    # Криптовалюты
    elif command in ("crypto", "крипта", "курс") and args:
        crypto_data = await get_crypto_price(args)
        if crypto_data:
            results.append(
                InlineQueryResultArticle(
                    id=f"crypto_{args}",
                    title=f"💰 Курс: {args.upper()}",
                    description="Нажми для отправки",
                    input_message_content=InputTextMessageContent(
                        message_text=crypto_data
                    )
                )
            )
        else:
            results.append(
                InlineQueryResultArticle(
                    id=f"crypto_error_{args}",
                    title=f"❌ Не удалось найти {args}",
                    description="Проверь название криптовалюты",
                    input_message_content=InputTextMessageContent(
                        message_text=f"❌ Не удалось найти <b>{args}</b>"
                    )
                )
            )
    
    # Неизвестная команда
    else:
        results.append(
            InlineQueryResultArticle(
                id="unknown",
                title="❓ Неизвестная команда",
                description=f"Попробуй: погода {text} или crypto {text}",
                input_message_content=InputTextMessageContent(
                    message_text=(
                        "❓ <b>Неизвестная команда</b>\n\n"
                        "Попробуй:\n"
                        f"• <code>погода {text}</code>\n"
                        f"• <code>crypto {text}</code>"
                    )
                )
            )
        )
    
    await query.answer(results, cache_time=5)
