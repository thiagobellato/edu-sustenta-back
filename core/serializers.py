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
            "cpf",             # Novo
            "data_nascimento", # Novo
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class AlunoSerializer(serializers.ModelSerializer):
    # Como tiramos esses campos do modelo Aluno, precisamos 
    # buscá-los no User relacionado usando 'source'
    nome = serializers.CharField(source='user.nome', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    ativo = serializers.BooleanField(source='user.ativo', read_only=True)
    cpf = serializers.CharField(source='user.cpf', read_only=True)

    class Meta:
        model = Aluno
        fields = [
            "id",
            "nome",      # Vem do user
            "email",     # Vem do user
            "ativo",     # Vem do user
            "cpf",       # Vem do user
            "matricula", # Campo próprio do aluno
        ]


class ProfessorSerializer(serializers.ModelSerializer):
    # Mesmo processo do Aluno: busca dados no User
    nome = serializers.CharField(source='user.nome', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    ativo = serializers.BooleanField(source='user.ativo', read_only=True)
    cpf = serializers.CharField(source='user.cpf', read_only=True)

    class Meta:
        model = Professor
        fields = [
            "id",
            "nome",
            "email",
            "ativo",
            "cpf",
            "matricula",
            "comprovante_vinculo", # Campo novo de arquivo
        ]


# =======================================================
# SERIALIZER ESPECÍFICO PARA CADASTRO (WRITE-ONLY)
# =======================================================
class ProfessorCadastroSerializer(serializers.ModelSerializer):
    """
    Recebe tudo num formulário só (User + Professor + Arquivo)
    e salva em duas tabelas diferentes.
    """
    # Campos do User (precisamos declarar explícito pois o model aqui é Professor)
    nome = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    cpf = serializers.CharField(max_length=14)
    data_nascimento = serializers.DateField()

    class Meta:
        model = Professor
        fields = [
            'nome', 
            'email', 
            'password', 
            'cpf', 
            'data_nascimento', 
            'matricula', 
            'comprovante_vinculo'
        ]

    def create(self, validated_data):
        # 1. Separa e retira os dados do Usuário do dicionário
        user_data = {
            'email': validated_data.pop('email'),
            'nome': validated_data.pop('nome'),
            'password': validated_data.pop('password'),
            'cpf': validated_data.pop('cpf'),
            'data_nascimento': validated_data.pop('data_nascimento'),
            'role': 'PROFESSOR'
        }

        # 2. Cria o Usuário (isso já hash a senha)
        user = User.objects.create_user(**user_data)

        # 3. Cria o Professor vinculado ao usuário
        # O que sobrou em validated_data é matricula e comprovante
        professor = Professor.objects.create(user=user, **validated_data)
        
        return professor