from django.conf import settings
from django.db import models


class Client(models.Model):
    """Cliente do brechó."""

    nome = models.CharField("Nome", max_length=150)
    email = models.EmailField("Email", blank=True)
    telefone = models.CharField("Telefone", max_length=20, blank=True)
    endereco = models.CharField("Endereço", max_length=255, blank=True)
    cidade = models.CharField("Cidade", max_length=100, blank=True)
    cep = models.CharField("CEP", max_length=10, blank=True)
    cpf_cnpj = models.CharField("CPF/CNPJ", max_length=18, unique=True)
    data_cadastro = models.DateTimeField("Data de cadastro", auto_now_add=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Usuário responsável",
        on_delete=models.SET_NULL,
        related_name="clientes",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nome
