from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AlunoViewSet,
    ProfessorViewSet,
    UserViewSet,
    ProfessorCreateView,
    ConsultaCPFView
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"alunos", AlunoViewSet)
router.register(r"professores", ProfessorViewSet)

urlpatterns = [
    # === ROTAS MANUAIS (Prioridade Alta) ===
    # Removemos o "api/" daqui porque ele já vem do arquivo principal
    
    # URL Final: /api/professores/cadastro/
    path("professores/cadastro/", ProfessorCreateView.as_view(), name="professor-cadastro"),

    # URL Final: /api/consulta-cpf/<cpf>/
    # (CORRIGIDO: Antes estava "api/consulta-cpf/...", gerando duplicidade)
    path("consulta-cpf/<str:cpf>/", ConsultaCPFView.as_view(), name="consulta-cpf"),

    # === ROTAS AUTOMÁTICAS (Router) ===
    path("", include(router.urls)),
]