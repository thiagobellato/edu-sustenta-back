from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db import transaction
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Aluno, Professor, School, TeacherSchoolLink, Notification
from .serializers import (
    AlunoSerializer,
    ProfessorSerializer,
    UserSerializer,
    ProfessorCadastroSerializer,
    NotificationSerializer,
    SchoolSerializer,
    CustomLoginSerializer,
    TeacherSchoolLinkSerializer
)

User = get_user_model()

def home(request):
    return JsonResponse({"status": "API EduSustenta está rodando", "version": "2.7"})


# ==========================
# LOGIN & AUTH
# ==========================
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer


class JoinSchoolView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle] 

    def post(self, request):
        if request.user.role != 'ALUNO':
            return Response({"error": "Apenas Alunos podem utilizar este token."}, status=400)

        token_input = request.data.get('token', '').upper().strip()
        if len(token_input) < 6:
            return Response({"error": "Token inválido."}, status=400)

        try:
            with transaction.atomic():
                try:
                    school = School.objects.select_for_update().get(invite_token=token_input, active=True)
                except School.DoesNotExist:
                    return Response({"error": "Escola não encontrada."}, status=404)

                if school.token_uses_remaining <= 0:
                    now = timezone.now()
                    if (now - school.token_last_reset) > timedelta(minutes=15):
                        school.token_uses_remaining = 5
                        school.token_last_reset = now
                        school.save()
                    else:
                        return Response({"error": "Token esgotado. Tente em alguns minutos."}, status=429)

                user = request.user
                if TeacherSchoolLink.objects.filter(user=user, school=school).exists():
                    return Response({"error": "Você já está nesta escola."}, status=400)

                school.token_uses_remaining -= 1
                school.save()
                
                user.role = 'PROFESSOR'
                user.save()
                Professor.objects.get_or_create(user=user)

                TeacherSchoolLink.objects.create(user=user, school=school, status='APPROVED')
                
                Notification.objects.create(
                    user=user,
                    title="Parabéns, Professor!",
                    message=f"Você foi vinculado com sucesso à escola {school.name}."
                )

                return Response({
                    "message": "Sucesso! Vínculo criado.",
                    "school": school.name,
                    "role": user.role.lower()
                }, status=200)

        except Exception:
            return Response({"error": "Erro interno."}, status=500)


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = user.role.upper()

        if role == 'GESTOR':
            minhas_escolas = School.objects.filter(manager=user)
            total_professores = TeacherSchoolLink.objects.filter(
                school__in=minhas_escolas, status='APPROVED'
            ).count()

            recent_links = TeacherSchoolLink.objects.filter(
                school__in=minhas_escolas
            ).order_by('-date_linked')[:5]

            data = {
                "total_escolas": minhas_escolas.count(),
                "total_professores": total_professores,
                "alunos_impactados": 0,
                "recentActivity": [
                    {
                        "id": link.id,
                        "text": f"Prof. {link.user.first_name} entrou em {link.school.name}",
                        "time": link.date_linked.strftime("%d/%m %H:%M")
                    } for link in recent_links
                ]
            }

        elif role == 'PROFESSOR':
            vinculos = TeacherSchoolLink.objects.filter(user=user, status='APPROVED')
            data = {
                "escolas_vinculadas": vinculos.count(), 
                "total_atividades": 0,
                "total_alunos": 0,
                "recentActivity": [{"id": 1, "text": "Vínculo com escola ativo!", "time": "Agora"}]
            }

        else:
            data = {"escolas_vinculadas": 0, "message": "Painel de Aluno"}

        return Response(data)


# ==========================
# VIEWSETS
# ==========================
class TeacherSchoolViewSet(ReadOnlyModelViewSet):
    serializer_class = TeacherSchoolLinkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TeacherSchoolLink.objects.filter(user=self.request.user)


class SchoolViewSet(ModelViewSet):
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if user.role.lower() == 'gestor':
            # retorna todas as escolas que o gestor gerencia
            return School.objects.filter(manager=user)
            
        elif user.role.lower() == 'professor':
            # retorna escolas vinculadas ao professor
            return School.objects.filter(
                teacherschoollink__user=user, 
                teacherschoollink__status='APPROVED'
            )
        
        else:
            # fallback seguro: retorna apenas escolas ativas
            # isso garante que o invite_token sempre estará disponível
            return School.objects.filter(active=True)

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)


class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(ativo=True)
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class AlunoViewSet(ReadOnlyModelViewSet):
    queryset = Aluno.objects.filter(user__ativo=True)
    serializer_class = AlunoSerializer


class ProfessorViewSet(ReadOnlyModelViewSet):
    queryset = Professor.objects.filter(user__ativo=True)
    serializer_class = ProfessorSerializer


class ProfessorCreateView(generics.CreateAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorCadastroSerializer
    permission_classes = [AllowAny]