import requests
from datetime import datetime
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import generics
from rest_framework.views import APIView
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
    return JsonResponse({"status": "API EduSustenta está rodando"})

# ==========================================================
# 1. USERS (Gerenciamento Central - Full CRUD)
# ==========================================================
class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(ativo=True)
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Realiza o Soft Delete (apenas desativa o usuário)
        """
        user = self.get_object()
        user.ativo = False
        user.save(update_fields=["ativo"])
        return Response(
            {"detail": "Usuário desativado com sucesso."},
            status=status.HTTP_200_OK
        )

# ==========================================================
# 2. LISTAGEM DE PERFIS (Apenas Leitura - ReadOnly)
# ==========================================================
class AlunoViewSet(ReadOnlyModelViewSet):
    queryset = Aluno.objects.filter(user__ativo=True)
    serializer_class = AlunoSerializer

class ProfessorViewSet(ReadOnlyModelViewSet):
    queryset = Professor.objects.filter(user__ativo=True)
    serializer_class = ProfessorSerializer

# ==========================================================
# 3. CADASTRO PÚBLICO (Sign Up com Arquivo)
# ==========================================================
class ProfessorCreateView(generics.CreateAPIView):
    """
    Endpoint: POST /professores/cadastro/
    Aceita Multipart/Form-Data para enviar JSON + Arquivo PDF/IMG
    """
    queryset = Professor.objects.all()
    serializer_class = ProfessorCadastroSerializer
    parser_classes = (MultiPartParser, FormParser)

# ==========================================================
# 4. INTEGRAÇÃO EXTERNA (Consulta CPF) - CORRIGIDA
# ==========================================================
class ConsultaCPFView(APIView):
    """
    Endpoint: GET /api/consulta-cpf/<cpf>/
    Conecta com a API CPFHub, trata a data e retorna para o React.
    """
    def get(self, request, cpf):
        # Limpa o CPF mantendo apenas números
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        
        # URL da API CPFHub
        url = f"https://api.cpfhub.io/cpf/{cpf_limpo}"
        headers = {
            "x-api-key": "1a007394ec4d6307af3d3447422fa687c4474f5e2d2107917492d69ff28e2fb2",
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            
            # Debug no terminal para conferência (opcional)
            print(f"API Externa Status: {response.status_code}")

            if response.status_code == 200:
                json_response = response.json()
                
                # A API retorna { "success": true, "data": { ... } }
                if not json_response.get("success"):
                     return Response({"error": "CPF inválido ou não encontrado na base."}, status=404)

                # Pegamos o objeto real com os dados
                api_data = json_response.get("data", {})
                
                # TRATAMENTO DE DATA (Crucial para o React)
                # A API manda "15/06/1990", o HTML input date exige "1990-06-15"
                data_nascimento_br = api_data.get("birthDate")
                data_nascimento_iso = ""
                
                if data_nascimento_br:
                    try:
                        # Converte de BR para ISO
                        data_obj = datetime.strptime(data_nascimento_br, "%d/%m/%Y")
                        data_nascimento_iso = data_obj.strftime("%Y-%m-%d")
                    except ValueError:
                        pass # Se falhar, vai vazio e o usuário digita

                # Monta o JSON final com as chaves que o seu Front espera
                payload = {
                    "nome": api_data.get("name"),           
                    "data_nascimento": data_nascimento_iso, 
                    "situacao": "REGULAR" # A API CPFHub free as vezes não manda status, assumimos regular para preencher
                }
                
                return Response(payload, status=status.HTTP_200_OK)
            
            elif response.status_code == 404:
                return Response({"error": "CPF não encontrado."}, status=status.HTTP_404_NOT_FOUND)
            
            else:
                return Response(
                    {"error": "Erro ao consultar API externa."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            print(f"Erro interno na consulta: {e}")
            return Response(
                {"error": "Erro de conexão com o servidor de consulta."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )