import datetime

from mongoengine import (
    NULLIFY,
    DateTimeField,
    DecimalField,
    Document,
    IntField,
    ReferenceField,
    StringField,
)

from fornecedores.models import Fornecedor


class Produto(Document):
    """Produto disponível no estoque do brechó (MongoEngine Document).

    O campo ``fornecedor`` referencia o :class:`fornecedores.models.Fornecedor`.
    Para consultar os produtos de um fornecedor use:
    ``Produto.objects(fornecedor=fornecedor)``.
    """

    nome = StringField(max_length=150, required=True)
    descricao = StringField()
    sku = StringField(max_length=50, required=True, unique=True)
    preco = DecimalField(precision=2, required=True)
    quantidade = IntField(default=0, min_value=0)
    data_criacao = DateTimeField(default=datetime.datetime.utcnow)
    fornecedor = ReferenceField(Fornecedor, reverse_delete_rule=NULLIFY)

    meta = {"collection": "estoque"}

    def __str__(self):
        return self.nome
