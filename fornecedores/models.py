from django.db import models


class Fornecedor(models.Model):
    """Fornecedor de produtos para o brechó."""

    nome = models.CharField("Nome", max_length=150)
    email = models.EmailField("Email", blank=True)
    telefone = models.CharField("Telefone", max_length=20, blank=True)
    endereco = models.CharField("Endereço", max_length=255, blank=True)
    cnpj = models.CharField("CNPJ", max_length=18, unique=True)
    contato = models.CharField("Contato", max_length=150, blank=True)
    ativo = models.BooleanField("Ativo", default=True)
    data_cadastro = models.DateTimeField("Data de cadastro", auto_now_add=True)

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"

    def __str__(self):
        return self.nome
