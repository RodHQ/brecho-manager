"""Serviço de recuperação de senha: geração de token, validação e redefinição."""
from db.mongodb_connection import get_connection
from models.recovery_token_model import RecoveryToken, novo_recovery_token_documento
from services.email_service import EmailService
from utils.config import config
from utils.hash_password import hash_password


class RecoveryError(Exception):
    """Erro genérico do fluxo de recuperação de senha."""


class RecoveryService:
    def __init__(self, connection=None, email_service=None):
        self._connection = connection or get_connection()
        self._email_service = email_service or EmailService()

    def solicitar_recuperacao(self, email):
        """Gera um token de recuperação para o email informado e envia por email.

        Lança ``RecoveryError`` caso o email não esteja cadastrado.
        """
        usuario_doc = self._connection.find_usuario_by_email(email)
        if not usuario_doc:
            raise RecoveryError("Não encontramos um usuário com esse email.")

        token_doc = novo_recovery_token_documento(
            usuario_doc["_id"], config.RECOVERY_TOKEN_EXPIRY
        )
        self._connection.insert_recovery_token(token_doc)

        self._email_service.enviar_email_recuperacao(email, token_doc["token"])
        return token_doc["token"]

    def validar_token(self, token):
        """Valida se o token existe, não foi usado e não expirou."""
        if not token:
            raise RecoveryError("Token de recuperação inválido.")

        token_doc = self._connection.find_recovery_token(token)
        if not token_doc:
            raise RecoveryError("Token de recuperação inválido.")

        recovery_token = RecoveryToken(token_doc)
        if not recovery_token.is_valido():
            raise RecoveryError("Token de recuperação expirado ou já utilizado.")

        return recovery_token

    def redefinir_senha(self, token, nova_senha):
        """Valida o token, atualiza a senha do usuário e invalida o token."""
        recovery_token = self.validar_token(token)

        hashed = hash_password(nova_senha)
        usuario_atualizado = self._connection.update_usuario_password(
            recovery_token.usuario_id, hashed
        )
        if not usuario_atualizado:
            raise RecoveryError("Usuário associado ao token não foi encontrado.")

        self._connection.invalidate_recovery_token(token)
        return True
