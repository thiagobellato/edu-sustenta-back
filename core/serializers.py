from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Aluno, Professor, School, TeacherSchoolLink, Notification, Trail, Module, generate_school_token

User = get_user_model()

# ==================================================
# 1. SERIALIZER DE LOGIN (Email + Password)
# ==================================================
class CustomLoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuário não encontrado")

        # authenticate precisa do USERNAME_FIELD, que é 'email'
        user = authenticate(self.context['request'], email=email, password=password)

        if not user:
            raise serializers.ValidationError("Credenciais inválidas")

        refresh = self.get_token(user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "id": user.id,
            "email": user.email,  # garante compatibilidade com front
            "name": user.first_name,
            "role": user.role.lower(),
            "has_school": False
        }

        if user.role.lower() == "professor":
            data["has_school"] = TeacherSchoolLink.objects.filter(
                user=user,
                status="APPROVED"
            ).exists()

        return data


# ==================================================
# 2. USER SERIALIZER (Perfil Completo)
# ==================================================
class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name', required=False)
    has_school = serializers.SerializerMethodField()
    schools = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'password',
            'role', 'cpf', 'matricula', 'data_nascimento', 'ativo',
            'name', 'has_school', 'schools'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret.get('role'):
            ret['role'] = ret['role'].lower()
        return ret

    def get_has_school(self, obj):
        role = str(obj.role).lower()
        if role == 'professor':
            return TeacherSchoolLink.objects.filter(user=obj, status='APPROVED').exists()
        return False

    def get_schools(self, obj):
        role = str(obj.role).lower()
        if role == 'professor':
            links = TeacherSchoolLink.objects.filter(user=obj, status='APPROVED')
            return [{"id": link.school.id, "name": link.school.name} for link in links]
        return []

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        role = validated_data.get('role', 'USER')

        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()

        # Cria perfil apenas se não for USER genérico
        if role == 'ALUNO':
            Aluno.objects.get_or_create(user=user)
        elif role == 'PROFESSOR':
            Professor.objects.get_or_create(user=user)

        return user


# ==================================================
# 3. OUTROS SERIALIZERS
# ==================================================
class TeacherSchoolLinkSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model = TeacherSchoolLink
        fields = ['id', 'school', 'school_name', 'status', 'date_linked']


class AlunoSerializer(serializers.ModelSerializer):
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


# ===========================
# School Serializer Corrigido
# ===========================
class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'invite_token', 'token_uses_remaining', 'active']
        read_only_fields = ['invite_token', 'token_uses_remaining', 'active']

    def create(self, validated_data):
        if 'invite_token' not in validated_data or not validated_data.get('invite_token'):
            validated_data['invite_token'] = generate_school_token()
        return super().create(validated_data)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'is_read', 'created_at']


class ProfessorCadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'matricula']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['role'] = 'PROFESSOR'
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        Professor.objects.create(user=user)
        return user


# ===========================
# Trail & Module Serializers
# ===========================
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order']
        read_only_fields = ['id']


class TrailSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, required=False)
    created_by_name = serializers.CharField(source='created_by.first_name', read_only=True)
    
    class Meta:
        model = Trail
        fields = [
            'id', 'title', 'description', 'status', 'created_by', 
            'created_by_name', 'created_at', 'updated_at',
            'category', 'difficulty', 'cover_image', 'modules'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        modules_data = validated_data.pop('modules', [])
        trail = Trail.objects.create(**validated_data)
        
        for index, module_data in enumerate(modules_data):
            Module.objects.create(trail=trail, order=index, **module_data)
        
        return trail
    
    def update(self, instance, validated_data):
        modules_data = validated_data.pop('modules', None)
        
        # Atualiza campos da trilha
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Atualiza módulos se fornecidos
        if modules_data is not None:
            # Remove módulos existentes
            instance.modules.all().delete()
            # Cria novos módulos
            for index, module_data in enumerate(modules_data):
                Module.objects.create(trail=instance, order=index, **module_data)
        
        return instance