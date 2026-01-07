from django.db import models


class Professor(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Aluno(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    matricula = models.CharField(max_length=50, unique=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
