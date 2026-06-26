from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class Usuario(AbstractUser):
    """Modelo extendido de usuario"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    avatar = models.URLField(blank=True)
    rol = models.CharField(max_length=20, choices=[
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('admin', 'Administrador'),
    ], default='estudiante')
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='usuario_set',
        related_query_name='usuario',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='usuario_set',
        related_query_name='usuario',
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


class Curso(models.Model):
    """Modelo de cursos"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.URLField(blank=True)
    profesor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='cursos_impartidos')
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duracion_horas = models.IntegerField(default=0)
    nivel = models.CharField(max_length=20, choices=[
        ('basico', 'Básico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ], default='basico')
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_creacion']


class Modulo(models.Model):
    """Módulos de un curso"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='modulos')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    orden = models.IntegerField(default=0)
    duracion_minutos = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['orden']


class Leccion(models.Model):
    """Lecciones dentro de un módulo"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='lecciones')
    titulo = models.CharField(max_length=200)
    contenido = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    duracion_minutos = models.IntegerField(default=0)
    orden = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['orden']


class Inscripcion(models.Model):
    """Inscripciones de estudiantes a cursos"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='inscripciones')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False)
    progreso = models.FloatField(default=0)
    
    class Meta:
        unique_together = ['estudiante', 'curso']


class Quiz(models.Model):
    """Cuestionarios"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=200)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='quizzes')
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, null=True, blank=True, related_name='quizzes')
    tiempo_limite_minutos = models.IntegerField(default=30)
    intentos_maximos = models.IntegerField(default=3)
    puntaje_aprobacion = models.FloatField(default=70)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'quizzes'


class Pregunta(models.Model):
    """Preguntas de un quiz"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='preguntas')
    texto = models.TextField()
    tipo = models.CharField(max_length=20, choices=[
        ('multiple', 'Opción múltiple'),
        ('verdadero_falso', 'Verdadero/Falso'),
        ('abierta', 'Abierta'),
    ], default='multiple')
    puntos = models.IntegerField(default=1)
    
    class Meta:
        ordering = ['id']


class Opcion(models.Model):
    """Opciones de respuesta"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='opciones')
    texto = models.CharField(max_length=500)
    es_correcta = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['id']


class IntentoQuiz(models.Model):
    """Intentos de un estudiante en un quiz"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='intentos')
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='intentos_quiz')
    puntaje = models.FloatField(default=0)
    aprobado = models.BooleanField(default=False)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    completado = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-fecha_inicio']


class RespuestaQuiz(models.Model):
    """Respuestas individuales en un intento"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    intento = models.ForeignKey(IntentoQuiz, on_delete=models.CASCADE, related_name='respuestas')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion_seleccionada = models.ForeignKey(Opcion, on_delete=models.CASCADE, null=True, blank=True)
    texto_respuesta = models.TextField(blank=True)
    es_correcta = models.BooleanField(default=False)
    puntos_obtenidos = models.FloatField(default=0)


class Certificado(models.Model):
    """Certificados de finalización"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=50, unique=True)
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='certificados')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='certificados')
    fecha_emision = models.DateTimeField(auto_now_add=True)
    imagen_url = models.URLField(blank=True)
    url_verificacion = models.URLField(blank=True)
    badge_url = models.URLField(blank=True)
    hash_firma = models.CharField(max_length=64, blank=True)
    
    class Meta:
        ordering = ['-fecha_emision']


class Mensaje(models.Model):
    """Mensajes del chat"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contenido = models.TextField()
    remitente = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='mensajes_enviados')
    canal = models.CharField(max_length=50, default='general')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
