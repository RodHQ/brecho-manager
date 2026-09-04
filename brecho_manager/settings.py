"""Django settings for brecho_manager."""

import os
from pathlib import Path

import mongoengine
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-development-only-change-me",
)
DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() in {"1", "true", "yes"}
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS if host.strip()]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "core",
    "usuarios",
    "clientes",
    "fornecedores",
    "estoque",
    "transacoes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "brecho_manager.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "brecho_manager.wsgi.application"
ASGI_APPLICATION = "brecho_manager.asgi.application"

# Não há banco de dados relacional configurado. MongoDB via MongoEngine é o
# único banco de dados (ver `mongoengine.Document` nos módulos `models.py`).
# Recursos do Django que dependem de um banco relacional (Django Admin,
# sessões e autenticação padrão via `django.contrib.auth`) não estão
# habilitados, já que os modelos de domínio agora são Documents do
# MongoEngine em vez de Models do Django ORM.
DATABASES = {}

# Conexão com o MongoDB via MongoEngine, configurada por variáveis de
# ambiente (ver `.env.example`). O host/porta/usuário/senha também
# alimentam o `docker-compose.yml`.
MONGO_DB = os.environ.get("MONGO_DB", "brecho_manager")
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = int(os.environ.get("MONGO_PORT", "27017"))
MONGO_USERNAME = os.environ.get("MONGO_USERNAME") or None
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD") or None

MONGODB_SETTINGS = {
    "db": MONGO_DB,
    "host": MONGO_HOST,
    "port": MONGO_PORT,
}
if MONGO_USERNAME and MONGO_PASSWORD:
    MONGODB_SETTINGS.update(
        {
            "username": MONGO_USERNAME,
            "password": MONGO_PASSWORD,
            "authentication_source": "admin",
        }
    )

mongoengine.connect(**MONGODB_SETTINGS)

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
