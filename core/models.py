from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário precisa ter um email")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("ativo", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser precisa ter is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser precisa ter is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = (
        ("ALUNO", "Aluno"),
        ("PROFESSOR", "Professor"),
        ("GESTOR", "Gestor"),
    )

    username = None  # remove username
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    ativo = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome", "role"]

    objects = UserManager()

    def __str__(self):
        return self.nome


class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=20, unique=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"Aluno: {self.user.nome}"


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=20, unique=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"Professor: {self.user.nome}"


class Trilha(models.Model):
    nome = models.CharField(max_length=100)
    nivel = models.CharField(max_length=50)

    professor = models.ForeignKey(
        Professor, on_delete=models.CASCADE, related_name="trilhas_criadas"
    )

    alunos = models.ManyToManyField(Aluno, related_name="trilhas")
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Escola(models.Model):
    nome = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
