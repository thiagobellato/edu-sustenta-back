from rest_framework import serializers
from .models import User, Aluno, Professor


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = [
            "id",
            "nome",
            "email",
            "cpf",
            "data_nascimento",
            "role",
            "is_active",
            "password",
            "password_confirm",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "As senhas não conferem"}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")

        user = User.objects.create_user(password=password, **validated_data)

        if user.role == "ALUNO":
            Aluno.objects.create(user=user)
        elif user.role == "PROFESSOR":
            Professor.objects.create(user=user)

        return user


class AlunoSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source="user.nome", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    cpf = serializers.CharField(source="user.cpf", read_only=True)
    data_nascimento = serializers.DateField(
        source="user.data_nascimento", read_only=True
    )
    is_active = serializers.BooleanField(source="user.is_active", read_only=True)

    class Meta:
        model = Aluno
        fields = [
            "id",
            "nome",
            "email",
            "cpf",
            "data_nascimento",
            "is_active",
        ]


class ProfessorSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source="user.nome", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    cpf = serializers.CharField(source="user.cpf", read_only=True)
    data_nascimento = serializers.DateField(
        source="user.data_nascimento", read_only=True
    )
    is_active = serializers.BooleanField(source="user.is_active", read_only=True)

    class Meta:
        model = Professor
        fields = [
            "id",
            "nome",
            "email",
            "cpf",
            "data_nascimento",
            "is_active",
        ]
