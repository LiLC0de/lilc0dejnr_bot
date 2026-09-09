"""
Сервис для работы с OpenAI API
Интеграция с ChatGPT для ответов на вопросы
"""
import logging
from openai import AsyncOpenAI
from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

# Инициализация клиента OpenAI
client = AsyncOpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


async def ask_ai(question: str) -> str:
    """
    Задать вопрос ChatGPT
    
    Args:
        question: Вопрос пользователя
    
    Returns:
        Ответ AI или None при ошибке
    """
    if not client:
        logger.error("OPENAI_API_KEY не установлен")
        return None
    
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты — полезный AI-помощник в Telegram боте. "
                        "Отвечай кратко, по делу и дружелюбно. "
                        "Используй эмодзи умеренно. "
                        "Отвечай на языке пользователя."
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        answer = response.choices[0].message.content
        return answer
    
    except Exception as e:
        logger.error(f"Ошибка AI запроса: {e}")
        return None