from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Aluno, Professor

# Configuração do Usuário
# Usamos UserAdmin para garantir que a senha seja tratada corretamente
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Adicionamos os novos campos CPF e Nascimento na visualização
    fieldsets = UserAdmin.fieldsets + (
        ('Dados Pessoais', {'fields': ('cpf', 'data_nascimento', 'role', 'ativo')}),
    )
    
    list_display = ("id", "nome", "email", "role", "ativo", "is_staff")
    search_fields = ("nome", "email", "cpf")
    list_filter = ("role", "ativo", "is_staff")
    ordering = ("id",)


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    # 'get_nome' e 'get_email' são funções criadas lá embaixo para pegar dados do User
    list_display = ("id", "get_nome", "get_email", "matricula", "get_ativo")
    
    # Para busca e filtro, usamos __ para navegar até o user
    search_fields = ("user__nome", "user__email", "matricula")
    list_filter = ("user__ativo",)
    ordering = ("id",)

    # --- Funções auxiliares para mostrar dados do User ---
    @admin.display(ordering='user__nome', description='Nome')
    def get_nome(self, obj):
        return obj.user.nome

    @admin.display(ordering='user__email', description='Email')
    def get_email(self, obj):
        return obj.user.email

    @admin.display(ordering='user__ativo', description='Ativo', boolean=True)
    def get_ativo(self, obj):
        return obj.user.ativo


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("id", "get_nome", "get_email", "matricula", "get_ativo")
    search_fields = ("user__nome", "user__email", "matricula")
    list_filter = ("user__ativo",)
    ordering = ("id",)

    # --- Funções auxiliares para mostrar dados do User ---
    @admin.display(ordering='user__nome', description='Nome')
    def get_nome(self, obj):
        return obj.user.nome

    @admin.display(ordering='user__email', description='Email')
    def get_email(self, obj):
        return obj.user.email

    @admin.display(ordering='user__ativo', description='Ativo', boolean=True)
    def get_ativo(self, obj):
        return obj.user.ativo