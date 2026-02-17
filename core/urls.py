from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    AlunoViewSet,
    ProfessorViewSet,
    UserViewSet,
    NotificationViewSet,
    SchoolViewSet,
    TeacherSchoolViewSet, # [NOVO]
    ProfessorCreateView,
    JoinSchoolView,
    BecomeAlunoView,
    DashboardStatsView,
    CustomLoginView,
    TrailViewSet
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"alunos", AlunoViewSet)
router.register(r"professores", ProfessorViewSet)
router.register(r"notifications", NotificationViewSet, basename="notifications")
router.register(r"schools", SchoolViewSet, basename="schools") # Gestor vê escolas
router.register(r"teacher-schools", TeacherSchoolViewSet, basename="teacher-schools") # [NOVO] Professor vê suas escolas
router.register(r"trails", TrailViewSet, basename="trails")

urlpatterns = [
    path('token/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("schools/join/", JoinSchoolView.as_view(), name="join-school"),
    path("users/become-aluno/", BecomeAlunoView.as_view(), name="become-aluno"),
    path("dashboard/stats/", DashboardStatsView.as_view(), name="dashboard-stats"),
    path("professores/cadastro/", ProfessorCreateView.as_view(), name="professor-cadastro"),
    path("", include(router.urls)),
]