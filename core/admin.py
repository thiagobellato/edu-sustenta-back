from django.contrib import admin
from .models import (
    User,
    Aluno,
    Professor,
    Escola,
    Trilha,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "role", "ativo", "is_staff")
    search_fields = ("nome", "email")
    list_filter = ("role", "ativo", "is_staff")
    ordering = ("id",)


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "matricula", "ativo")
    search_fields = ("user__nome", "user__email", "matricula")
    list_filter = ("ativo",)
    ordering = ("id",)

    def nome(self, obj):
        return obj.user.nome

    def email(self, obj):
        return obj.user.email

    nome.short_description = "Nome"
    email.short_description = "Email"


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "matricula", "ativo")
    search_fields = ("user__nome", "user__email", "matricula")
    list_filter = ("ativo",)
    ordering = ("id",)

    def nome(self, obj):
        return obj.user.nome

    def email(self, obj):
        return obj.user.email

    nome.short_description = "Nome"
    email.short_description = "Email"


@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "ativo")
    search_fields = ("nome",)
    list_filter = ("ativo",)
    ordering = ("id",)


@admin.register(Trilha)
class TrilhaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "nivel", "professor", "ativo")
    search_fields = ("nome", "nivel", "professor__user__nome")
    list_filter = ("nivel", "ativo")
    filter_horizontal = ("alunos",)
    ordering = ("id",)
