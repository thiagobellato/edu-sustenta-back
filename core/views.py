from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from .models import Aluno, Professor
from .serializers import (
    AlunoSerializer,
    ProfessorSerializer,
    UserSerializer,
)

User = get_user_model()


def home(request):
    return JsonResponse({"status": "API Edusustenta está rodando"})


# ==========================
# USERS
# ==========================
class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(ativo=True)
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()

        # DELETE LÓGICO CORRETO
        user.ativo = False
        user.save(update_fields=["ativo"])

        return Response(
            {"detail": "Usuário desativado com sucesso."},
            status=status.HTTP_200_OK
        )


# ==========================
# ALUNOS
# ==========================
class AlunoViewSet(ModelViewSet):
    queryset = Aluno.objects.filter(ativo=True)
    serializer_class = AlunoSerializer

    def destroy(self, request, *args, **kwargs):
        aluno = self.get_object()
        aluno.ativo = False
        aluno.save(update_fields=["ativo"])
        return Response(
            {"detail": "Aluno desativado com sucesso."},
            status=status.HTTP_200_OK
        )


# ==========================
# PROFESSORES
# ==========================
class ProfessorViewSet(ModelViewSet):
    queryset = Professor.objects.filter(ativo=True)
    serializer_class = ProfessorSerializer

    def destroy(self, request, *args, **kwargs):
        professor = self.get_object()
        professor.ativo = False
        professor.save(update_fields=["ativo"])
        return Response(
            {"detail": "Professor desativado com sucesso."},
            status=status.HTTP_200_OK
        )


# ==========================
# FUTUROS VIEWSETS (PAUSADOS)
# ==========================

# class TrilhaViewSet(ModelViewSet):
#     queryset = Trilha.obje
