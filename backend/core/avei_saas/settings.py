import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Charger fichier .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------
# BASE DJANGO
# ---------------------------

SECRET_KEY = os.getenv("SECRET_KEY", "changeme_local")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# ---------------------------
# APPS INSTALLÉES
# ---------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps externes
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    # Ton app
    'core',
]

# ---------------------------
# MIDDLEWARE
# ---------------------------

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'avei_saas.urls'

# ---------------------------
# TEMPLATES
# ---------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'avei_saas.wsgi.application'
ASGI_APPLICATION = 'avei_saas.asgi.application'

# ---------------------------
# BASE DE DONNÉES (PostgreSQL)
# ---------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("PG_DB"),
        'USER': os.getenv("PG_USER"),
        'PASSWORD': os.getenv("PG_PASS"),
        'HOST': os.getenv("PG_HOST", "db"),
        'PORT': os.getenv("PG_PORT", "5432"),
    }
}

# ---------------------------
# UTILISATEUR CUSTOM
# ---------------------------

AUTH_USER_MODEL = "core.User"

# ---------------------------
# CONFIG REST FRAMEWORK
# ---------------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# ---------------------------
# AUTH JWT
# ---------------------------

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=90),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ---------------------------
# DÉFINITION FICHIERS STATIQUES
# ---------------------------

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------
# CORS (autoriser frontend)
# ---------------------------

CORS_ALLOW_ALL_ORIGINS = True

# ---------------------------
# EMAILS (pour notifications)
# ---------------------------

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "no-reply@avei.local")

# ---------------------------
# REDIS + CELERY
# ---------------------------

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

