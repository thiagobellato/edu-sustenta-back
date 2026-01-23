from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import secrets
import string


def generate_school_token():
    letters = ''.join(secrets.choice(string.ascii_uppercase) for _ in range(3))
    numbers = ''.join(secrets.choice(string.digits) for _ in range(5))
    return f"{letters}{numbers}"


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ALUNO', 'Aluno'),
        ('PROFESSOR', 'Professor'),
        ('GESTOR', 'Gestor'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='ALUNO')
    ativo = models.BooleanField(default=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    matricula = models.CharField(max_length=50, blank=True, null=True)


class School(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='managed_schools',
        blank=True,
        null=True
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


class TeacherSchoolLink(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='school_links'
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='teacher_links'
    )
    date_linked = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='APPROVED')

    class Meta:
        unique_together = ('user', 'school')


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

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Aluno(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='aluno_profile'
    )


class Professor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='professor_profile'
    )
