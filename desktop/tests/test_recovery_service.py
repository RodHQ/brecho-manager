"""Testes do serviço de recuperação de senha (geração de token, validação, redefinição)."""
import datetime

import pytest

from models.recovery_token_model import gerar_token, novo_recovery_token_documento
from services.recovery_service import RecoveryError, RecoveryService
from utils.hash_password import check_password


class FakeEmailService:
    def __init__(self):
        self.enviados = []

    def enviar_email_recuperacao(self, destinatario, token):
        self.enviados.append((destinatario, token))
        return True


class FakeConnection:
    def __init__(self, usuarios=None, tokens=None):
        self.usuarios = usuarios or {}
        self.tokens = tokens or {}

    def find_usuario_by_email(self, email):
        for usuario in self.usuarios.values():
            if usuario["email"] == email:
                return usuario
        return None

    def insert_recovery_token(self, token_doc):
        self.tokens[token_doc["token"]] = token_doc
        return token_doc["token"]

    def find_recovery_token(self, token):
        return self.tokens.get(token)

    def update_usuario_password(self, usuario_id, hashed_password):
        for usuario in self.usuarios.values():
            if usuario["_id"] == usuario_id:
                usuario["password"] = hashed_password
                return usuario
        return None

    def invalidate_recovery_token(self, token):
        if token in self.tokens:
            self.tokens[token]["usado"] = True
        return self.tokens.get(token)


@pytest.fixture
def usuario():
    return {
        "_id": "user-1",
        "email": "maria@teste.com",
        "password": "hash-antigo",
    }


@pytest.fixture
def connection(usuario):
    return FakeConnection(usuarios={usuario["_id"]: usuario})


@pytest.fixture
def email_service():
    return FakeEmailService()


@pytest.fixture
def recovery_service(connection, email_service):
    return RecoveryService(connection=connection, email_service=email_service)


class TestGerarToken:
    def test_gerar_token_unico(self):
        assert gerar_token() != gerar_token()

    def test_novo_recovery_token_documento_expira_corretamente(self):
        doc = novo_recovery_token_documento("user-1", 3600)
        assert doc["usado"] is False
        assert doc["expira_em"] > doc["criado_em"]
        delta = doc["expira_em"] - doc["criado_em"]
        assert abs(delta.total_seconds() - 3600) < 1


class TestSolicitarRecuperacao:
    def test_solicitar_recuperacao_email_existente(
        self, recovery_service, email_service, connection
    ):
        token = recovery_service.solicitar_recuperacao("maria@teste.com")
        assert token in connection.tokens
        assert email_service.enviados == [("maria@teste.com", token)]

    def test_solicitar_recuperacao_email_inexistente(self, recovery_service):
        with pytest.raises(RecoveryError):
            recovery_service.solicitar_recuperacao("desconhecido@teste.com")


class TestValidarToken:
    def test_token_valido(self, recovery_service, connection):
        token = recovery_service.solicitar_recuperacao("maria@teste.com")
        recovery_token = recovery_service.validar_token(token)
        assert recovery_token.token == token

    def test_token_inexistente(self, recovery_service):
        with pytest.raises(RecoveryError):
            recovery_service.validar_token("token-que-nao-existe")

    def test_token_expirado(self, recovery_service, connection):
        token = recovery_service.solicitar_recuperacao("maria@teste.com")
        connection.tokens[token]["expira_em"] = (
            datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
        )
        with pytest.raises(RecoveryError):
            recovery_service.validar_token(token)

    def test_token_ja_usado(self, recovery_service, connection):
        token = recovery_service.solicitar_recuperacao("maria@teste.com")
        connection.tokens[token]["usado"] = True
        with pytest.raises(RecoveryError):
            recovery_service.validar_token(token)


class TestRedefinirSenha:
    def test_redefine_senha_com_sucesso(self, recovery_service, connection, usuario):
        token = recovery_service.solicitar_recuperacao("maria@teste.com")
        assert recovery_service.redefinir_senha(token, "NovaSenha123") is True
        assert check_password("NovaSenha123", usuario["password"])
        assert connection.tokens[token]["usado"] is True

    def test_nao_permite_reutilizar_token(self, recovery_service, connection):
        token = recovery_service.solicitar_recuperacao("maria@teste.com")
        recovery_service.redefinir_senha(token, "NovaSenha123")
        with pytest.raises(RecoveryError):
            recovery_service.redefinir_senha(token, "OutraSenha123")
