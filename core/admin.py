from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Aluno, Professor, School, TeacherSchoolLink


class CustomUserAdmin(UserAdmin):
    ordering = ('email',)
    model = User

    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('role', 'cpf', 'matricula', 'ativo')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': ('role', 'cpf', 'matricula', 'ativo')
        }),
    )

    list_display = (
        'email', 'first_name',
        'last_name', 'role', 'matricula', 'ativo'
    )

    list_filter = ('role', 'ativo', 'is_staff')
    search_fields = ('email', 'first_name', 'cpf', 'matricula')



class AlunoAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email')
    search_fields = ('user__username', 'user__email')

    @admin.display(description='Usuário', ordering='user__username')
    def get_username(self, obj):
        return obj.user.username

    @admin.display(description='Email', ordering='user__email')
    def get_email(self, obj):
        return obj.user.email


class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'get_email', 'get_matricula')
    search_fields = ('user__username', 'user__email')

    @admin.display(description='Nome', ordering='user__first_name')
    def get_name(self, obj):
        return obj.user.first_name

    @admin.display(description='Email', ordering='user__email')
    def get_email(self, obj):
        return obj.user.email

    @admin.display(description='Matrícula', ordering='user__matricula')
    def get_matricula(self, obj):
        return obj.user.matricula


class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'invite_token',
        'token_uses_remaining',
        'token_last_reset', 'active'
    )
    search_fields = ('name', 'invite_token')
    readonly_fields = ('invite_token',)


class TeacherSchoolLinkAdmin(admin.ModelAdmin):
    list_display = ('get_professor', 'get_school', 'status', 'date_linked')
    list_filter = ('status', 'school')

    @admin.display(description='Professor')
    def get_professor(self, obj):
        return obj.user.email

    @admin.display(description='Escola')
    def get_school(self, obj):
        return obj.school.name


admin.site.register(User, CustomUserAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(TeacherSchoolLink, TeacherSchoolLinkAdmin)
