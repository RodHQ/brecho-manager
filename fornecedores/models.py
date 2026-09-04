import datetime

from mongoengine import BooleanField, DateTimeField, Document, EmailField, StringField


class Fornecedor(Document):
    """Fornecedor de produtos para o brechó (MongoEngine Document)."""

    nome = StringField(max_length=150, required=True)
    email = EmailField()
    telefone = StringField(max_length=20)
    endereco = StringField(max_length=255)
    cnpj = StringField(max_length=18, required=True, unique=True)
    contato = StringField(max_length=150)
    ativo = BooleanField(default=True)
    data_cadastro = DateTimeField(default=datetime.datetime.utcnow)

    meta = {"collection": "fornecedores"}

    def __str__(self):
        return self.nome
