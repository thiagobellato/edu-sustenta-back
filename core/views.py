from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet # <--- Importante
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from .models import Aluno, Professor
from .serializers import (
    AlunoSerializer,
    ProfessorSerializer,
    UserSerializer,
    ProfessorCadastroSerializer
)

User = get_user_model()

def home(request):
    return JsonResponse({"status": "API Edusustenta está rodando"})

# ==========================
# USERS (Mantém tudo: GET, POST, PUT, DELETE)
# ==========================
class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(ativo=True)
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.ativo = False
        user.save(update_fields=["ativo"])
        return Response(
            {"detail": "Usuário desativado com sucesso."},
            status=status.HTTP_200_OK
        )

# ==========================
# ALUNOS (Somente Leitura: GET)
# ==========================
class AlunoViewSet(ReadOnlyModelViewSet): # <--- Mudou aqui
    queryset = Aluno.objects.filter(user__ativo=True)
    serializer_class = AlunoSerializer
    # Removemos o destroy() daqui, pois agora é ReadOnly. 
    # Para deletar um aluno, deleta-se o User associado.

# ==========================
# PROFESSORES (Somente Leitura: GET)
# ==========================
class ProfessorViewSet(ReadOnlyModelViewSet): # <--- Mudou aqui
    queryset = Professor.objects.filter(user__ativo=True)
    serializer_class = ProfessorSerializer
    # Removemos o destroy() daqui também.

# ==========================
# CADASTRO PÚBLICO (Sign Up)
# ==========================
class ProfessorCreateView(generics.CreateAPIView):
    """
    View específica para o cadastro (POST) público.
    Não afeta a listagem restrita acima.
    """
    queryset = Professor.objects.all()
    serializer_class = ProfessorCadastroSerializer
    parser_classes = (MultiPartParser, FormParser)