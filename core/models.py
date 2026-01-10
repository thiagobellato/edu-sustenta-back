from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# ==========================
# USER MANAGER
# ==========================
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário precisa ter um email")

        email = self.normalize_email(email)
        role = extra_fields.get("role")

        # REGRA DE NEGÓCIO: apenas GESTOR é admin
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


# ==========================
# USER (BASE ÚNICA)
# ==========================
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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome", "role"]

    objects = UserManager()

    def save(self, *args, **kwargs):
        """
        Garante consistência de permissões,
        mesmo se alguém tentar alterar via Admin.
        """
        if self.role == "GESTOR":
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


# ==========================
# ALUNO (PERFIL DO USUÁRIO)
# ==========================
class Aluno(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="aluno",
        limit_choices_to={"role": "ALUNO"},
    )
    matricula = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"Aluno: {self.user.nome}"


# ==========================
# PROFESSOR (PERFIL DO USUÁRIO)
# ==========================
class Professor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="professor",
        limit_choices_to={"role": "PROFESSOR"},
    )
    matricula = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"Professor: {self.user.nome}"
