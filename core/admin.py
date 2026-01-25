from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Aluno, Professor, School, TeacherSchoolLink

# ==================================================
# 1. Configuração do Usuário (CustomUser)
# ==================================================
class CustomUserAdmin(UserAdmin):
    model = User

    # Remove qualquer referência a username
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Informações Adicionais', {'fields': ('role', 'cpf', 'matricula', 'ativo')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'cpf', 'matricula', 'ativo'),
        }),
    )

    list_display = ('email', 'first_name', 'last_name', 'role', 'matricula', 'ativo', 'is_staff')
    list_filter = ('role', 'ativo', 'is_staff')
    search_fields = ('email', 'first_name', 'cpf', 'matricula')
    filter_horizontal = ('groups', 'user_permissions')


# ==================================================
# 2. Configuração de Aluno
# ==================================================
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'get_nome')
    search_fields = ('user__email', 'user__first_name')

    @admin.display(description='Email', ordering='user__email')
    def get_email(self, obj):
        return obj.user.email

    @admin.display(description='Nome', ordering='user__first_name')
    def get_nome(self, obj):
        return obj.user.first_name


# ==================================================
# 3. Configuração de Professor
# ==================================================
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'get_nome', 'get_matricula')
    search_fields = ('user__email', 'user__first_name', 'user__matricula')

    @admin.display(description='Email', ordering='user__email')
    def get_email(self, obj):
        return obj.user.email

    @admin.display(description='Nome', ordering='user__first_name')
    def get_nome(self, obj):
        return obj.user.first_name

    @admin.display(description='Matrícula', ordering='user__matricula')
    def get_matricula(self, obj):
        return obj.user.matricula


# ==================================================
# 4. Configuração de Escolas
# ==================================================
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'invite_token', 'token_uses_remaining', 'token_last_reset', 'active')
    search_fields = ('name', 'invite_token')
    readonly_fields = ('invite_token',)


# ==================================================
# 5. Configuração de Vínculo Professor-Escola
# ==================================================
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