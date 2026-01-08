from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import Aluno, Professor
from .serializers import AlunoSerializer, ProfessorSerializer


def home(request):
    return JsonResponse({"status": "API Edusustenta está rodando"})


class ProfessorViewSet(ModelViewSet):
    queryset = Professor.objects.filter(ativo=True)
    serializer_class = ProfessorSerializer

    def destroy(self, request, *args, **kwargs):
        professor = self.get_object()
        professor.ativo = False
        professor.save()

        return Response(
            {"detail": "Professor desativado com sucesso."},
            status=status.HTTP_204_NO_CONTENT,
        )


class AlunoViewSet(ModelViewSet):
    queryset = Aluno.objects.filter(ativo=True)
    serializer_class = AlunoSerializer

    def destroy(self, request, *args, **kwargs):
        aluno = self.get_object()
        aluno.ativo = False
        aluno.save()

        return Response(
            {"detail": "Aluno desativado com sucesso."},
            status=status.HTTP_204_NO_CONTENT,
        )
