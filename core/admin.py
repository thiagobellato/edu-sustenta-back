from django.contrib import admin
from .models import User, Aluno, Professor


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "role", "ativo", "is_staff")
    search_fields = ("nome", "email")
    list_filter = ("role", "ativo", "is_staff")
    ordering = ("id",)


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "matricula", "ativo")
    search_fields = ("nome", "email", "matricula")
    list_filter = ("ativo",)
    ordering = ("id",)


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "matricula", "ativo")
    search_fields = ("nome", "email", "matricula")
    list_filter = ("ativo",)
    ordering = ("id",)


# ==========================
# MODELS FUTUROS (PAUSADOS)
# ==========================

# from .models import Escola, Trilha

# @admin.register(Escola)
# class EscolaAdmin(admin.ModelAdmin):
#     list_display = ("id", "nome", "ativo")
#     search_fields = ("nome",)
#     list_filter = ("ativo",)
#     ordering = ("id",)


# @admin.register(Trilha)
# class TrilhaAdmin(admin.ModelAdmin):
#     list_display = ("id", "nome", "nivel", "ativo")
#     search_fields = ("nome", "nivel")
#     list_filter = ("nivel", "ativo")
#     ordering = ("id",)
