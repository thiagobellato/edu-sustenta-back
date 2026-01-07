from django.contrib import admin
from .models import Aluno, Professor


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "ativo")
    search_fields = ("nome", "email")
    list_filter = ("ativo",)


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "matricula", "ativo")
    search_fields = ("nome", "email", "matricula")
    list_filter = ("ativo",)
