"""Funções de validação de entrada (email, senha, etc)."""
import re

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

MIN_PASSWORD_LENGTH = 8


def is_valid_email(email):
    """Valida se a string informada tem um formato de email válido."""
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def validate_password_strength(password):
    """Valida a força da senha.

    Retorna uma tupla (valido, mensagem). A senha precisa ter no mínimo
    ``MIN_PASSWORD_LENGTH`` caracteres, além de conter ao menos uma letra
    maiúscula, uma letra minúscula e um número.
    """
    if not password:
        return False, "A senha não pode ser vazia."

    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"A senha deve ter no mínimo {MIN_PASSWORD_LENGTH} caracteres."

    if not re.search(r"[A-Z]", password):
        return False, "A senha deve conter ao menos uma letra maiúscula."

    if not re.search(r"[a-z]", password):
        return False, "A senha deve conter ao menos uma letra minúscula."

    if not re.search(r"\d", password):
        return False, "A senha deve conter ao menos um número."

    return True, ""


def passwords_match(password, confirmation):
    """Verifica se a senha e a confirmação são iguais."""
    return bool(password) and password == confirmation


def is_not_empty(value):
    """Valida se o valor informado não é vazio (após remover espaços)."""
    return bool(value and value.strip())
