"""Serviço de autenticação: login, geração e verificação de token JWT."""
import datetime

import jwt

from db.mongodb_connection import get_connection
from models.usuario_model import Usuario
from utils.config import config
from utils.hash_password import check_password


class AuthError(Exception):
    """Erro genérico de autenticação."""


class AuthService:
    def __init__(self, connection=None):
        self._connection = connection or get_connection()

    def login(self, identifier, password):
        """Valida usuário/email + senha e retorna (usuario, token) em caso de sucesso.

        Lança ``AuthError`` quando as credenciais são inválidas ou o usuário
        está inativo.
        """
        if not identifier or not password:
            raise AuthError("Informe usuário/email e senha.")

        doc = self._connection.find_usuario_by_email_ou_username(identifier)
        if not doc:
            raise AuthError("Usuário ou senha inválidos.")

        if not check_password(password, doc.get("password", "")):
            raise AuthError("Usuário ou senha inválidos.")

        if not doc.get("ativo", True):
            raise AuthError("Usuário inativo. Contate o administrador.")

        usuario = Usuario(doc)
        token = self.gerar_token(usuario)
        return usuario, token

    def gerar_token(self, usuario):
        """Gera um token JWT válido pelo período configurado (padrão: 7 dias)."""
        agora = datetime.datetime.now(datetime.timezone.utc)
        payload = {
            "sub": str(usuario.id),
            "username": usuario.username,
            "email": usuario.email,
            "iat": agora,
            "exp": agora + datetime.timedelta(days=config.JWT_EXPIRY_DAYS),
        }
        return jwt.encode(payload, config.JWT_SECRET_KEY, algorithm="HS256")

    def verificar_token(self, token):
        """Verifica e decodifica o token JWT. Retorna o payload ou ``None`` se inválido."""
        if not token:
            return None
        try:
            return jwt.decode(token, config.JWT_SECRET_KEY, algorithms=["HS256"])
        except jwt.PyJWTError:
            return None
