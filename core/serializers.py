from rest_framework import serializers
from .models import User, Aluno, Professor

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    class Meta:
        model = User
        fields = ["id", "nome", "email", "password", "cpf", "data_nascimento", "role", "ativo"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)

class AlunoSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source="user.nome", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    ativo = serializers.BooleanField(source="user.ativo", read_only=True)
    class Meta:
        model = Aluno
        fields = ["id", "nome", "email", "matricula", "ativo"]

class ProfessorSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source="user.nome", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    cpf = serializers.CharField(source="user.cpf", read_only=True)
    data_nascimento = serializers.DateField(source="user.data_nascimento", read_only=True)
    ativo = serializers.BooleanField(source="user.ativo", read_only=True)
    class Meta:
        model = Professor
        fields = ["id", "nome", "email", "cpf", "data_nascimento", "ativo"]