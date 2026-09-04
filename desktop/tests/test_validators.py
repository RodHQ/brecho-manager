"""Testes das funções de validação (email, senha, etc)."""
from utils.validators import (
    is_not_empty,
    is_valid_email,
    passwords_match,
    validate_password_strength,
)


class TestIsValidEmail:
    def test_valid_emails(self):
        assert is_valid_email("usuario@exemplo.com")
        assert is_valid_email("nome.sobrenome@dominio.com.br")

    def test_invalid_emails(self):
        assert not is_valid_email("usuario@")
        assert not is_valid_email("usuario.com")
        assert not is_valid_email("")
        assert not is_valid_email(None)
        assert not is_valid_email("usuario @exemplo.com")


class TestValidatePasswordStrength:
    def test_valid_password(self):
        valido, mensagem = validate_password_strength("Senha1234")
        assert valido
        assert mensagem == ""

    def test_password_too_short(self):
        valido, mensagem = validate_password_strength("Ab1")
        assert not valido
        assert "8 caracteres" in mensagem

    def test_password_missing_uppercase(self):
        valido, mensagem = validate_password_strength("senha1234")
        assert not valido
        assert "maiúscula" in mensagem

    def test_password_missing_lowercase(self):
        valido, mensagem = validate_password_strength("SENHA1234")
        assert not valido
        assert "minúscula" in mensagem

    def test_password_missing_number(self):
        valido, mensagem = validate_password_strength("SenhaForte")
        assert not valido
        assert "número" in mensagem

    def test_empty_password(self):
        valido, mensagem = validate_password_strength("")
        assert not valido


class TestPasswordsMatch:
    def test_matching_passwords(self):
        assert passwords_match("Senha1234", "Senha1234")

    def test_non_matching_passwords(self):
        assert not passwords_match("Senha1234", "OutraSenha1")

    def test_empty_password(self):
        assert not passwords_match("", "")


class TestIsNotEmpty:
    def test_non_empty_value(self):
        assert is_not_empty("valor")

    def test_empty_value(self):
        assert not is_not_empty("")
        assert not is_not_empty("   ")
        assert not is_not_empty(None)
