from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário precisa ter um email")

        email = self.normalize_email(email)
        role = extra_fields.get("role")

        # REGRA DE NEGÓCIO
        if role == "GESTOR":
            extra_fields.setdefault("is_staff", True)
            extra_fields.setdefault("is_superuser", True)
        else:
            extra_fields.setdefault("is_staff", False)
            extra_fields.setdefault("is_superuser", False)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", "GESTOR")
        extra_fields.setdefault("ativo", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = (
        ("ALUNO", "Aluno"),
        ("PROFESSOR", "Professor"),
        ("GESTOR", "Gestor"),
    )

    username = None
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    ativo = models.BooleanField(default=True)

    # --- NOVOS CAMPOS PARA O FORMULÁRIO ---
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    # --------------------------------------

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome", "role"]

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.role == "GESTOR":
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Aluno(models.Model):
    # Vincula ao usuário de login (substitui nome/email duplicados)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='aluno_profile')
    matricula = models.CharField(max_length=20, unique=True)
    
    # Ativo já existe no user, mas se precisar de controle específico do aluno:
    # ativo = models.BooleanField(default=True) 

    def __str__(self):
        return f"{self.user.nome} - {self.matricula}"


class Professor(models.Model):
    # Vincula ao usuário de login
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professor_profile')
    matricula = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    # --- NOVO CAMPO DE ARQUIVO ---
    # Requer que você configure MEDIA_URL e MEDIA_ROOT no settings.py
    comprovante_vinculo = models.FileField(upload_to='comprovantes/', null=True, blank=True)
    # -----------------------------

    def __str__(self):
        return f"{self.user.nome} - Professor"