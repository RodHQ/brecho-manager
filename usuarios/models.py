import datetime

from django.contrib.auth.hashers import check_password, make_password
from mongoengine import BooleanField, DateTimeField, Document, EmailField, StringField


class Usuario(Document):
    """Usuário do sistema (MongoEngine Document)."""

    username = StringField(max_length=150, required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)  # armazenado como hash
    nome = StringField(max_length=150)
    telefone = StringField(max_length=20)
    data_criacao = DateTimeField(default=datetime.datetime.utcnow)
    ativo = BooleanField(default=True)

    meta = {"collection": "usuarios"}

    def set_password(self, raw_password):
        """Gera e armazena o hash da senha informada."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Verifica se a senha informada corresponde ao hash armazenado."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.nome or self.username
