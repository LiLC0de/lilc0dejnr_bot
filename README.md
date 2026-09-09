# 🤖 @lilc0dejnr_bot

Telegram бот-помощник с интеграцией погоды, криптовалют и AI.

## ✨ Возможности

- 🌤 **Погода** — актуальная погода в любом городе
- 💰 **Криптовалюты** — курсы BTC, ETH и других монет
- 🤖 **AI-помощник** — ответы на вопросы через ChatGPT
- 📊 **Статистика** — просмотр использования бота
- 💾 **База данных** — хранение пользовательских данных

## 🚀 Установка

### 1. Клонируй репозиторий
```bash
git clone https://github.com/LiLC0de/lilc0dejnr_bot.git
cd lilc0dejnr_bot
```

### 2. Установи зависимости
```bash
pip install -r requirements.txt
```

### 3. Настрой окружение
```bash
cp .env.example .env
# Отредактируй .env и добавь свои API ключи
```

### 4. Запусти бота
```bash
python bot.py
```

## 📝 Команды бота

- `/start` — Приветствие и регистрация
- `/help` — Список доступных команд
- `/weather <город>` — Погода в городе
- `/crypto <монета>` — Курс криптовалюты
- `/ai <вопрос>` — Задать вопрос AI
- `/stats` — Статистика использования

## 🛠 Технологии

- **Python 3.10+**
- **Aiogram 3.x** — асинхронный фреймворк для Telegram Bot API
- **SQLAlchemy** — ORM для базы данных
- **SQLite** — локальная база данных (по умолчанию)
- **OpenAI API** — интеграция с ChatGPT

## 📦 Структура проекта

```
lilc0dejnr_bot/
├── bot.py              # Главный файл запуска
├── config.py           # Конфигурация
├── requirements.txt    # Зависимости
├── .env               # Переменные окружения
├── handlers/          # Обработчики команд
│   ├── start.py
│   ├── help.py
│   ├── weather.py
│   ├── crypto.py
│   ├── ai.py
│   └── stats.py
├── services/          # API сервисы
│   ├── weather_api.py
│   ├── crypto_api.py
│   └── ai_service.py
├── database/          # База данных
│   ├── database.py
│   └── models.py
└── utils/             # Утилиты
    ├── logger.py
    └── decorators.py
```

## 🔑 Получение API ключей

### Telegram Bot Token
1. Открой [@BotFather](https://t.me/BotFather) в Telegram
2. Отправь `/newbot` и следуй инструкциям
3. Скопируй токен в `.env`

### OpenWeatherMap API
1. Зарегистрируйся на [openweathermap.org](https://openweathermap.org/api)
2. Создай API ключ (бесплатно)
3. Добавь в `.env`

### CoinMarketCap API
1. Зарегистрируйся на [coinmarketcap.com/api](https://coinmarketcap.com/api/)
2. Получи бесплатный API ключ
3. Добавь в `.env`

### OpenAI API
1. Зарегистрируйся на [platform.openai.com](https://platform.openai.com/)
2. Создай API ключ
3. Добавь в `.env`

## 🐳 Docker (опционально)

```bash
docker-compose up -d
```

## 📄 Лицензия

MIT License

## 👨‍💻 Автор

LiL C. — [GitHub](https://github.com/LiLC0de) | [Telegram](https://t.me/lilc0d3)