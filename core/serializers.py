from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Aluno, Professor, School, TeacherSchoolLink, Notification

User = get_user_model()


class CustomLoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuário não encontrado")

        attrs["username"] = user.username
        attrs["password"] = password

        data = super().validate(attrs)

        data.update({
            "id": user.id,
            "name": user.first_name,
            "role": user.role.lower(),
            "has_school": False,
        })

        if user.role.lower() == "professor":
            data["has_school"] = TeacherSchoolLink.objects.filter(
                user=user, status="APPROVED"
            ).exists()

        return data




class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="first_name", required=False)
    has_school = serializers.SerializerMethodField()
    schools = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "role",
            "cpf",
            "matricula",
            "data_nascimento",
            "ativo",
            "name",
            "has_school",
            "schools",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {"required": False},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get("role"):
            data["role"] = data["role"].lower()
        return data

    def get_has_school(self, obj):
        if obj.role.lower() == "professor":
            return TeacherSchoolLink.objects.filter(
                user=obj, status="APPROVED"
            ).exists()
        return False

    def get_schools(self, obj):
        if obj.role.lower() == "professor":
            links = TeacherSchoolLink.objects.filter(user=obj, status="APPROVED")
            return [{"id": link.school.id, "name": link.school.name} for link in links]
        return []

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        role = validated_data.get("role", "ALUNO")

        validated_data.setdefault("username", validated_data.get("email"))

        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()

        if role == "ALUNO":
            Aluno.objects.get_or_create(user=user)
        elif role == "PROFESSOR":
            Professor.objects.get_or_create(user=user)

        return user


class TeacherSchoolLinkSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source="school.name", read_only=True)
    school_cnpj = serializers.CharField(source="school.cnpj", read_only=True)

    class Meta:
        model = TeacherSchoolLink
        fields = ["id", "school", "school_name", "school_cnpj", "status", "date_linked"]


class AlunoSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source="user.first_name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    cpf = serializers.CharField(source="user.cpf", read_only=True)

    class Meta:
        model = Aluno
        fields = ["id", "user", "nome", "email", "cpf"]


class ProfessorSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source="user.first_name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    matricula = serializers.CharField(source="user.matricula", read_only=True)

    class Meta:
        model = Professor
        fields = ["id", "user", "nome", "email", "matricula"]


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ["id", "name", "invite_token", "token_uses_remaining", "active"]
        read_only_fields = ["invite_token", "token_uses_remaining", "active"]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "title", "message", "is_read", "created_at"]


class ProfessorCadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "matricula"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["role"] = "PROFESSOR"
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        Professor.objects.create(user=user)
        return user
