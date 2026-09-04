from django.contrib import admin

from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "cpf_cnpj", "email", "telefone", "cidade", "usuario", "data_cadastro")
    list_filter = ("cidade",)
    search_fields = ("nome", "cpf_cnpj", "email", "telefone")
