from django.contrib import admin
from .models import User, Aluno, Professor


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "role", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("nome", "email", "cpf")
    readonly_fields = ("id",)
    ordering = ("id",)


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("id", "get_nome", "get_email", "get_is_active")
    readonly_fields = (
        "get_nome",
        "get_email",
        "get_cpf",
        "get_data_nascimento",
        "get_is_active",
    )

    def get_nome(self, obj):
        return obj.user.nome

    def get_email(self, obj):
        return obj.user.email

    def get_cpf(self, obj):
        return obj.user.cpf

    def get_data_nascimento(self, obj):
        return obj.user.data_nascimento

    def get_is_active(self, obj):
        return obj.user.is_active

    get_nome.short_description = "Nome"
    get_email.short_description = "E-mail"
    get_cpf.short_description = "CPF"
    get_data_nascimento.short_description = "Data de Nascimento"
    get_is_active.short_description = "Ativo"


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("id", "get_nome", "get_email", "get_cpf", "get_is_active")
    readonly_fields = (
        "get_nome",
        "get_email",
        "get_cpf",
        "get_data_nascimento",
        "get_is_active",
    )

    def get_nome(self, obj):
        return obj.user.nome

    def get_email(self, obj):
        return obj.user.email

    def get_cpf(self, obj):
        return obj.user.cpf

    def get_data_nascimento(self, obj):
        return obj.user.data_nascimento

    def get_is_active(self, obj):
        return obj.user.is_active

    get_nome.short_description = "Nome"
    get_email.short_description = "E-mail"
    get_cpf.short_description = "CPF"
    get_data_nascimento.short_description = "Data de Nascimento"
    get_is_active.short_description = "Ativo"
