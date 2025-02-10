# Используем образ Python на основе Alpine
FROM python:3.12.0-alpine

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости, необходимые для сборки psycopg2
RUN apk add --no-cache \
    postgresql-dev gcc python3-dev musl-dev icu icu-dev icu-data-full

# Копируем файл зависимостей
COPY requirements.txt requirements.txt

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта FastAPI
COPY . .

# Открываем порт для FastAPI
EXPOSE 8001

# Запускаем FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]