from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from django.db import IntegrityError
from django.http import JsonResponse
from datetime import datetime, timedelta
import uuid
import hashlib

from .models import (
    Usuario, Curso, Modulo, Leccion, Inscripcion,
    Quiz, Pregunta, Opcion, IntentoQuiz, RespuestaQuiz,
    Certificado, Mensaje
)
from .serializers import (
    CustomTokenObtainPairSerializer, UsuarioSerializer, RegistroSerializer,
    CursoSerializer, CursoDetalleSerializer,
    ModuloSerializer, LeccionSerializer, InscripcionSerializer,
    QuizSerializer, QuizDetalleSerializer, PreguntaSerializer,
    IntentoQuizSerializer, CertificadoSerializer, MensajeSerializer
)


def set_token_cookies(response, refresh_token, access_token):
    """Set JWT tokens as httpOnly cookies"""
    response.set_cookie(
        'access_token', access_token,
        httponly=True, secure=False, samesite='Lax',
        max_age=3600  # 1 hour
    )
    response.set_cookie(
        'refresh_token', refresh_token,
        httponly=True, secure=False, samesite='Lax',
        max_age=7 * 24 * 3600  # 7 days
    )
    return response


def clear_token_cookies(response):
    """Clear JWT cookies"""
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response


# ============ AUTH VIEWS ============

