from django.contrib import admin
from .models import (
    Usuario, Curso, Modulo, Leccion, Inscripcion,
    Quiz, Pregunta, Opcion, IntentoQuiz, RespuestaQuiz,
    Certificado, Mensaje
)


class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 3


class PreguntaInline(admin.StackedInline):
    model = Pregunta
    extra = 1


class LeccionInline(admin.TabularInline):
    model = Leccion
    extra = 1


class ModuloInline(admin.StackedInline):
    model = Modulo
    extra = 1


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'rol', 'date_joined']
    list_filter = ['rol', 'date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'profesor', 'nivel', 'precio', 'activo', 'fecha_creacion']
    list_filter = ['nivel', 'activo', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion']
    ordering = ['-fecha_creacion']
    inlines = [ModuloInline]


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'curso', 'orden', 'duracion_minutos']
    list_filter = ['curso']
    ordering = ['curso', 'orden']
    inlines = [LeccionInline]


@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'modulo', 'orden', 'duracion_minutos']
    list_filter = ['modulo__curso']
    ordering = ['modulo', 'orden']


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'curso', 'fecha_inscripcion', 'completado', 'progreso']
    list_filter = ['completado', 'fecha_inscripcion']
    search_fields = ['estudiante__email', 'curso__titulo']


class OpcionInlineForPregunta(admin.TabularInline):
    model = Opcion
    extra = 3


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ['texto', 'quiz', 'tipo', 'puntos']
    list_filter = ['quiz', 'tipo']
    inlines = [OpcionInlineForPregunta]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'curso', 'tiempo_limite_minutos', 'puntaje_aprobacion', 'activo']
    list_filter = ['curso', 'activo']
    inlines = [PreguntaInline]


@admin.register(IntentoQuiz)
class IntentoQuizAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'estudiante', 'puntaje', 'aprobado', 'fecha_inicio', 'completado']
    list_filter = ['aprobado', 'completado', 'fecha_inicio']
    search_fields = ['estudiante__email', 'quiz__titulo']


@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'estudiante', 'curso', 'fecha_emision']
    list_filter = ['fecha_emision']
    search_fields = ['codigo', 'estudiante__email', 'curso__titulo']
    readonly_fields = ['codigo', 'hash_firma']


@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ['contenido', 'remitente', 'canal', 'timestamp']
    list_filter = ['canal', 'timestamp']
    search_fields = ['contenido']
