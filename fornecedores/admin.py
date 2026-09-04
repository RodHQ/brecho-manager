from django.contrib import admin

from .models import Fornecedor


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ("nome", "cnpj", "email", "telefone", "contato", "ativo", "data_cadastro")
    list_filter = ("ativo",)
    search_fields = ("nome", "cnpj", "email", "contato")
