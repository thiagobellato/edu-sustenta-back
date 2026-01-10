from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # REGRA DE NEGÓCIO: cria entidade dependente (SEGURA)
        if user.role == "ALUNO":
            Aluno.objects.get_or_create(
                user=user,
                defaults={
                    "matricula": f"ALU-{user.id}"
                }
            )

        elif user.role == "PROFESSOR":
            Professor.objects.get_or_create(
                user=user,
                defaults={
                    "matricula": f"PROF-{user.id}"
                }
            )

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()

        # DELETE LÓGICO CENTRALIZADO
        user.ativo = False
        user.save(update_fields=["ativo"])

        return Response(
            {"detail": "Usuário desativado com sucesso."},
            status=status.HTTP_200_OK
        )


# ==========================
# ALUNOS (SOMENTE LEITURA)
# ==========================
class AlunoViewSet(ReadOnlyModelViewSet):
    queryset = Aluno.objects.filter(user__ativo=True)
    serializer_class = AlunoSerializer


# ==========================
# PROFESSORES (SOMENTE LEITURA)
# ==========================
class ProfessorViewSet(ReadOnlyModelViewSet):
    queryset = Professor.objects.filter(user__ativo=True)
    serializer_class = ProfessorSerializer
