from django.contrib import admin
from .models import User, Aluno, Professor

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "role", "ativo")
    readonly_fields = ("nome", "data_nascimento")

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("id", "get_nome", "matricula")
    def get_nome(self, obj): return obj.user.nome

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("id", "get_nome", "get_cpf")
    readonly_fields = ("get_nome", "get_cpf", "get_data_nascimento")
    def get_nome(self, obj): return obj.user.nome
    def get_cpf(self, obj): return obj.user.cpf
    def get_data_nascimento(self, obj): return obj.user.data_nascimento