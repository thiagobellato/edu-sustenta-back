from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário precisa ter um email")
        email = self.normalize_email(email)
        role = extra_fields.get("role")

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
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    ativo = models.BooleanField(default=True)

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


class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="aluno")
    matricula = models.CharField(max_length=20, unique=True)


class Professor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="professor"
    )


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def criar_perfil_automatico(sender, instance, created, **kwargs):
    if created:
        if instance.role == "ALUNO":
            Aluno.objects.get_or_create(
                user=instance, defaults={"matricula": f"MAT-{instance.id}"}
            )
        elif instance.role == "PROFESSOR":
            Professor.objects.get_or_create(user=instance)
