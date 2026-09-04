from django.contrib import admin

from .models import Transacao


@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ("tipo", "produto", "cliente", "fornecedor", "quantidade", "valor", "data")
    list_filter = ("tipo",)
    search_fields = ("produto__nome", "cliente__nome", "fornecedor__nome")
