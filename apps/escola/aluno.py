from django.db import models


class Aluno(models.Model):
    # Dados pessoais
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)  # formato XXX.XXX.XXX-XX
    senha = models.CharField(max_length=128)  # normalmente hashed
    data_nascimento = models.DateField()

    # Informações de login e função
    username = models.CharField(max_length=50, unique=True)
    ROLE_CHOICES = [
        ("aluno", "Aluno"),
        ("admin", "Admin"),
        ("professor", "Professor"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="aluno")

    # Controle
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.username})"

    # Métodos de ativação/desativação
    def desativar(self):
        self.ativo = False
        self.save()

    def ativar(self):
        self.ativo = True
        self.save()
