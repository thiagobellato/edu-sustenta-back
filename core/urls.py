from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlunoViewSet, ProfessorViewSet

router = DefaultRouter()
router.register(r'alunos', AlunoViewSet)
router.register(r'professores', ProfessorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
