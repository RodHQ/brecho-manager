from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("tipo", "produto", "cliente", "fornecedor", "quantidade", "valor", "data")
    list_filter = ("tipo",)
    search_fields = ("produto__nome", "cliente__nome", "fornecedor__nome")
