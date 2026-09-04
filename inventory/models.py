from django.db import models

from suppliers.models import Supplier


class Product(models.Model):
    """Produto disponível no estoque do brechó."""

    nome = models.CharField("Nome", max_length=150)
    descricao = models.TextField("Descrição", blank=True)
    sku = models.CharField("SKU", max_length=50, unique=True)
    preco = models.DecimalField("Preço", max_digits=10, decimal_places=2)
    quantidade_estoque = models.PositiveIntegerField("Quantidade em estoque", default=0)
    data_criacao = models.DateTimeField("Data de criação", auto_now_add=True)
    fornecedor = models.ForeignKey(
        Supplier,
        verbose_name="Fornecedor",
        on_delete=models.SET_NULL,
        related_name="produtos",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.nome
