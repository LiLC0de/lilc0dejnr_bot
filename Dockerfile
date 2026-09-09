FROM python:3.11-slim

# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Создание директории для данных
RUN mkdir -p /app/data

# Команда запуска
CMD ["python", "bot.py"]