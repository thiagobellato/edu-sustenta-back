from django.contrib import admin
from .models import User, Aluno, Professor


# ==========================
# USER
# ==========================
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "role", "ativo", "is_staff")
    search_fields = ("nome", "email")
    list_filter = ("role", "ativo", "is_staff")
    ordering = ("id",)


# ==========================
# ALUNO
# ==========================
@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "matricula", "ativo")
    search_fields = ("user__nome", "user__email", "matricula")
    list_filter = ("user__ativo",)
    ordering = ("id",)

    def nome(self, obj):
        return obj.user.nome

    def email(self, obj):
        return obj.user.email

    def ativo(self, obj):
        return obj.user.ativo

    nome.short_description = "Nome"
    email.short_description = "Email"
    ativo.short_description = "Ativo"


# ==========================
# PROFESSOR
# ==========================
@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "matricula", "ativo")
    search_fields = ("user__nome", "user__email", "matricula")
    list_filter = ("user__ativo",)
    ordering = ("id",)

    def nome(self, obj):
        return obj.user.nome

    def email(self, obj):
        return obj.user.email

    def ativo(self, obj):
        return obj.user.ativo

    nome.short_description = "Nome"
    email.short_description = "Email"
    ativo.short_description = "Ativo"
