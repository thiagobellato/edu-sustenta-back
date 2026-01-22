from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Aluno, Professor, School, TeacherSchoolLink

# ==================================================
# 1. Configuração do Usuário (CustomUser)
# ==================================================
class CustomUserAdmin(UserAdmin):
    model = User
    
    # Adiciona os campos novos na tela de edição do admin
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('role', 'cpf', 'matricula', 'ativo')}),
    )
    
    # Adiciona os campos novos na tela de criação
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('role', 'cpf', 'matricula', 'ativo')}),
    )

    # Colunas da tabela de listagem
    # CORREÇÃO: 'nome' não existe no User padrão, usa-se 'first_name'.
    # CORREÇÃO: 'matricula' agora existe no User, então pode ficar aqui.
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'matricula', 'ativo')
    
    # Filtros laterais
    list_filter = ('role', 'ativo', 'is_staff')
    
    # Campos de busca
    search_fields = ('username', 'email', 'first_name', 'cpf', 'matricula')

# ==================================================
# 2. Configuração de Aluno e Professor (Perfis)
# ==================================================
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email')
    search_fields = ('user__username', 'user__email')

    # Como Aluno agora é só um link para User, acessamos os dados via 'obj.user'
    @admin.display(description='Usuário', ordering='user__username')
    def get_username(self, obj):
        return obj.user.username

    @admin.display(description='Email', ordering='user__email')
    def get_email(self, obj):
        return obj.user.email

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'get_matricula')
    search_fields = ('user__username', 'user__email')

    @admin.display(description='Nome', ordering='user__first_name')
    def get_username(self, obj):
        return obj.user.first_name

    @admin.display(description='Email', ordering='user__email')
    def get_email(self, obj):
        return obj.user.email

    @admin.display(description='Matrícula', ordering='user__matricula')
    def get_matricula(self, obj):
        return obj.user.matricula

# ==================================================
# 3. Configuração de Escolas e Vínculos (Novo)
# ==================================================
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'invite_token', 'token_uses_remaining', 'token_last_reset', 'active')
    search_fields = ('name', 'invite_token')
    readonly_fields = ('invite_token',) # Token é gerado automático, melhor não editar na mão

class TeacherSchoolLinkAdmin(admin.ModelAdmin):
    list_display = ('get_professor', 'get_school', 'status', 'date_linked')
    list_filter = ('status', 'school')
    
    @admin.display(description='Professor')
    def get_professor(self, obj):
        return obj.user.email

    @admin.display(description='Escola')
    def get_school(self, obj):
        return obj.school.name

# ==================================================
# REGISTRO DOS MODELOS
# ==================================================
admin.site.register(User, CustomUserAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(TeacherSchoolLink, TeacherSchoolLinkAdmin)