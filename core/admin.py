from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Aluno, Professor, School, TeacherSchoolLink


# =========================
# User
# =========================

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    model = User

    ordering = ("email",)
    search_fields = ("email", "cpf", "matricula")

    list_display = ("email", "role", "matricula", "ativo", "is_staff")
    list_filter = ("role", "ativo", "is_staff")

    fieldsets = (
        ("Credenciais", {"fields": ("email", "password")}),
        ("Perfil", {"fields": ("role", "cpf", "matricula", "data_nascimento", "ativo")}),
        ("Permissões", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role"),
        }),
    )

    filter_horizontal = ("groups", "user_permissions")


# =========================
# Aluno
# =========================

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("get_email", "get_cpf")
    search_fields = ("user__email", "user__cpf")

    @admin.display(description="Email", ordering="user__email")
    def get_email(self, obj):
        return obj.user.email

    @admin.display(description="CPF", ordering="user__cpf")
    def get_cpf(self, obj):
        return obj.user.cpf


# =========================
# Professor
# =========================

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("get_email", "get_matricula")
    search_fields = ("user__email", "user__matricula")

    @admin.display(description="Email", ordering="user__email")
    def get_email(self, obj):
        return obj.user.email

    @admin.display(description="Matrícula", ordering="user__matricula")
    def get_matricula(self, obj):
        return obj.user.matricula


# =========================
# School
# =========================

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        "name", "invite_token",
        "token_uses_remaining",
        "token_last_reset", "active"
    )
    search_fields = ("name", "invite_token")
    readonly_fields = ("invite_token",)


# =========================
# TeacherSchoolLink
# =========================

@admin.register(TeacherSchoolLink)
class TeacherSchoolLinkAdmin(admin.ModelAdmin):
    list_display = ("get_professor", "get_school", "status", "date_linked")
    list_filter = ("status", "school")

    @admin.display(description="Professor")
    def get_professor(self, obj):
        return obj.user.email

    @admin.display(description="Escola")
    def get_school(self, obj):
        return obj.school.name