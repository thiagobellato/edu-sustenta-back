from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AlunoViewSet,
    ProfessorViewSet,
    UserViewSet,
    ProfessorCreateView,
    JoinSchoolView # <--- Nova View
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"alunos", AlunoViewSet)
router.register(r"professores", ProfessorViewSet)

urlpatterns = [
    # Rota para converter Aluno -> Professor via Token
    path("schools/join/", JoinSchoolView.as_view(), name="join-school"),

    # Cadastro inicial (se mantido)
    path("professores/cadastro/", ProfessorCreateView.as_view(), name="professor-cadastro"),

    # Rotas do Router
    path("", include(router.urls)),
]