import datetime

from mongoengine import (
    DENY,
    NULLIFY,
    DateTimeField,
    DecimalField,
    Document,
    IntField,
    ReferenceField,
    StringField,
)

from clientes.models import Cliente
from estoque.models import Produto
from fornecedores.models import Fornecedor


class Transacao(Document):
    """Registro de movimentação de estoque (entrada ou saída).

    MongoEngine Document com referências para Cliente, Fornecedor e Produto.
    """

    TIPO_ENTRADA = "entrada"
    TIPO_SAIDA = "saida"
    TIPO_CHOICES = (
        (TIPO_ENTRADA, "Entrada"),
        (TIPO_SAIDA, "Saída"),
    )

    tipo = StringField(max_length=10, required=True, choices=TIPO_CHOICES)
    cliente = ReferenceField(Cliente, reverse_delete_rule=NULLIFY)
    fornecedor = ReferenceField(Fornecedor, reverse_delete_rule=NULLIFY)
    produto = ReferenceField(Produto, required=True, reverse_delete_rule=DENY)
    quantidade = IntField(required=True, min_value=0)
    valor = DecimalField(precision=2, required=True)
    data = DateTimeField(default=datetime.datetime.utcnow)

    meta = {"collection": "transacoes"}

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto} ({self.quantidade})"
