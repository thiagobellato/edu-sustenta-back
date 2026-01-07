from rest_framework import serializers
from .models import Aluno, Professor


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = "__all__"


class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = "__all__"
