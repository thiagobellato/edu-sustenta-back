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


# --- ESTA FUNÇÃO PRECISA EXISTIR PARA O URLS.PY FUNCIONAR ---
def home(request):
    return JsonResponse({"status": "API Edusustenta está rodando"})


# ==========================
# USERS
# ==========================
class UserViewSet(ModelViewSet):
    """
    Endpoint principal para criação e gestão de usuários.
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save(update_fields=["is_active"])
        return Response(
            {"detail": "Usuário desativado com sucesso."},
            status=status.HTTP_200_OK,
        )


# ==========================
# ALUNOS (Somente Leitura)
# ==========================
class AlunoViewSet(ReadOnlyModelViewSet):
    queryset = Aluno.objects.filter(user__is_active=True)
    serializer_class = AlunoSerializer


# ==========================
# PROFESSORES (Somente Leitura)
# ==========================
class ProfessorViewSet(ReadOnlyModelViewSet):
    queryset = Professor.objects.filter(user__is_active=True)
    serializer_class = ProfessorSerializer
