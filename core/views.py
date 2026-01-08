from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from .models import Aluno, Professor, Trilha, Escola
from .serializers import (
    AlunoSerializer,
    ProfessorSerializer,
    UserSerializer,
    TrilhaSerializer,
    EscolaSerializer,
)

User = get_user_model()


def home(request):
    return JsonResponse({"status": "API Edusustenta está rodando"})


# ==========================
# USERS
# ==========================
class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==========================
# ALUNOS
# ==========================
class AlunoViewSet(ModelViewSet):
    queryset = Aluno.objects.filter(ativo=True)
    serializer_class = AlunoSerializer

    def destroy(self, request, *args, **kwargs):
        aluno = self.get_object()
        aluno.ativo = False
        aluno.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==========================
# PROFESSORES
# ==========================
class ProfessorViewSet(ModelViewSet):
    queryset = Professor.objects.filter(ativo=True)
    serializer_class = ProfessorSerializer

    def destroy(self, request, *args, **kwargs):
        professor = self.get_object()
        professor.ativo = False
        professor.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==========================
# TRILHAS
# ==========================
class TrilhaViewSet(ModelViewSet):
    queryset = Trilha.objects.filter(ativo=True)
    serializer_class = TrilhaSerializer

    def destroy(self, request, *args, **kwargs):
        trilha = self.get_object()
        trilha.ativo = False
        trilha.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==========================
# ESCOLAS
# ==========================
class EscolaViewSet(ModelViewSet):
    queryset = Escola.objects.filter(ativo=True)
    serializer_class = EscolaSerializer

    def destroy(self, request, *args, **kwargs):
        escola = self.get_object()
        escola.ativo = False
        escola.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
