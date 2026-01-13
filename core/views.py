from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser # Necessário para upload de arquivos
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from .models import Aluno, Professor
from .serializers import (
    AlunoSerializer,
    ProfessorSerializer,
    UserSerializer,
    ProfessorCadastroSerializer # Certifique-se de criar este no serializers.py
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
    # CORREÇÃO: Filtra pelo ativo do User relacionado
    queryset = Aluno.objects.filter(user__ativo=True)
    serializer_class = AlunoSerializer

    def destroy(self, request, *args, **kwargs):
        aluno = self.get_object()
        # CORREÇÃO: Desativa o User vinculado, não o Aluno diretamente
        aluno.user.ativo = False
        aluno.user.save(update_fields=["ativo"])
        
        return Response(
            {"detail": "Aluno desativado com sucesso."},
            status=status.HTTP_200_OK
        )

# ==========================
# PROFESSORES (Gestão)
# ==========================
class ProfessorViewSet(ModelViewSet):
    # CORREÇÃO: Filtra pelo ativo do User relacionado
    queryset = Professor.objects.filter(user__ativo=True)
    serializer_class = ProfessorSerializer

    def destroy(self, request, *args, **kwargs):
        professor = self.get_object()
        # CORREÇÃO: Desativa o User vinculado
        professor.user.ativo = False
        professor.user.save(update_fields=["ativo"])
        
        return Response(
            {"detail": "Professor desativado com sucesso."},
            status=status.HTTP_200_OK
        )

# ==========================
# CADASTRO PÚBLICO (Sign Up)
# ==========================
class ProfessorCreateView(generics.CreateAPIView):
    """
    View específica para o cadastro público de professores.
    Aceita Multipart (Arquivos + JSON).
    """
    queryset = Professor.objects.all()
    serializer_class = ProfessorCadastroSerializer
    # Permite upload de arquivos e dados de formulário
    parser_classes = (MultiPartParser, FormParser) 
    # permission_classes = [AllowAny] # Descomente se quiser liberar sem login