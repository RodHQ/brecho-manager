from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """Usuário customizado do sistema, baseado em AbstractUser."""

    nome = models.CharField("Nome", max_length=150, blank=True)
    telefone = models.CharField("Telefone", max_length=20, blank=True)
    data_criacao = models.DateTimeField("Data de criação", auto_now_add=True)
    ativo = models.BooleanField("Ativo", default=True)

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.nome or self.username
