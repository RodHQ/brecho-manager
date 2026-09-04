from django.db import models

from clients.models import Client
from inventory.models import Product
from suppliers.models import Supplier


class Transaction(models.Model):
    """Registro de movimentação de estoque (entrada ou saída)."""

    TIPO_ENTRADA = "entrada"
    TIPO_SAIDA = "saida"
    TIPO_CHOICES = [
        (TIPO_ENTRADA, "Entrada"),
        (TIPO_SAIDA, "Saída"),
    ]

    tipo = models.CharField("Tipo", max_length=10, choices=TIPO_CHOICES)
    cliente = models.ForeignKey(
        Client,
        verbose_name="Cliente",
        on_delete=models.SET_NULL,
        related_name="transacoes",
        null=True,
        blank=True,
    )
    fornecedor = models.ForeignKey(
        Supplier,
        verbose_name="Fornecedor",
        on_delete=models.SET_NULL,
        related_name="transacoes",
        null=True,
        blank=True,
    )
    produto = models.ForeignKey(
        Product,
        verbose_name="Produto",
        on_delete=models.PROTECT,
        related_name="transacoes",
    )
    quantidade = models.PositiveIntegerField("Quantidade")
    valor = models.DecimalField("Valor", max_digits=10, decimal_places=2)
    data = models.DateTimeField("Data", auto_now_add=True)

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto} ({self.quantidade})"
