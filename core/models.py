from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
from django.utils import timezone
import secrets
import string


# =========================
# Utils
# =========================

def generate_school_token():
    return ''.join(
        secrets.choice(string.ascii_uppercase + string.digits)
        for _ in range(8)
    )


# =========================
# User Manager
# =========================

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário precisa ter um email")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'GESTOR')

        return self.create_user(email, password, **extra_fields)


# =========================
# User
# =========================

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('ALUNO', 'Aluno'),
        ('PROFESSOR', 'Professor'),
        ('GESTOR', 'Gestor'),
    )

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)  # nome completo
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='ALUNO')
    ativo = models.BooleanField(default=True)

    cpf = models.CharField(max_length=14, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    matricula = models.CharField(max_length=50, blank=True, null=True)

    # Campos obrigatórios pro Django Admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


# =========================
# School
# =========================

class School(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='managed_schools'
    )
    invite_token = models.CharField(
        max_length=8,
        unique=True,
        default=generate_school_token
    )
    token_uses_remaining = models.IntegerField(default=5)
    token_last_reset = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


# =========================
# TeacherSchoolLink
# =========================

class TeacherSchoolLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    date_linked = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='APPROVED')

    class Meta:
        unique_together = ('user', 'school')


# =========================
# Notification
# =========================

class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


# =========================
# Profiles
# =========================

class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)