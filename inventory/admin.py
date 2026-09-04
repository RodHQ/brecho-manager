from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("nome", "sku", "preco", "quantidade_estoque", "fornecedor", "data_criacao")
    list_filter = ("fornecedor",)
    search_fields = ("nome", "sku")
