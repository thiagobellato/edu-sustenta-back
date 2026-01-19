from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.http import JsonResponse  # <--- Importante para a home

from .models import Aluno, Professor, School, TeacherSchoolLink
from .serializers import (
    AlunoSerializer,
    ProfessorSerializer,
    UserSerializer,
    ProfessorCadastroSerializer
)

User = get_user_model()

# ==========================
# 1. FUNÇÃO HOME (A que estava faltando)
# ==========================
def home(request):
    """
    Rota simples para verificar se a API está online.
    Acessível em http://127.0.0.1:8000/
    """
    return JsonResponse({"status": "API EduSustenta está rodando", "version": "2.0"})

# ==========================
# 2. VIEW DE CONVERSÃO (TOKEN DE ESCOLA)
# ==========================
class JoinSchoolView(APIView):
    """
    Recebe um token, valida as regras de negócio (5 usos / 15 mins)
    e converte o Aluno em Professor vinculado à escola.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token_input = request.data.get('token', '').upper().strip()

        # 1. Validação Básica
        if len(token_input) < 6:
            return Response({"error": "Token inválido (muito curto)."}, status=400)

        # 2. Busca Escola
        try:
            school = School.objects.get(invite_token=token_input, active=True)
        except School.DoesNotExist:
            return Response({"error": "Escola não encontrada ou token inválido."}, status=404)

        # 3. Lógica de Renovação Automática (15 min)
        if school.token_uses_remaining <= 0:
            now = timezone.now()
            tempo_passado = now - school.token_last_reset
            
            if tempo_passado > timedelta(minutes=15):
                # RENOVA O TOKEN
                school.token_uses_remaining = 5
                school.token_last_reset = now
                school.save()
            else:
                # AINDA BLOQUEADO
                minutos_restantes = 15 - int(tempo_passado.total_seconds() / 60)
                return Response({
                    "error": f"Token esgotado temporariamente. Tente novamente em {minutos_restantes} minutos."
                }, status=429) 

        # 4. Executa a Conversão
        user = request.user
        
        # Verifica se já não é vinculado
        if TeacherSchoolLink.objects.filter(user=user, school=school).exists():
            return Response({"error": "Você já está vinculado a esta escola."}, status=400)

        try:
            # Decrementa uso
            school.token_uses_remaining -= 1
            school.save()

            # Atualiza Role para Professor (se ainda for aluno)
            if user.role == 'ALUNO':
                user.role = 'PROFESSOR'
                user.save()
                
                # Garante que existe o perfil de Professor
                if not hasattr(user, 'professor_profile'):
                    Professor.objects.create(user=user)

            # Cria Vínculo
            TeacherSchoolLink.objects.create(
                user=user,
                school=school,
                status='APPROVED'
            )

            return Response({
                "message": "Sucesso! Você agora é um Professor vinculado à escola.",
                "school": school.name,
                "role": user.role
            }, status=200)

        except Exception as e:
            return Response({"error": f"Erro interno: {str(e)}"}, status=500)


# ==========================
# 3. VIEWSETS PADRÃO (CRUD)
# ==========================

class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(ativo=True)
    serializer_class = UserSerializer

class AlunoViewSet(ReadOnlyModelViewSet):
    queryset = Aluno.objects.filter(user__ativo=True)
    serializer_class = AlunoSerializer

class ProfessorViewSet(ReadOnlyModelViewSet):
    queryset = Professor.objects.filter(user__ativo=True)
    serializer_class = ProfessorSerializer

# Cadastro público inicial (ainda mantido para compatibilidade)
class ProfessorCreateView(generics.CreateAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorCadastroSerializer
    permission_classes = [AllowAny]