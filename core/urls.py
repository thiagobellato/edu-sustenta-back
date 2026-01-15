from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AlunoViewSet,
    ProfessorViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"alunos", AlunoViewSet)
router.register(r"professores", ProfessorViewSet)
# router.register(r"escolas", EscolaViewSet)
# router.register(r"trilhas", TrilhaViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
