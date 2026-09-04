from django.contrib import admin

from .models import Produto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "sku", "preco", "quantidade", "fornecedor", "data_criacao")
    list_filter = ("fornecedor",)
    search_fields = ("nome", "sku")
