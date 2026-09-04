"""Utilitário para hash e verificação de senhas usando bcrypt."""
import bcrypt


def hash_password(raw_password):
    """Gera o hash bcrypt de uma senha em texto puro."""
    if not raw_password:
        raise ValueError("A senha não pode ser vazia.")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(raw_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def check_password(raw_password, hashed_password):
    """Verifica se a senha em texto puro corresponde ao hash armazenado."""
    if not raw_password or not hashed_password:
        return False
    try:
        return bcrypt.checkpw(
            raw_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except (ValueError, TypeError):
        return False
