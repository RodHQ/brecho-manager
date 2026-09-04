import datetime

from mongoengine import (
    NULLIFY,
    DateTimeField,
    Document,
    EmailField,
    ReferenceField,
    StringField,
)

from usuarios.models import Usuario


class Cliente(Document):
    """Cliente do brechó (MongoEngine Document).

    O campo ``usuario`` referencia o :class:`usuarios.models.Usuario`
    responsável pelo cadastro. MongoEngine não possui ``related_name``
    nativo; para consultar os clientes de um usuário use:
    ``Cliente.objects(usuario=usuario)``.
    """

    nome = StringField(max_length=150, required=True)
    email = EmailField()
    telefone = StringField(max_length=20)
    endereco = StringField(max_length=255)
    cidade = StringField(max_length=100)
    cep = StringField(max_length=10)
    cpf_cnpj = StringField(max_length=18, required=True, unique=True)
    data_cadastro = DateTimeField(default=datetime.datetime.utcnow)
    usuario = ReferenceField(Usuario, reverse_delete_rule=NULLIFY)

    meta = {"collection": "clientes"}

    def __str__(self):
        return self.nome
