from datetime import datetime

import mongoengine as me


class Produto(me.Document):
    """Produto disponível no estoque do brechó."""

    nome = me.StringField(verbose_name="Nome", max_length=150, required=True)
    descricao = me.StringField(verbose_name="Descrição", default="")
    sku = me.StringField(verbose_name="SKU", max_length=50, required=True, unique=True)
    preco = me.DecimalField(verbose_name="Preço", precision=2, force_string=True, required=True)
    quantidade = me.IntField(verbose_name="Quantidade em estoque", default=0, min_value=0)
    data_criacao = me.DateTimeField(verbose_name="Data de criação", default=datetime.utcnow)
    fornecedor = me.ReferenceField(
        "Fornecedor",
        verbose_name="Fornecedor",
        reverse_delete_rule=me.NULLIFY,
        null=True,
    )

    meta = {
        "collection": "produtos",
        "ordering": ["nome"],
    }

    def __str__(self):
        return self.nome
