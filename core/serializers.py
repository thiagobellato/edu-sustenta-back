from rest_framework import serializers
from .models import User, Aluno, Professor, Escola, Trilha


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "nome",
            "email",
            "role",
            "ativo",
        ]


class AlunoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Aluno
        fields = [
            "id",
            "user",
            "matricula",
            "ativo",
        ]


class ProfessorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Professor
        fields = [
            "id",
            "user",
            "matricula",
            "ativo",
        ]


class EscolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escola
        fields = [
            "id",
            "nome",
            "ativo",
        ]


class TrilhaSerializer(serializers.ModelSerializer):
    professor = ProfessorSerializer(read_only=True)
    alunos = AlunoSerializer(read_only=True, many=True)

    class Meta:
        model = Trilha
        fields = [
            "id",
            "nome",
            "nivel",
            "professor",
            "alunos",
            "ativo",
        ]
