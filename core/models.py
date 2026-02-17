from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
import secrets
import string

# ==================================================
# Utils
# ==================================================
def generate_school_token():
    letters = ''.join(secrets.choice(string.ascii_uppercase) for i in range(3))
    numbers = ''.join(secrets.choice(string.digits) for i in range(5))
    return f"{letters}{numbers}"

# ==================================================
# Custom User Manager
# ==================================================
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, password=None, **extra_fields):
        """
        Cria um usuário normal. Solicita email, nome e senha.
        """
        if not email:
            raise ValueError("O usuário precisa de um email")
        if not first_name:
            raise ValueError("O usuário precisa de um primeiro nome")

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password=None, **extra_fields):
        """
        Cria um superuser com todas permissões e role 'GESTOR'.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "GESTOR")

        return self.create_user(email, first_name, password, **extra_fields)

# ==================================================
# User
# ==================================================
class User(AbstractUser):
    ROLE_CHOICES = (
        ('USER', 'Usuário'),
        ('ALUNO', 'Aluno'),
        ('PROFESSOR', 'Professor'),
        ('GESTOR', 'Gestor'),
    )

    # Remove username
    username = None

    # Usa email como login
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']  # <-- Pede o nome no createsuperuser

    objects = UserManager()  # <-- Importante!

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')
    ativo = models.BooleanField(default=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    data_nascimento = models.DateField(null=True, blank=True)
    matricula = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.email

# ==================================================
# School
# ==================================================
class School(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    
    manager = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='managed_schools', 
        null=True, 
        blank=True
    )
    
    invite_token = models.CharField(max_length=8, unique=True, default=generate_school_token)
    token_uses_remaining = models.IntegerField(default=5)
    token_last_reset = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

# ==================================================
# Teacher x School
# ==================================================
class TeacherSchoolLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='school_links')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teacher_links')
    date_linked = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='APPROVED')

    class Meta:
        unique_together = ('user', 'school')

# ==================================================
# Notification
# ==================================================
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"

# ==================================================
# Profiles
# ==================================================
class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='aluno_profile')

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professor_profile')

# ==================================================
# Trail & Module
# ==================================================
class Trail(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
        ('archived', 'Desativada'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_trails')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Campos opcionais para compatibilidade com frontend
    category = models.CharField(max_length=100, blank=True, null=True)
    difficulty = models.CharField(max_length=50, blank=True, null=True)
    cover_image = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Module(models.Model):
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        unique_together = ('trail', 'order')
    
    def __str__(self):
        return f"{self.trail.title} - {self.title}"