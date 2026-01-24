from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Aluno, Professor, School, TeacherSchoolLink, Notification

User = get_user_model()


# =========================
# Login
# =========================

class CustomLoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuário não encontrado")

        if not user.check_password(password):
            raise serializers.ValidationError("Senha incorreta")

        if not user.is_active:
            raise serializers.ValidationError("Usuário inativo")

        refresh = self.get_token(user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "id": user.id,
            "name": user.name,
            "role": user.role.lower(),
            "has_school": False,
        }

        if user.role == "PROFESSOR":
            data["has_school"] = TeacherSchoolLink.objects.filter(
                user=user, status="APPROVED"
            ).exists()

        return data


# =========================
# User
# =========================

class UserSerializer(serializers.ModelSerializer):
    has_school = serializers.SerializerMethodField()
    schools = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "name",
            "role",
            "cpf",
            "matricula",
            "data_nascimento",
            "ativo",
            "has_school",
            "schools",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "role": {"read_only": True},
        }

    def get_has_school(self, obj):
        if obj.role == "PROFESSOR":
            return TeacherSchoolLink.objects.filter(
                user=obj, status="APPROVED"
            ).exists()
        return False

    def get_schools(self, obj):
        if obj.role == "PROFESSOR":
            links = TeacherSchoolLink.objects.filter(user=obj, status="APPROVED")
            return [{"id": link.school.id, "name": link.school.name} for link in links]
        return []

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        Aluno.objects.get_or_create(user=user)
        return user


# =========================
# TeacherSchoolLink
# =========================

class TeacherSchoolLinkSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source="school.name", read_only=True)

    class Meta:
        model = TeacherSchoolLink
        fields = ["id", "school", "school_name", "status", "date_linked"]


# =========================
# Aluno / Professor
# =========================

class AlunoSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source="user.name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    cpf = serializers.CharField(source="user.cpf", read_only=True)

    class Meta:
        model = Aluno
        fields = ["id", "user", "nome", "email", "cpf"]


class ProfessorSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source="user.name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    matricula = serializers.CharField(source="user.matricula", read_only=True)

    class Meta:
        model = Professor
        fields = ["id", "user", "nome", "email", "matricula"]


# =========================
# School
# =========================

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ["id", "name", "invite_token", "token_uses_remaining", "active"]
        read_only_fields = ["invite_token", "token_uses_remaining", "active"]


# =========================
# Notification
# =========================

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "title", "message", "is_read", "created_at"]


# =========================
# Cadastro de Professor
# =========================

class ProfessorCadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "name", "matricula"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.role = "PROFESSOR"
        user.save()

        Professor.objects.create(user=user)
        return user