class CustomTokenObtainPairView(TokenObtainPairView):
    """Login: returns user + tokens (body) + sets httpOnly cookies (fallback)"""
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        refresh = RefreshToken.for_user(user)

        response = Response({
            'user': {
                'id': str(user.id),
                'nombre': f"{user.first_name} {user.last_name}".strip() or user.username,
                'email': user.email,
                'rol': user.rol,
                'avatar': user.avatar if user.avatar else None,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
        return set_token_cookies(response, str(refresh), str(refresh.access_token))


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def registro_view(request):
    """Register new student"""
    serializer = RegistroSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response = Response({
            'user': {
                'id': str(user.id),
                'nombre': f"{user.first_name} {user.last_name}".strip(),
                'email': user.email,
                'rol': user.rol,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)
        return set_token_cookies(response, str(refresh), str(refresh.access_token))
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def me_view(request):
    """Get current user data - reads token from cookie or header"""
    user = request.user
    return Response({
        'id': str(user.id),
        'nombre': f"{user.first_name} {user.last_name}".strip() or user.username,
        'email': user.email,
        'rol': user.rol,
        'telefono': user.telefono,
        'avatar': user.avatar,
    })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def logout_view(request):
    """Logout: blacklists refresh token + clears cookies"""
    try:
        refresh_token = request.COOKIES.get('refresh_token') or request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
    except Exception:
        pass

    response = Response({'mensaje': 'Sesión cerrada exitosamente'})
    return clear_token_cookies(response)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def google_auth_view(request):
    """Login/Register with Google via Firebase"""
    email = request.data.get('email')
    nombre = request.data.get('nombre', '')
    apellido = request.data.get('apellido', '')
    avatar = request.data.get('avatar', '')

    if not email:
        return Response({'detail': 'Email requerido'}, status=400)

    try:
        user = Usuario.objects.get(email=email)
        user.avatar = avatar or user.avatar
        user.save()
    except Usuario.DoesNotExist:
        try:
            user = Usuario.objects.create_user(
                username=email.split('@')[0] + '_' + str(uuid.uuid4())[:6],
                email=email,
                first_name=nombre,
                last_name=apellido,
                avatar=avatar,
                rol='estudiante',
            )
        except IntegrityError:
            user = Usuario.objects.create_user(
                username=f"user_{uuid.uuid4().hex[:8]}",
                email=email,
                first_name=nombre,
                last_name=apellido,
                avatar=avatar,
                rol='estudiante',
            )

    refresh = RefreshToken.for_user(user)
    response = Response({
        'user': {
            'id': str(user.id),
            'nombre': f"{user.first_name} {user.last_name}".strip() or user.username,
            'email': user.email,
            'rol': user.rol,
            'avatar': user.avatar,
        },
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })
    return set_token_cookies(response, str(refresh), str(refresh.access_token))


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def refresh_token_view(request):
    """Refresh access token using refresh cookie"""
    refresh_token = request.COOKIES.get('refresh_token')
    if not refresh_token:
        return Response({'detail': 'No refresh token'}, status=401)

    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        response = Response({'access': access_token})
        response.set_cookie(
            'access_token', access_token,
            httponly=True, secure=False, samesite='Lax',
            max_age=3600
        )
        return response
    except Exception:
        response = Response({'detail': 'Token inválido'}, status=401)
        return clear_token_cookies(response)


# ============ CURSO VIEWS ============

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CursoDetalleSerializer
        return CursoSerializer
    
    def get_queryset(self):
        queryset = Curso.objects.all()
        profesor_id = self.request.query_params.get('profesor')
        nivel = self.request.query_params.get('nivel')
        activo = self.request.query_params.get('activo')
        buscar = self.request.query_params.get('buscar')
        
        if profesor_id:
            queryset = queryset.filter(profesor_id=profesor_id)
        if nivel:
            queryset = queryset.filter(nivel=nivel)
        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() == 'true')
        if buscar:
            queryset = queryset.filter(
                Q(titulo__icontains=buscar) | Q(descripcion__icontains=buscar)
            )
        return queryset.order_by('-fecha_creacion')


class ModuloViewSet(viewsets.ModelViewSet):
    queryset = Modulo.objects.all()
    serializer_class = ModuloSerializer
    
    def get_queryset(self):
        queryset = Modulo.objects.all()
        curso_id = self.request.query_params.get('curso')
        if curso_id:
            queryset = queryset.filter(curso_id=curso_id)
        return queryset.order_by('orden')


class LeccionViewSet(viewsets.ModelViewSet):
    queryset = Leccion.objects.all()
    serializer_class = LeccionSerializer
    
    def get_queryset(self):
        queryset = Leccion.objects.all()
        modulo_id = self.request.query_params.get('modulo')
        if modulo_id:
            queryset = queryset.filter(modulo_id=modulo_id)
        return queryset.order_by('orden')


class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
    
    def get_queryset(self):
        queryset = Inscripcion.objects.all()
        estudiante_id = self.request.query_params.get('estudiante')
        curso_id = self.request.query_params.get('curso')
        if estudiante_id:
            queryset = queryset.filter(estudiante_id=estudiante_id)
        if curso_id:
            queryset = queryset.filter(curso_id=curso_id)
        return queryset.order_by('-fecha_inscripcion')


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuizDetalleSerializer
        return QuizSerializer


class IntentoQuizViewSet(viewsets.ModelViewSet):
    queryset = IntentoQuiz.objects.all()
    serializer_class = IntentoQuizSerializer
    
    def get_queryset(self):
        queryset = IntentoQuiz.objects.all()
        quiz_id = self.request.query_params.get('quiz')
        estudiante_id = self.request.query_params.get('estudiante')
        if quiz_id:
            queryset = queryset.filter(quiz_id=quiz_id)
        if estudiante_id:
            queryset = queryset.filter(estudiante_id=estudiante_id)
        return queryset.order_by('-fecha_inicio')


class CertificadoViewSet(viewsets.ModelViewSet):
    queryset = Certificado.objects.all()
    serializer_class = CertificadoSerializer
    http_method_names = ['get', 'post', 'head', 'options']
    
    def get_queryset(self):
        queryset = Certificado.objects.all()
        estudiante_id = self.request.query_params.get('estudiante')
        if estudiante_id:
            queryset = queryset.filter(estudiante_id=estudiante_id)
        return queryset.order_by('-fecha_emision')


class MensajeViewSet(viewsets.ModelViewSet):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer


# ============ PUBLIC VIEWS ============

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def verificar_certificado(request, codigo):
    try:
        certificado = Certificado.objects.get(codigo=codigo)
        serializer = CertificadoSerializer(certificado)
        return Response(serializer.data)
    except Certificado.DoesNotExist:
        return Response({'error': 'Certificado no encontrado'}, status=404)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def estadisticas(request):
    data = {
        'total_cursos': Curso.objects.filter(activo=True).count(),
        'total_estudiantes': Usuario.objects.filter(rol='estudiante').count(),
        'total_profesores': Usuario.objects.filter(rol='profesor').count(),
        'total_inscripciones': Inscripcion.objects.count(),
        'total_certificados': Certificado.objects.count(),
    }
    return Response(data)
