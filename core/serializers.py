from rest_framework import serializers
from .models import User, Aluno, Professor


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=6
    )

    class Meta:
        model = User
        fields = [
            "id",
            "nome",
            "email",
            "password",
            "role",
            "ativo",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user


class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = [
            "id",
            "nome",
            "email",
            "matricula",
            "ativo",
        ]


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = [
            "id",
            "nome",
            "email",
            "matricula",
            "ativo",
        ]


# ==========================
# FUTUROS SERIALIZERS (PAUSADOS)
# ==========================

# from .models import Escola, Trilha

# class EscolaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Escola
#         fields = [
#             "id",
#             "nome",
#             "ativo",
#         ]


# class TrilhaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Trilha
#         fields = [
#             "id",
#             "nome",
#             "nivel",
#             "ativo",
#         ]
