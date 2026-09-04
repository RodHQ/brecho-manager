"""Modelo (documento) de Usuario para uso direto com PyMongo na app desktop."""
import datetime


def novo_usuario_documento(username, email, hashed_password, nome="", telefone=""):
    """Monta o documento de um novo usuário pronto para inserção no MongoDB."""
    return {
        "username": username,
        "email": email,
        "password": hashed_password,
        "nome": nome,
        "telefone": telefone,
        "data_criacao": datetime.datetime.utcnow(),
        "ativo": True,
    }


class Usuario:
    """Representação em memória de um documento da collection ``usuarios``."""

    def __init__(self, doc):
        doc = doc or {}
        self.id = doc.get("_id")
        self.username = doc.get("username")
        self.email = doc.get("email")
        self.password = doc.get("password")
        self.nome = doc.get("nome")
        self.telefone = doc.get("telefone")
        self.data_criacao = doc.get("data_criacao")
        self.ativo = doc.get("ativo", True)

    @property
    def nome_exibicao(self):
        return self.nome or self.username

    def to_dict(self):
        return {
            "_id": self.id,
            "username": self.username,
            "email": self.email,
            "nome": self.nome,
            "telefone": self.telefone,
            "data_criacao": self.data_criacao,
            "ativo": self.ativo,
        }
