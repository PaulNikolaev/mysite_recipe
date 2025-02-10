# Используем Python на основе Alpine
FROM python:3.12.0-alpine

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости для PostgreSQL
RUN apk add --no-cache \
    postgresql-dev gcc python3-dev musl-dev icu icu-dev icu-data-full

# Копируем файл зависимостей
COPY requirements.txt requirements.txt

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код Django-проекта (ТОЛЬКО `app_django`, а не всё)
COPY . .

# Открываем порт 8000
EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]