from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import (
    Usuario, Curso, Modulo, Leccion, Inscripcion,
    Quiz, Pregunta, Opcion, IntentoQuiz, RespuestaQuiz,
    Certificado, Mensaje
)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # Use email instead of username

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['rol'] = user.rol
        token['nombre'] = f"{user.first_name} {user.last_name}".strip() or user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': str(self.user.id),
            'nombre': f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username,
            'email': self.user.email,
            'rol': self.user.rol,
            'avatar': self.user.avatar if self.user.avatar else None,
        }
        return data


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 
                  'telefono', 'avatar', 'rol', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = Usuario
        fields = ['email', 'username', 'first_name', 'last_name', 
                  'telefono', 'password']
    
    def create(self, validated_data):
        user = Usuario.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            telefono=validated_data.get('telefono', ''),
            password=validated_data['password'],
            rol='estudiante'
        )
        return user


class LeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leccion
        fields = ['id', 'titulo', 'contenido', 'video_url', 'duracion_minutos', 'orden']


class ModuloSerializer(serializers.ModelSerializer):
    lecciones = LeccionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Modulo
        fields = ['id', 'titulo', 'descripcion', 'orden', 'duracion_minutos', 'lecciones']


class CursoSerializer(serializers.ModelSerializer):
    profesor_nombre = serializers.CharField(source='profesor.get_full_name', read_only=True)
    total_inscripciones = serializers.SerializerMethodField()
    total_modulos = serializers.SerializerMethodField()
    
    class Meta:
        model = Curso
        fields = ['id', 'titulo', 'descripcion', 'imagen', 'profesor',
                  'profesor_nombre', 'precio', 'duracion_horas', 'nivel',
                  'activo', 'fecha_creacion', 'fecha_actualizacion',
                  'total_inscripciones', 'total_modulos']
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
    
    def get_total_inscripciones(self, obj):
        return obj.inscripciones.count()
    
    def get_total_modulos(self, obj):
        return obj.modulos.count()


class CursoDetalleSerializer(CursoSerializer):
    modulos = ModuloSerializer(many=True, read_only=True)
    
    class Meta(CursoSerializer.Meta):
        fields = CursoSerializer.Meta.fields + ['modulos']


class InscripcionSerializer(serializers.ModelSerializer):
    curso_titulo = serializers.CharField(source='curso.titulo', read_only=True)
    estudiante_nombre = serializers.CharField(source='estudiante.get_full_name', read_only=True)
    
    class Meta:
        model = Inscripcion
        fields = ['id', 'estudiante', 'estudiante_nombre', 'curso', 
                  'curso_titulo', 'fecha_inscripcion', 'completado', 'progreso']
        read_only_fields = ['id', 'fecha_inscripcion']


class OpcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcion
        fields = ['id', 'texto', 'es_correcta']
        extra_kwargs = {'es_correcta': {'write_only': True}}


class PreguntaSerializer(serializers.ModelSerializer):
    opciones = OpcionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pregunta
        fields = ['id', 'texto', 'tipo', 'puntos', 'opciones']


class QuizSerializer(serializers.ModelSerializer):
    total_preguntas = serializers.SerializerMethodField()
    curso_titulo = serializers.CharField(source='curso.titulo', read_only=True)
    
    class Meta:
        model = Quiz
        fields = ['id', 'titulo', 'curso', 'curso_titulo', 'modulo',
                  'tiempo_limite_minutos', 'intentos_maximos', 
                  'puntaje_aprobacion', 'activo', 'total_preguntas']
    
    def get_total_preguntas(self, obj):
        return obj.preguntas.count()


class QuizDetalleSerializer(QuizSerializer):
    preguntas = PreguntaSerializer(many=True, read_only=True)
    
    class Meta(QuizSerializer.Meta):
        fields = QuizSerializer.Meta.fields + ['preguntas']


class IntentoQuizSerializer(serializers.ModelSerializer):
    quiz_titulo = serializers.CharField(source='quiz.titulo', read_only=True)
    
    class Meta:
        model = IntentoQuiz
        fields = ['id', 'quiz', 'quiz_titulo', 'estudiante', 'puntaje',
                  'aprobado', 'fecha_inicio', 'fecha_fin', 'completado']


class CertificadoSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.CharField(source='estudiante.get_full_name', read_only=True)
    curso_titulo = serializers.CharField(source='curso.titulo', read_only=True)
    
    class Meta:
        model = Certificado
        fields = ['id', 'codigo', 'estudiante', 'estudiante_nombre',
                  'curso', 'curso_titulo', 'fecha_emision', 'imagen_url',
                  'url_verificacion', 'badge_url', 'hash_firma']
        read_only_fields = ['id', 'codigo', 'fecha_emision', 'hash_firma']


class MensajeSerializer(serializers.ModelSerializer):
    remitente_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = Mensaje
        fields = ['id', 'contenido', 'remitente', 'remitente_nombre',
                  'canal', 'timestamp']
        read_only_fields = ['id', 'timestamp']
    
    def get_remitente_nombre(self, obj):
        if obj.remitente:
            return obj.remitente.get_full_name() or obj.remitente.username
        return 'Anónimo'
