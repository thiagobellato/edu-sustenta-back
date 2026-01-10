from rest_framework import serializers
from .models import User, Aluno, Professor


# ==========================
# USER
# ==========================
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
        role = validated_data.get("role")

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        # CRIA PERFIL ESPECÍFICO AUTOMATICAMENTE
        if role == "ALUNO":
            Aluno.objects.create(
                user=user,
                matricula=f"ALU-{user.id}"
            )

        elif role == "PROFESSOR":
            Professor.objects.create(
                user=user,
                matricula=f"PROF-{user.id}"
            )

        return user


# ==========================
# ALUNO (SOMENTE LEITURA)
# ==========================
class AlunoSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source="user.nome", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    ativo = serializers.BooleanField(source="user.ativo", read_only=True)

    class Meta:
        model = Aluno
        fields = [
            "id",
            "nome",
            "email",
            "matricula",
            "ativo",
        ]
        read_only_fields = fields


# ==========================
# PROFESSOR (SOMENTE LEITURA)
# ==========================
class ProfessorSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source="user.nome", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    ativo = serializers.BooleanField(source="user.ativo", read_only=True)

    class Meta:
        model = Professor
        fields = [
            "id",
            "nome",
            "email",
            "matricula",
            "ativo",
        ]
        read_only_fields = fields
