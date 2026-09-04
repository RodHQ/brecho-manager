from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "nome", "email", "telefone", "ativo", "data_criacao")
    list_filter = ("ativo", "is_staff", "is_superuser")
    search_fields = ("username", "nome", "email", "telefone")
    fieldsets = UserAdmin.fieldsets + (
        ("Informações adicionais", {"fields": ("nome", "telefone", "ativo")}),
    )
