"""
Django settings for mysite_recipe project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Определяем базовую директорию проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Определяем путь к .env файлу (поддержка продакшена)
ENV_FILE = BASE_DIR.parent / ".env.prod" if os.getenv("DJANGO_PRODUCTION") else BASE_DIR.parent / ".env"
load_dotenv(ENV_FILE)

# Безопасный ключ
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")

# Режим DEBUG (конвертируем в bool)
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

# Разрешенные хосты
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",") if os.getenv("ALLOWED_HOSTS") else []

ROOT_URLCONF = "mysite_recipe.urls"

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if os.getenv("CSRF_TRUSTED_ORIGINS") else []

# Разрешенные внутренние IP (для Debug Toolbar)
INTERNAL_IPS = os.getenv("INTERNAL_IPS", "127.0.0.1").split(",")

# Подключенные приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.recipe.apps.RecipeConfig',
    'debug_toolbar',
    'apps.accounts',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.postgres',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'apps.accounts.middleware.ActiveUserMiddleware',
]

# Конфигурация базы данных
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.getenv("DB_NAME", "postgres"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite_recipe.wsgi.application'

# Конфигурация кеширования
CACHE_LOCATION = os.getenv("CACHE_LOCATION", "/tmp/django_cache")
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": CACHE_LOCATION,
        "TIMEOUT": int(os.getenv("CACHE_TIMEOUT", 300)),  # Таймаут кэша
    }
}


# Настройки почты
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() in ("true", "1", "yes")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

# Статические и медиа файлы
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATIC_ROOT = BASE_DIR / "static" if not DEBUG else None
MEDIA_ROOT = BASE_DIR / "media"

if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / "static"]

# Логирование
LOGFILE_PATH = os.getenv("LOGFILE_PATH", BASE_DIR / "logs" / "django.log")
LOGFILE_SIZE = int(os.getenv("LOGFILE_SIZE", 10485760))  # 10MB
LOGFILE_COUNT = int(os.getenv("LOGFILE_COUNT", 5))

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(levelname)s] %(asctime)s %(module)s %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "logfile": {
            "class": "concurrent_log_handler.ConcurrentRotatingFileHandler",
            "filename": LOGFILE_PATH,
            "maxBytes": LOGFILE_SIZE,
            "backupCount": LOGFILE_COUNT,
            "encoding": "utf-8",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "logfile"],
        "level": "INFO",
    },
}

# Безопасность
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
