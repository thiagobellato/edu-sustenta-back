from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Aluno, Professor, School, TeacherSchoolLink

User = get_user_model()

# ==================================================
# 1. USER SERIALIZER (Cadastro e Listagem Geral)
# ==================================================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Listamos todos os campos novos que adicionamos no models.py
        fields = [
            'id', 'username', 'email', 'first_name', 'password', 
            'role', 'cpf', 'matricula', 'data_nascimento', 'ativo'
        ]
        # A senha deve ser apenas de escrita (não retorna na API por segurança)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Sobrescrevemos o create para garantir que a senha seja criptografada
        e o perfil (Aluno/Professor) seja criado automaticamente.
        """
        password = validated_data.pop('password', None)
        role = validated_data.get('role', 'ALUNO')
        
        # Cria o usuário
        user = User(**validated_data)
        if password:
            user.set_password(password) # Criptografa a senha
        user.save()

        # Cria o perfil correspondente automaticamente
        if role == 'ALUNO':
            Aluno.objects.get_or_create(user=user)
        elif role == 'PROFESSOR':
            Professor.objects.get_or_create(user=user)
            
        return user

# ==================================================
# 2. SERIALIZERS DE PERFIL (Leitura)
# ==================================================
class AlunoSerializer(serializers.ModelSerializer):
    # Trazemos dados do usuário para facilitar o front-end
    nome = serializers.CharField(source='user.first_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    cpf = serializers.CharField(source='user.cpf', read_only=True)

    class Meta:
        model = Aluno
        fields = ['id', 'user', 'nome', 'email', 'cpf']

class ProfessorSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='user.first_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    matricula = serializers.CharField(source='user.matricula', read_only=True)

    class Meta:
        model = Professor
        fields = ['id', 'user', 'nome', 'email', 'matricula']

# ==================================================
# 3. LEGADO / ESPECÍFICOS
# ==================================================

# Mantivemos este nome pois a View antiga ainda o importa.
# Redirecionamos ele para comportar-se como um UserSerializer simplificado.
class ProfessorCadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'matricula']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        validated_data['role'] = 'PROFESSOR'
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Professor.objects.create(user=user)
        return user