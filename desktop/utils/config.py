"""Carregamento das variáveis de ambiente usadas pela aplicação desktop."""
import os
import warnings

from dotenv import load_dotenv

load_dotenv()

DEFAULT_JWT_SECRET_KEY = "dev-secret-change-me"


def _get_int(name, default):
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default


class Config:
    """Agrupa as configurações da aplicação lidas do ambiente/.env."""

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/brecho_manager")
    MONGO_DB = os.getenv("MONGO_DB", "brecho_manager")

    EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    EMAIL_PORT = _get_int("EMAIL_PORT", 587)
    EMAIL_USER = os.getenv("EMAIL_USER", "")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")

    RECOVERY_TOKEN_EXPIRY = _get_int("RECOVERY_TOKEN_EXPIRY", 86400)

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", DEFAULT_JWT_SECRET_KEY)
    JWT_EXPIRY_DAYS = _get_int("JWT_EXPIRY_DAYS", 7)

    APP_NAME = os.getenv("APP_NAME", "Brecho Manager")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5000")


config = Config()

if config.JWT_SECRET_KEY == DEFAULT_JWT_SECRET_KEY:
    warnings.warn(
        "JWT_SECRET_KEY não foi definido no ambiente/.env; usando um valor "
        "padrão inseguro. Defina uma chave secreta forte antes de usar em "
        "produção, pois qualquer pessoa pode forjar tokens válidos.",
        stacklevel=2,
    )
