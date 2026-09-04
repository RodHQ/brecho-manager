"""Testes do serviço de autenticação (login, geração e verificação de token)."""
import pytest

from services.auth_service import AuthError, AuthService
from utils.hash_password import hash_password


class FakeConnection:
    """Substitui a conexão com o MongoDB para os testes de autenticação."""

    def __init__(self, usuarios=None):
        self.usuarios = usuarios or {}

    def find_usuario_by_email_ou_username(self, identifier):
        for usuario in self.usuarios.values():
            if usuario["email"] == identifier or usuario["username"] == identifier:
                return usuario
        return None


@pytest.fixture
def usuario_ativo():
    return {
        "_id": "abc123",
        "username": "joao",
        "email": "joao@teste.com",
        "password": hash_password("SenhaForte123"),
        "nome": "João",
        "ativo": True,
    }


@pytest.fixture
def auth_service(usuario_ativo):
    connection = FakeConnection({usuario_ativo["_id"]: usuario_ativo})
    return AuthService(connection=connection)


class TestLogin:
    def test_login_success_with_email(self, auth_service):
        usuario, token = auth_service.login("joao@teste.com", "SenhaForte123")
        assert usuario.username == "joao"
        assert token

    def test_login_success_with_username(self, auth_service):
        usuario, token = auth_service.login("joao", "SenhaForte123")
        assert usuario.email == "joao@teste.com"
        assert token

    def test_login_wrong_password(self, auth_service):
        with pytest.raises(AuthError):
            auth_service.login("joao@teste.com", "SenhaErrada")

    def test_login_unknown_user(self, auth_service):
        with pytest.raises(AuthError):
            auth_service.login("desconhecido@teste.com", "SenhaForte123")

    def test_login_missing_fields(self, auth_service):
        with pytest.raises(AuthError):
            auth_service.login("", "")

    def test_login_inactive_user(self, usuario_ativo):
        usuario_ativo["ativo"] = False
        connection = FakeConnection({usuario_ativo["_id"]: usuario_ativo})
        service = AuthService(connection=connection)
        with pytest.raises(AuthError):
            service.login("joao@teste.com", "SenhaForte123")


class TestTokenJWT:
    def test_gerar_e_verificar_token(self, auth_service, usuario_ativo):
        usuario, token = auth_service.login("joao", "SenhaForte123")
        payload = auth_service.verificar_token(token)
        assert payload is not None
        assert payload["username"] == "joao"
        assert payload["email"] == "joao@teste.com"

    def test_verificar_token_invalido(self, auth_service):
        assert auth_service.verificar_token("token-invalido") is None

    def test_verificar_token_vazio(self, auth_service):
        assert auth_service.verificar_token("") is None
