from django.contrib import admin

from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("nome", "cnpj", "email", "telefone", "contato", "ativo", "data_cadastro")
    list_filter = ("ativo",)
    search_fields = ("nome", "cnpj", "email", "contato")
