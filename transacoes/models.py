from datetime import datetime

import mongoengine as me


class Transacao(me.Document):
    """Registro de movimentação de estoque (entrada ou saída)."""

    TIPO_ENTRADA = "entrada"
    TIPO_SAIDA = "saida"
    TIPO_CHOICES = (
        (TIPO_ENTRADA, "Entrada"),
        (TIPO_SAIDA, "Saída"),
    )

    tipo = me.StringField(
        verbose_name="Tipo",
        max_length=10,
        choices=TIPO_CHOICES,
        required=True,
    )
    cliente = me.ReferenceField(
        "Cliente",
        verbose_name="Cliente",
        reverse_delete_rule=me.NULLIFY,
        null=True,
    )
    fornecedor = me.ReferenceField(
        "Fornecedor",
        verbose_name="Fornecedor",
        reverse_delete_rule=me.NULLIFY,
        null=True,
    )
    produto = me.ReferenceField(
        "Produto",
        verbose_name="Produto",
        reverse_delete_rule=me.DENY,
        required=True,
    )
    quantidade = me.IntField(verbose_name="Quantidade", required=True, min_value=1)
    valor = me.DecimalField(verbose_name="Valor", precision=2, force_string=True, required=True)
    data = me.DateTimeField(verbose_name="Data", default=datetime.utcnow)

    meta = {
        "collection": "transacoes",
        "ordering": ["-data"],
    }

    def get_tipo_display(self):
        return dict(self.TIPO_CHOICES).get(self.tipo, self.tipo)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto} ({self.quantidade})"
