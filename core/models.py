from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import secrets
import string

# Função auxiliar para gerar token ABC12345
def generate_school_token():
    letters = ''.join(secrets.choice(string.ascii_uppercase) for i in range(3))
    numbers = ''.join(secrets.choice(string.digits) for i in range(5))
    return f"{letters}{numbers}"

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ALUNO', 'Aluno'),
        ('PROFESSOR', 'Professor'),
        ('GESTOR', 'Gestor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='ALUNO')
    ativo = models.BooleanField(default=True)
    # Campos antigos de CPF podem ser removidos ou mantidos como opcionais
    cpf = models.CharField(max_length=14, blank=True, null=True)
    data_nascimento = models.DateField(null=True, blank=True)
    matricula = models.CharField(max_length=50, blank=True, null=True)

class School(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    
    # --- NOVOS CAMPOS DO SISTEMA DE TOKEN ---
    invite_token = models.CharField(max_length=8, unique=True, default=generate_school_token)
    token_uses_remaining = models.IntegerField(default=5)
    token_last_reset = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class TeacherSchoolLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='school_links')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teacher_links')
    date_linked = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='APPROVED') # Já nasce aprovado pelo token

    class Meta:
        unique_together = ('user', 'school')

# ... (Seus modelos de Aluno/Professor herdam de User ou tem OneToOne, mantenha-os aqui)
class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='aluno_profile')
    # ... outros campos

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professor_profile')
    # ... outros campos