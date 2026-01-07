from rest_framework.viewsets import ModelViewSet
from .models import Aluno, Professor
from .serializers import AlunoSerializer, ProfessorSerializer
from django.http import JsonResponse

def home(request):
    return JsonResponse({"status": "API Edusustenta está rodando"})

class ProfessorViewSet(ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer


class AlunoViewSet(ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
