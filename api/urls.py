from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'cursos', views.CursoViewSet)
router.register(r'modulos', views.ModuloViewSet)
router.register(r'lecciones', views.LeccionViewSet)
router.register(r'inscripciones', views.InscripcionViewSet)
router.register(r'quizzes', views.QuizViewSet)
router.register(r'intentos-quiz', views.IntentoQuizViewSet)
router.register(r'certificados', views.CertificadoViewSet)
router.register(r'mensajes', views.MensajeViewSet)

urlpatterns = [
    # Auth endpoints
    path('auth/login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', views.refresh_token_view, name='token_refresh'),
    path('auth/registro/', views.registro_view, name='registro'),
    path('auth/google/', views.google_auth_view, name='google-auth'),
    path('auth/me/', views.me_view, name='me'),
    path('auth/logout/', views.logout_view, name='logout'),
    
    # API endpoints
    path('', include(router.urls)),
    path('verificar/<str:codigo>/', views.verificar_certificado, name='verificar-certificado'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
]
