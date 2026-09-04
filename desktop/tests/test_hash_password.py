"""Testes do utilitário de hash de senha (bcrypt)."""
import pytest

from utils.hash_password import check_password, hash_password


class TestHashPassword:
    def test_hash_is_different_from_raw_password(self):
        hashed = hash_password("MinhaSenha123")
        assert hashed != "MinhaSenha123"

    def test_hash_empty_raises(self):
        with pytest.raises(ValueError):
            hash_password("")


class TestCheckPassword:
    def test_correct_password(self):
        hashed = hash_password("MinhaSenha123")
        assert check_password("MinhaSenha123", hashed)

    def test_incorrect_password(self):
        hashed = hash_password("MinhaSenha123")
        assert not check_password("SenhaErrada", hashed)

    def test_empty_inputs(self):
        assert not check_password("", "algum-hash")
        assert not check_password("senha", "")
