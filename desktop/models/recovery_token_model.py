"""Modelo (documento) de token de recuperação de senha."""
import datetime
import secrets


def gerar_token():
    """Gera um token de recuperação único e seguro."""
    return secrets.token_urlsafe(32)


def novo_recovery_token_documento(usuario_id, expiry_seconds):
    """Monta o documento de um novo token de recuperação pronto para inserção."""
    agora = datetime.datetime.utcnow()
    return {
        "usuario_id": usuario_id,
        "token": gerar_token(),
        "criado_em": agora,
        "expira_em": agora + datetime.timedelta(seconds=expiry_seconds),
        "usado": False,
    }


class RecoveryToken:
    """Representação em memória de um documento da collection ``recovery_tokens``."""

    def __init__(self, doc):
        doc = doc or {}
        self.id = doc.get("_id")
        self.usuario_id = doc.get("usuario_id")
        self.token = doc.get("token")
        self.criado_em = doc.get("criado_em")
        self.expira_em = doc.get("expira_em")
        self.usado = doc.get("usado", False)

    def is_valido(self):
        if self.usado:
            return False
        if self.expira_em is None:
            return False
        return datetime.datetime.utcnow() < self.expira_em
