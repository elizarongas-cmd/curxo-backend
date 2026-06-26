# CURXO — GUÍA COMPLETA DE ARQUITECTURA Y DESARROLLO
## Columna Vertebral del Proyecto
### Versión: 2.0 | Fecha: 25/Junio/2026

---

# PARTE I: VISIÓN DEL ECOSISTEMA CURXO

## 1.1 ¿Qué es CURXO?

CURXO es un **ecosistema digital** que ofrece tres pilares de servicios:

```
                    ┌─────────────────────────────┐
                    │         CURXO               │
                    │   Ecosistema Digital         │
                    └──────────┬──────────────────┘
                               │
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼────────┐ ┌──────▼──────┐ ┌────────▼────────┐
   │  INFRAESTRUCTURA │ │  ACADEMIA   │ │  DESARROLLO     │
   │  VPS, Hosting,   │ │  Cursos,    │ │  Software a     │
   │  Dominios        │ │  Certificados│ │  medida         │
   └─────────────────┘ └─────────────┘ └─────────────────┘
```

### Pilar 1: Infraestructura (ServiceHub)
- **VPS Cloud:** Servidores virtuales privados (Linux)
- **Hosting NVMe:** Alojamiento web de alta velocidad
- **Dominios:** Registro y gestión de +500 dominios
- **Ciberseguridad:** Auditorías, protección, monitoreo
- **Soporte IA:** Asistente inteligente 24/7

### Pilar 2: Academia (AcademyHub)
- **Cursos:** Programación, Ciberseguridad, IA, Cloud
- **Quizzes:** Evaluaciones con timer y scoring
- **Certificados:** Códigos únicos verificables
- **Progreso:** Tracking de aprendizaje por estudiante
- **Profesores:** Dashboard para crear y gestionar cursos

### Pilar 3: Desarrollo
- **Software a medida:** Apps web, móviles, sistemas
- **Cotización gratis:** Formulario de contacto
- **Portafolio:** Proyectos completados
- **Consultoría:** Asesoría técnica

---

## 1.2 Flujo de Usuario Completo

```
VISITANTE (no autenticado)
  │
  ├─ Ve landing page (Hero, ServiceHub, AcademyHub, InfiniteBanner)
  │
  ├─ Navega catálogo de cursos (/cursos)
  │
  ├─ Verifica certificados (/verificar)
  │
  └─ Se registra (/auth/registro) ──→ USAUARIO AUTENTICADO
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
              ┌─────▼─────┐        ┌──────▼──────┐       ┌─────▼─────┐
              │ ESTUDIANTE │        │  PROFESOR   │       │   ADMIN   │
              │            │        │             │       │           │
              │ - Dashboard│        │ - Dashboard │       │ - Dashboard│
              │ - Cursos   │        │ - Cursos    │       │ - Usuarios│
              │ - Quizzes  │        │ - Módulos   │       │ - Cursos  │
              │ - Certs    │        │ - Lecciones │       │ - Stats   │
              │ - Chat IA  │        │ - Quizzes   │       │ - Config  │
              │ - Perfil   │        │ - Chat      │       │           │
              └───────────┘        └─────────────┘       └───────────┘
```

---

# PARTE II: SISTEMAS Y MODELOS DE DATOS

## 2.1 Sistema de Usuarios (AUTH)

### Modelo Usuario
| Campo | Tipo | Constraints | Descripción |
|-------|------|-------------|-------------|
| id | UUID | PK, auto | Identificador único |
| email | Email | unique, indexed | Login identifier |
| username | Char(150) | unique | Auto-generado del email |
| first_name | Char(150) | — | Nombre |
| last_name | Char(150) | — | Apellido |
| telefono | Char(20) | — | Teléfono |
| avatar | URL | — | Foto de perfil |
| rol | Char(20) | choices | admin/profesor/estudiante |
| is_active | Boolean | default True | Puede iniciar sesión |
| fecha_nacimiento | Date | — | Opcional |
| fecha_registro | DateTime | auto_now_add | Cuándo se registró |

### Roles y Permisos
| Rol | Puede | No puede |
|-----|-------|----------|
| admin | CRUD todo, ver stats, gestionar usuarios | — |
| profesor | CRUD sus cursos, módulos, lecciones, quizzes | Ver otros profesores |
| estudiante | Inscribirse, ver cursos, quizzes, certificados | Crear cursos |

### Endpoints Auth
| Método | URL | Auth | Descripción |
|--------|-----|------|-------------|
| POST | `/api/auth/login/` | No | Email+password → JWT tokens |
| POST | `/api/auth/registro/` | No | Crear cuenta → JWT tokens |
| POST | `/api/auth/google/` | No | Firebase Google token → JWT |
| GET | `/api/auth/me/` | Sí | Datos usuario actual |
| POST | `/api/auth/logout/` | No | Blacklist refresh token |
| POST | `/api/auth/token/refresh/` | No | Renovar access token |

---

## 2.2 Sistema de Cursos (ACADEMIA)

### Jerarquía de Modelos
```
Curso (título, descripción, nivel, precio, imagen, profesor FK)
  │
  ├── Modulo (título, descripción, orden, curso FK)
  │     │
  │     ├── Leccion (título, contenido, tipo, duración, orden, módulo FK)
  │     │
  │     └── Quiz (título, tiempo límite, puntaje aprobación, módulo FK)
  │           │
  │           ├── Pregunta (texto, tipo, puntaje, orden, quiz FK)
  │           │     │
  │           │     └── Opcion (texto, es_correcta, pregunta FK)
  │           │
  │           ├── IntentoQuiz (estudiante, quiz, puntaje, aprobado, tiempo)
  │           │     │
  │           │     └── RespuestaQuiz (intento FK, pregunta FK, opcion FK)
  │           │
  │
  ├── Inscripcion (estudiante FK, curso FK, fecha, estado, progreso)
  │
  └── Certificado (estudiante FK, curso FK, código único, fecha emisión)
```

### Modelos Detallados

#### Curso
| Campo | Tipo | Notas |
|-------|------|-------|
| id | UUID | PK |
| titulo | Char(200) | |
| descripcion | Text | |
| nivel | Char(20) | basico/intermedio/avanzado |
| precio | Decimal(10,2) | 0 = gratuito |
| imagen | URL | Portada |
| profesor | FK→Usuario | related_name='cursos_profesor' |
| activo | Boolean | default True |
| fecha_creacion | DateTime | auto_now_add |

#### Modulo
| Campo | Tipo | Notas |
|-------|------|-------|
| id | UUID | PK |
| titulo | Char(200) | |
| descripcion | Text | |
| orden | PositiveInt | Para ordenar |
| curso | FK→Curso | related_name='modulos' |

#### Leccion
| Campo | Tipo | Notas |
|-------|------|-------|
| id | UUID | PK |
| titulo | Char(200) | |
| contenido | Text | Markdown/HTML |
| tipo | Char(20) | texto/video/ejercicio |
| duracion_min | PositiveInt | Minutos estimados |
| orden | PositiveInt | |
| modulo | FK→Modulo | related_name='lecciones' |

#### Quiz
| Campo | Tipo | Notas |
|-------|------|-------|
| id | UUID | PK |
| titulo | Char(200) | |
| tiempo_limite | PositiveInt | Minutos |
| puntaje_aprobacion | PositiveInt | Porcentaje (0-100) |
| modulo | FK→Modulo | related_name='quizzes' |

#### Pregunta
| Campo | Tipo | Notas |
|-------|------|-------|
| id | UUID | PK |
| texto | Text | |
| tipo | Char(20) | multiple_choice/verdadero_falso |
| puntaje | PositiveInt | Puntos que vale |
| orden | PositiveInt | |
| quiz | FK→Quiz | related_name='preguntas' |

#### Opcion
| Campo | Tipo | Notas |
|-------|------|-------|
| id | UUID | PK |
| texto | Char(500) | |
| es_correcta | Boolean | write_only en serializer |
| pregunta | FK→Pregunta | related_name='opciones' |

#### Inscripcion
| Campo | Tipo | Notas |
|-------|------|-------|
| id | UUID | PK |
| estudiante | FK→Usuario | |
| curso | FK→Curso | unique_together |
| fecha_inscripcion | DateTime | auto_now_add |
| estado | Char(20) | activa/completada/cancelada |
| progreso | Float | 0.0 - 100.0 |

#### Certificado
| Campo | Tipo | Notas |
|-------|------|-------|
| id | UUID | PK |
| estudiante | FK→Usuario | |
| curso | FK→Curso | |
| codigo | Char(20) | unique, auto-generado |
| fecha_emision | DateTime | auto_now_add |

### Endpoints Cursos
| Método | URL | Auth | Descripción |
|--------|-----|------|-------------|
| GET | `/api/cursos/` | No | Listar cursos (filtros: profesor, nivel, activo, buscar) |
| POST | `/api/cursos/` | Profesor/Admin | Crear curso |
| GET | `/api/cursos/{id}/` | No | Detalle curso |
| PUT | `/api/cursos/{id}/` | Profesor/Admin | Editar curso |
| DELETE | `/api/cursos/{id}/` | Admin | Eliminar curso |
| GET | `/api/cursos/{id}/modulos/` | No | Módulos del curso |
| POST | `/api/cursos/{id}/modulos/` | Profesor | Crear módulo |
| GET | `/api/inscripciones/` | Estudiante | Mis inscripciones |
| POST | `/api/inscripciones/` | Estudiante | Inscribirse a curso |
| GET | `/api/quizzes/{id}/` | Estudiante | Ver quiz |
| POST | `/api/quizzes/{id}/responder/` | Estudiante | Enviar respuestas |
| GET | `/api/certificados/` | Estudiante | Mis certificados |
| GET | `/api/verificar/{codigo}/` | No | Verificar certificado |

---

## 2.3 Sistema de Servicios (SERVICEHUB)

### Servicios Ofrecidos
| Servicio | Descripción | Precio |
|----------|-------------|--------|
| VPS Cloud | Servidor virtual privado Linux | Desde $8.99/mes |
| Hosting NVMe | Alojamiento web rápido | Con 50% OFF primer mes |
| Dominios | Registro .com, .net, .org, etc. | Desde $9.99/año |
| Desarrollo Software | Apps web/móviles a medida | Cotización gratis |
| Ciberseguridad | Auditorías y protección | Por proyecto |
| Soporte IA | Asistente inteligente 24/7 | Incluido |

### Modelo de Datos (Futuro - no implementado aún)
```
Servicio (nombre, descripción, precio, categoría, activo)
  │
  └── PedidoServicio (cliente FK, servicio FK, estado, fecha, detalles)
        │
        └── Factura (pedido FK, monto, estado, fecha_pago)
```

### Endpoints (Futuros)
| Método | URL | Auth | Descripción |
|--------|-----|------|-------------|
| GET | `/api/servicios/` | No | Listar servicios |
| POST | `/api/servicios/pedir/` | Estudiante | Solicitar servicio |
| GET | `/api/servicios/mis-pedidos/` | Estudiante | Mis pedidos |
| POST | `/api/servicios/facturar/` | Admin | Generar factura |

---

## 2.4 Sistema de Desarrollo (Futuro)

### Modelo de Datos (Futuro)
```
Proyecto (nombre, descripción, cliente FK, estado, presupuesto)
  │
  ├── TareaProyecto (título, descripción, estado, prioridad, asignado FK)
  │
  └── EntregaProyecto (proyecto FK, fecha, archivos, notas)
```

### Endpoints (Futuros)
| Método | URL | Auth | Descripción |
|--------|-----|------|-------------|
| GET | `/api/proyectos/` | Admin/Desarrollador | Listar proyectos |
| POST | `/api/proyectos/cotizar/` | No | Solicitar cotización |
| GET | `/api/proyectos/{id}/` | Admin | Detalle proyecto |

---

# PARTE III: ARQUITECTURA TÉCNICA

## 3.1 Stack Completo

| Capa | Tecnología | Versión | Hosting |
|------|-----------|---------|---------|
| Frontend | Next.js (App Router) + React 19 | 15.x | Firebase Hosting |
| Backend | Django + Django REST Framework | 6.0.6 + 3.17.1 | Railway |
| DB Local | SQLite | — | Tu PC |
| DB Prod | PostgreSQL | — | Railway PostgreSQL |
| Auth | JWT (Simple JWT) + Email backend | 5.5.1 | — |
| Google Auth | Firebase Auth (signInWithPopup) | 11.x | — |
| CSS | CSS Modules + Variables CSS | — | — |
| Deploy FE | Firebase Hosting (estático) | — | — |
| Deploy BE | Railway (contenedor) | — | — |

## 3.2 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    USUARIO (Browser)                     │
│                                                         │
│  ┌───────────────────┐    ┌───────────────────────────┐ │
│  │   Firebase Auth    │    │   Next.js Frontend        │ │
│  │   (Google Login)   │    │   (Static Export)         │ │
│  └─────────┬─────────┘    └─────────────┬─────────────┘ │
│            │                            │                │
└────────────┼────────────────────────────┼────────────────┘
             │                            │
             │ Firebase Token             │ JWT Bearer
             │                            │
┌────────────▼────────────────────────────▼────────────────┐
│                    DJANGO BACKEND                         │
│                    (Railway)                              │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Auth        │  │   ViewSets   │  │   Public     │  │
│  │   (JWT +      │  │   (CRUD      │  │   (Stats +   │  │
│  │    Google)    │  │    Cursos)   │  │    Verify)   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │            │
│  ┌──────▼─────────────────▼─────────────────▼───────┐   │
│  │              PostgreSQL Database                  │   │
│  │              (Railway PostgreSQL)                 │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

## 3.3 Variables de Entorno

### Frontend (.env.local)
```env
NEXT_PUBLIC_FIREBASE_API_KEY=AIzaSyA357uvu8AV2lGpm7l8lBfQtFbbLNqXfkg
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=academia-curxo-26-47c4e.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=academia-curxo-26-47c4e
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=academia-curxo-26-47c4e.firebasestorage.app
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=163964061849
NEXT_PUBLIC_FIREBASE_APP_ID=1:163964061849:web:c2f913d59646c81e685b6f
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Backend (.env)
```env
SECRET_KEY=tu-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://academia-curxo-26-47c4e.web.app
```

### Railway (Environment Variables)
```env
SECRET_KEY=tu-secret-key
DEBUG=False
DATABASE_URL=postgresql://postgres:KlndoEdplPauRKuDstzLtKZOrdXRNdgq@postgres.railway.internal:5432/railway
CORS_ALLOWED_ORIGINS=https://academia-curxo-26-47c4e.web.app
```

---

# PARTE IV: FASES DE DESARROLLO

## FASE 0: LIMPIEZA Y PREPARACIÓN
**Objetivo:** Eliminar basura de eras anteriores, preparar entorno limpio

### Acciones
| # | Tarea | Archivos | Estado |
|---|-------|----------|--------|
| 0.1 | Eliminar basura Era 1 (Vite+React root) | `package.json`, `src/`, `app/`, `dist/`, `node_modules/`, `index.html`, `vite.config.js`, `server.js`, `index.js` | Pendiente |
| 0.2 | Eliminar basura Era 2 (React at root) | `public/`, `assets/`, `tailwind.config.js`, `postcss.config.js` | Pendiente |
| 0.3 | Fusionar backend: copiar `token_blacklist` de `curxo-backend-temp/` → `backend/` | `academia/settings.py` | Pendiente |
| 0.4 | Copiar `seeddata.py` management command | `api/management/commands/seeddata.py` | Pendiente |
| 0.5 | Actualizar `.gitignore` (remover `seed_*.py`) | `.gitignore` | Pendiente |
| 0.6 | Crear `.env` de backend local | `backend/.env` | Pendiente |
| 0.7 | Verificar `requirements.txt` correcto | `requirements.txt` | Pendiente |

---

## FASE 1: BACKEND DJANGO (Limpio)
**Objetivo:** API REST funcional con auth JWT, CRUD cursos, certificados

### 1.1 Modelos (12 tablas)
| Modelo | Campos clave | Relaciones |
|--------|-------------|------------|
| Usuario | UUID, email, rol, avatar, telefono | — |
| Curso | titulo, nivel, precio, imagen, profesor FK | → Usuario |
| Modulo | titulo, orden, curso FK | → Curso |
| Leccion | titulo, contenido, tipo, duracion, orden, modulo FK | → Modulo |
| Quiz | titulo, tiempo_limite, puntaje_aprobacion, modulo FK | → Modulo |
| Pregunta | texto, tipo, puntaje, orden, quiz FK | → Quiz |
| Opcion | texto, es_correcta, pregunta FK | → Pregunta |
| Inscripcion | estudiante FK, curso FK, estado, progreso | → Usuario, Curso |
| IntentoQuiz | estudiante FK, quiz FK, puntaje, aprobado, tiempo | → Usuario, Quiz |
| RespuestaQuiz | intento FK, pregunta FK, opcion FK | → IntentoQuiz, Pregunta, Opcion |
| Certificado | estudiante FK, curso FK, codigo unico | → Usuario, Curso |
| Mensaje | remitente FK, contenido, canal, fecha | → Usuario |

### 1.2 Serializers (15)
| Serializer | Modelo | Notas |
|-----------|--------|-------|
| UsuarioSerializer | Usuario | Read: todos los campos. Write: password oculto |
| RegistroSerializer | Usuario | Accepts nombre, apellido, email, password, telefono |
| LoginSerializer | — | email + password |
| GoogleLoginSerializer | — | Firebase token → JWT |
| CursoSerializer | Curso | Profesor anidado (read), profesor_id (write) |
| CursoDetalleSerializer | Curso | Con módulos, lecciones, quizzes anidados |
| ModuloSerializer | Modulo | Con lecciones y quizzes |
| LeccionSerializer | Leccion | — |
| QuizSerializer | Quiz | Con preguntas y opciones (es_correcta oculto en read) |
| PreguntaSerializer | Pregunta | Con opciones |
| InscripcionSerializer | Inscripcion | Estudiante + curso anidados |
| IntentoQuizSerializer | IntentoQuiz | Con respuestas |
| CertificadoSerializer | Certificado | Con curso anidado |
| MensajeSerializer | Mensaje | — |
| EstadisticasSerializer | — | Conteos agregados |

### 1.3 Endpoints Completos
| Método | URL | Auth | Descripción |
|--------|-----|------|-------------|
| POST | `/api/auth/login/` | No | Login email+password |
| POST | `/api/auth/registro/` | No | Crear cuenta |
| POST | `/api/auth/google/` | No | Login Google |
| GET | `/api/auth/me/` | Sí | Usuario actual |
| POST | `/api/auth/logout/` | No | Cerrar sesión |
| POST | `/api/auth/token/refresh/` | No | Renovar token |
| GET/POST | `/api/cursos/` | Listar/Crear | CRUD cursos |
| GET/PUT/DELETE | `/api/cursos/{id}/` | Detalle/Editar/Eliminar | |
| GET/POST | `/api/modulos/` | Listar/Crear | CRUD módulos |
| GET/PUT/DELETE | `/api/modulos/{id}/` | Detalle/Editar/Eliminar | |
| GET/POST | `/api/lecciones/` | Listar/Crear | CRUD lecciones |
| GET/PUT/DELETE | `/api/lecciones/{id}/` | Detalle/Editar/Eliminar | |
| GET/POST | `/api/quizzes/` | Listar/Crear | CRUD quizzes |
| GET/PUT/DELETE | `/api/quizzes/{id}/` | Detalle/Editar/Eliminar | |
| GET/POST | `/api/inscripciones/` | Listar/Crear | Inscripciones |
| GET/POST | `/api/intentos-quiz/` | Listar/Crear | Intentos quiz |
| GET/POST | `/api/certificados/` | Listar/Crear | Certificados |
| GET | `/api/verificar/{codigo}/` | No | Verificar certificado |
| GET | `/api/estadisticas/` | No | Stats públicas |
| GET/POST | `/api/mensajes/` | Listar/Crear | Chat |

### 1.4 Settings Django
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',  # ← OBLIGATORIO
    'corsheaders',
    # Local
    'api',
]

AUTH_USER_MODEL = 'api.Usuario'  # ← OBLIGATORIO

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,  # ← OBLIGATORIO
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'api.backends.CookieJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
```

---

## FASE 2: FRONTEND NEXT.JS (Limpio)
**Objetivo:** SPA estática con 19 páginas, auth JWT, conexión API real

### 2.1 Estructura de Archivos
```
aula_virtual_nextjs/
├── app/
│   ├── layout.jsx              ← Root layout + Navbar
│   ├── page.js                 ← Landing (Hero, ServiceHub, AcademyHub, InfiniteBanner)
│   ├── globals.css             ← Variables CSS + reset
│   ├── auth/
│   │   ├── login/page.js       ← Login email+password + Google
│   │   ├── registro/page.js    ← Registro 2 columnas
│   │   └── recuperar/page.js   ← Recuperar contraseña
│   ├── admin/
│   │   ├── dashboard/page.js   ← Dashboard admin
│   │   ├── usuarios/page.js    ← CRUD usuarios
│   │   └── cursos/
│   │       ├── page.js         ← Lista cursos admin
│   │       ├── nuevo/page.js   ← Crear curso
│   │       └── editar/page.js  ← Editar curso
│   ├── profesor/
│   │   ├── dashboard/page.js   ← Dashboard profesor
│   │   └── cursos/page.js      ← Cursos del profesor
│   ├── estudiante/
│   │   ├── dashboard/page.js   ← Dashboard estudiante
│   │   └── certificados/page.js← Mis certificados
│   ├── cursos/
│   │   ├── page.js             ← Catálogo cursos
│   │   └── detalle/page.js     ← Detalle curso
│   ├── certificados/page.js    ← Lista certificados
│   ├── chat/page.js            ← Chat IA
│   ├── perfil/page.js          ← Editar perfil
│   └── verificar/page.js       ← Verificar certificado
├── src/
│   ├── components/
│   │   ├── Navbar.jsx          ← Navegación por rol
│   │   ├── Dashboard.jsx       ← Dashboard reutilizable
│   │   ├── Chat.jsx            ← Chat IA
│   │   ├── Quiz.jsx            ← Tomar quiz
│   │   ├── Certificado.jsx     ← Tarjeta certificado
│   │   ├── CursosList.jsx      ← Grid de cursos
│   │   ├── Perfil.jsx          ← Formulario perfil
│   │   ├── AcademyHub.jsx      ← Hub cursos landing
│   │   ├── ServiceHub.jsx      ← Hub servicios landing
│   │   └── InfiniteBanner.jsx  ← Banner métricas
│   ├── services/
│   │   └── api.js              ← API client JWT
│   ├── hooks/
│   │   └── useGoogleAuth.js    ← Hook Google login
│   ├── lib/
│   │   └── firebase.js         ← Firebase config
│   └── styles/
│       ├── globals.css         ← Variables + reset
│       ├── Home.module.css
│       ├── Login.module.css
│       ├── Registro.module.css
│       ├── Dashboard.module.css
│       ├── Navbar.module.css
│       ├── Chat.module.css
│       ├── Quiz.module.css
│       ├── CursosList.module.css
│       ├── ServiceHub.module.css
│       ├── AcademyHub.module.css
│       ├── InfiniteBanner.module.css
│       ├── AdminDashboard.module.css
│       ├── AdminUsuarios.module.css
│       ├── AdminCursos.module.css
│       ├── EstudianteDashboard.module.css
│       ├── EstudianteCertificados.module.css
│       └── Perfil.module.css
├── public/
│   ├── logo.png
│   ├── logo-white.png
│   ├── favicon.ico
│   └── images/
├── .env.local
├── next.config.mjs
├── package.json
└── firebase.json
```

### 2.2 Páginas y Descripción
| # | Ruta | Página | Descripción |
|---|------|--------|-------------|
| 1 | `/` | page.js | Landing: Hero + ServiceHub + AcademyHub + InfiniteBanner |
| 2 | `/auth/login` | page.js | Login email+password + Google |
| 3 | `/auth/registro` | page.js | Registro: nombre, email, teléfono, password |
| 4 | `/auth/recuperar` | page.js | Recuperar contraseña por email |
| 5 | `/admin/dashboard` | page.js | Dashboard admin: stats, cursos, usuarios |
| 6 | `/admin/usuarios` | page.js | CRUD usuarios con búsqueda y filtro |
| 7 | `/admin/cursos` | page.js | Lista cursos admin |
| 8 | `/admin/cursos/nuevo` | page.js | Crear curso |
| 9 | `/admin/cursos/editar` | page.js | Editar curso (?id=X) |
| 10 | `/profesor/dashboard` | page.js | Dashboard profesor: sus cursos, stats |
| 11 | `/profesor/cursos` | page.js | Cursos del profesor |
| 12 | `/estudiante/dashboard` | page.js | Dashboard estudiante: inscripciones, progreso, certs |
| 13 | `/estudiante/certificados` | page.js | Mis certificados |
| 14 | `/cursos` | page.js | Catálogo público de cursos |
| 15 | `/cursos/detalle` | page.js | Detalle de curso (?id=X) |
| 16 | `/certificados` | page.js | Lista certificados |
| 17 | `/chat` | page.js | Chat IA |
| 18 | `/perfil` | page.js | Editar perfil |
| 19 | `/verificar` | page.js | Verificar certificado (?codigo=X) |

### 2.3 Componentes Clave

#### api.js (API Client)
```javascript
// Flujo: localStorage → Bearer header → fetch → auto-refresh
const API_URL = process.env.NEXT_PUBLIC_API_URL;

const getToken = () => localStorage.getItem('access_token');

const apiRequest = async (endpoint, options = {}) => {
  const token = getToken();
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  
  let response = await fetch(`${API_URL}${endpoint}`, { ...options, headers });
  
  // Auto-refresh si token expiró
  if (response.status === 401) {
    const refreshed = await refreshToken();
    if (refreshed) {
      headers['Authorization'] = `Bearer ${localStorage.getItem('access_token')}`;
      response = await fetch(`${API_URL}${endpoint}`, { ...options, headers });
    }
  }
  return response;
};
```

#### Auth Guard (por página)
```javascript
// Patrón en cada página protegida:
'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/services/api';

export default function ProtectedPage() {
  const router = useRouter();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const userData = await api.me();
        setUser(userData);
        if (userData.rol !== 'admin') router.push('/auth/login');
      } catch {
        router.push('/auth/login');
      }
    };
    checkAuth();
  }, []);

  if (!user) return <div>Cargando...</div>;
  // ... contenido protegido
}
```

---

## FASE 3: FIREBASE (Hosting)
**Objetivo:** Deploy estático del frontend en Firebase Hosting

### 3.1 Configuración
| Archivo | Contenido |
|---------|-----------|
| `firebase.json` | `hosting: { public: 'out', rewrites: [{ source: '**', destination: '/index.html' }] }` |
| `.firebaserc` | `{ "projects": { "default": "academia-curxo-26-47c4e" } }` |
| `next.config.mjs` | `output: 'export'` (sin API routes) |

### 3.2 Deploy
```bash
# 1. Build
cd aula_virtual_nextjs
npm run build  # Genera carpeta out/

# 2. Deploy
firebase deploy --only hosting
```

### 3.3 Consideraciones
- **NO API routes:** `output: 'export'` las deshabilita
- **Rutas dinámicas:** Usar query params (`?id=X`) en vez de `[id]`
- **Static-only:** Todo el contenido es HTML/CSS/JS estático
- **CDN global:** Firebase distribuye automáticamente

---

## FASE 4: RAILWAY (Backend)
**Objetivo:** Django API en la nube con PostgreSQL

### 4.1 Configuración Railway
| Archivo | Contenido |
|---------|-----------|
| `Procfile` | `web: gunicorn academia.wsgi --bind 0.0.0.0:$PORT` |
| `railway.toml` | `startCommand: "python manage.py migrate api && python manage.py migrate && gunicorn academia.wsgi"` |
| `requirements.txt` | 8 dependencias pip |
| `.env` | Variables de entorno Railway |

### 4.2 Variables de Entorno Railway
```env
SECRET_KEY=<generate-new>
DEBUG=False
DATABASE_URL=postgresql://postgres:KlndoEdplPauRKuDstzLtKZOrdXRNdgq@postgres.railway.internal:5432/railway
CORS_ALLOWED_ORIGINS=https://academia-curxo-26-47c4e.web.app
```

### 4.3 Deploy
```bash
# 1. Push a GitHub
cd curxo-backend-temp
git add .
git commit -m "Deploy update"
git push origin main

# 2. Railway auto-deploys from GitHub
# 3. Verificar en: https://web-production-b9874.up.railway.app/api/
```

### 4.4 Migraciones (Orden Crítico)
```bash
# Railway ejecuta automáticamente:
python manage.py migrate api --noinput      # Primero: crear tablas api.*
python manage.py migrate --noinput          # Segundo: admin.0001 necesita api.Usuario
```

### 4.5 Seed Data
```bash
# Ejecutar después de cada deploy (DB se limpia):
python manage.py seeddata
```

### 4.6 Usuarios de Prueba
| Email | Password | Rol |
|-------|----------|-----|
| admin@curxo.com | admin123 | admin |
| estudiante@curxo.com | test123 | estudiante |
| profesor@curxo.com | test123 | profesor |

---

## FASE 5: INTEGRACIÓN COMPLETA
**Objetivo:** Frontend ↔ Backend funcionando end-to-end

### 5.1 Flujo de Autenticación
```
1. Usuario ingresa email + password
2. Frontend POST /api/auth/login/
3. Backend valida con EmailBackend
4. Backend retorna { user: {...}, access: "jwt...", refresh: "jwt..." }
5. Frontend guarda tokens en localStorage
6. Frontend guarda user en sessionStorage
7. Cada request incluye Authorization: Bearer <access_token>
8. Si 401 → refresh automático → retry request
```

### 5.2 Flujo de Google Login
```
1. Usuario hace click en "Continuar con Google"
2. Firebase signInWithPopup → Google ID token
3. Frontend POST /api/auth/google/ { token: "google_id_token" }
4. Backend verifica con Firebase Admin SDK
5. Backend crea/obtiene usuario → retorna JWT tokens
6. Mismo flujo que login normal
```

### 5.3 Flujo de Cursos
```
ESTUDIANTE:
1. GET /api/cursos/?activo=true → lista cursos
2. POST /api/inscripciones/ { curso_id } → inscribirse
3. GET /api/inscripciones/ → mis inscripciones
4. GET /api/modulos/?curso=X → módulos del curso
5. GET /api/lecciones/?modulo=Y → lecciones del módulo
6. GET /api/quizzes/?modulo=Y → quiz del módulo
7. POST /api/quizzes/{id}/responder/ → enviar respuestas
8. GET /api/certificados/ → mis certificados
9. GET /api/verificar/{codigo}/ → verificar certificado

PROFESOR:
1. POST /api/cursos/ → crear curso
2. POST /api/modulos/ { curso: X } → crear módulo
3. POST /api/lecciones/ { modulo: Y } → crear lección
4. POST /api/quizzes/ { modulo: Y } → crear quiz
5. POST /api/quizzes/{id}/preguntas/ → crear pregunta
6. POST /api/preguntas/{id}/opciones/ → crear opciones

ADMIN:
1. GET /api/usuarios/ → listar usuarios
2. DELETE /api/usuarios/{id}/ → eliminar usuario
3. GET /api/estadisticas/ → stats globales
4. GET /api/cursos/ → todos los cursos
5. DELETE /api/cursos/{id}/ → eliminar curso
```

---

## FASE 6: CONTENT SEEDING
**Objetivo:** Poblar la plataforma con contenido real

### 6.1 Cursos (8 iniciales)
| # | Título | Nivel | Módulos | Profesor |
|---|--------|-------|---------|----------|
| 1 | Desarrollo Full Stack 2026 | Intermedio | 5 | profesor@curxo.com |
| 2 | Ciberseguridad Ofensiva | Avanzado | 4 | profesor2@curxo.com |
| 3 | Inteligencia Artificial con Python | Intermedio | 5 | profesor@curxo.com |
| 4 | Cloud Computing AWS | Intermedio | 4 | profesor2@curxo.com |
| 5 | DevOps y CI/CD | Avanzado | 3 | profesor@curxo.com |
| 6 | React y Next.js Moderno | Básico | 4 | profesor2@curxo.com |
| 7 | bases de Datos y SQL | Básico | 3 | profesor@curxo.com |
| 8 | Administración de Servidores Linux | Intermedio | 4 | profesor2@curxo.com |

### 6.2 Módulos por Curso (ejemplo Curso 1)
| Módulo | Lecciones | Quiz |
|--------|-----------|------|
| Fundamentos HTML/CSS | 4 | Sí |
| JavaScript Moderno | 5 | Sí |
| React Básico | 4 | Sí |
| Node.js y Express | 5 | Sí |
| Proyecto Final | 3 | No |

### 6.3 Seed Script
```bash
# Management command
python manage.py seeddata
# Crea: 5 usuarios, 8 cursos, 32 módulos, 160 lecciones, 32 quizzes
```

---

## FASE 7: TESTING Y VERIFICACIÓN
**Objetivo:** Verificar que todo funciona en producción

### 7.1 Checklist de Verificación
| # | Test | URL | Esperado |
|---|------|-----|----------|
| 1 | Landing carga | `/` | Hero + ServiceHub + AcademyHub visibles |
| 2 | Login funciona | `/auth/login` | Redirige a dashboard por rol |
| 3 | Google Login | `/auth/login` | Popup Google → dashboard |
| 4 | Registro funciona | `/auth/registro` | Crea cuenta → dashboard |
| 5 | Admin dashboard | `/admin/dashboard` | Stats reales de DB |
| 6 | Admin usuarios | `/admin/usuarios` | Lista usuarios de DB |
| 7 | Admin CRUD cursos | `/admin/cursos/nuevo` | Crea curso en DB |
| 8 | Profesor dashboard | `/profesor/dashboard` | Sus cursos |
| 9 | Estudiante dashboard | `/estudiante/dashboard` | Sus inscripciones |
| 10 | Catálogo cursos | `/cursos` | Cursos de DB |
| 11 | Detalle curso | `/cursos/detalle?id=X` | Datos del curso |
| 12 | Verificar cert | `/verificar?codigo=X` | Datos certificado |
| 13 | Chat IA | `/chat` | Respuestas del bot |
| 14 | Perfil | `/perfil` | Datos usuario, guardar funciona |

### 7.2 Endpoints Test
```bash
# Login
curl -X POST https://web-production-b9874.up.railway.app/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@curxo.com","password":"admin123"}'

# Me (con token)
curl https://web-production-b9874.up.railway.app/api/auth/me/ \
  -H "Authorization: Bearer <token>"

# Cursos
curl https://web-production-b9874.up.railway.app/api/cursos/

# Stats
curl https://web-production-b9874.up.railway.app/api/estadisticas/
```

---

## FASE 8: SERVICIOS (SERVICEHUB)
**Objetivo:** Implementar sistema de servicios VPS/Hosting/Dominios

### 8.1 Modelos Nuevos
```python
class Servicio(models.Model):
    CATEGORIAS = [
        ('vps', 'VPS Cloud'),
        ('hosting', 'Hosting NVMe'),
        ('dominio', 'Dominios'),
        ('desarrollo', 'Desarrollo Software'),
        ('ciberseguridad', 'Ciberseguridad'),
        ('soporte', 'Soporte IA'),
    ]
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    imagen = models.URLField(blank=True)

class PedidoServicio(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    detalles = models.JSONField(default=dict)
    fecha_pedido = models.DateTimeField(auto_now_add=True)

class Factura(models.Model):
    pedido = models.OneToOneField(PedidoServicio, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20)  # pagada/pendiente
    fecha_pago = models.DateTimeField(null=True)
```

### 8.2 Endpoints Nuevos
| Método | URL | Auth | Descripción |
|--------|-----|------|-------------|
| GET | `/api/servicios/` | No | Listar servicios |
| GET | `/api/servicios/{id}/` | No | Detalle servicio |
| POST | `/api/pedidos/` | Estudiante | Crear pedido |
| GET | `/api/pedidos/` | Admin/Estudiante | Listar pedidos |
| PUT | `/api/pedidos/{id}/` | Admin | Actualizar estado |
| POST | `/api/facturas/` | Admin | Crear factura |

### 8.3 Páginas Nuevas
| Ruta | Descripción |
|------|-------------|
| `/servicios` | Catálogo de servicios |
| `/servicios/detalle?id=X` | Detalle del servicio |
| `/servicios/pedir?id=X` | Formulario de solicitud |
| `/admin/pedidos` | Gestión de pedidos (admin) |

---

## FASE 9: DESARROLLO SOFTWARE (FUTURO)
**Objetivo:** Sistema de proyectos y cotizaciones

### 9.1 Modelos
```python
class Proyecto(models.Model):
    ESTADOS = [
        ('cotizacion', 'Cotización'),
        ('aprobado', 'Aprobado'),
        ('en_progreso', 'En Progreso'),
        ('completado', 'Completado'),
    ]
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin_estimada = models.DateField()

class Cotizacion(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    notas = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
```

---

## FASE 10: MANTENIMIENTO CONTINUO
**Objetivo:** Monitoreo, backups, actualizaciones

### 10.1 Monitoreo
| Herramienta | Uso |
|-------------|-----|
| Railway Dashboard | Logs, métricas, uptime |
| Firebase Console | Hosting analytics, errors |
| Sentry | Error tracking (futuro) |

### 10.2 Backups
| Tipo | Frecuencia | Método |
|------|-----------|--------|
| DB PostgreSQL | Automático Railway | Snapshot diario |
| Código fuente | Cada push | GitHub |
| Firebase config | Antes de cada deploy | `firebase.json` en Git |

### 10.3 Actualizaciones
| Componente | Frecuencia | Método |
|-----------|-----------|--------|
| Dependencias npm | Mensual | `npm update` |
| Dependencias pip | Mensual | `pip install --upgrade` |
| Django | Según seguridad | `pip install django@latest` |
| Next.js | Según features | `npm install next@latest` |

---

# PARTE V: COMANDOS ESENCIALES

## Desarrollo Local
```bash
# Iniciar todo
start.bat                    # Activa .env local + inicia backend + frontend

# Solo backend
cd backend
python manage.py runserver    # localhost:8000

# Solo frontend
cd aula_virtual_nextjs
npm run dev                   # localhost:3000

# Crear superuser
python manage.py createsuperuser

# Seed data
python manage.py seeddata
```

## Deploy
```bash
# Deploy completo (auto-switches env)
deploy.bat                    # Build + Firebase deploy + restore

# Solo Firebase
cd aula_virtual_nextjs
npm run build
firebase deploy --only hosting

# Solo Railway
cd curxo-backend-temp
git add . && git commit -m "update" && git push origin main
```

## Testing
```bash
# Test login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@curxo.com","password":"admin123"}'

# Test cursos
curl http://localhost:8000/api/cursos/

# Test stats
curl http://localhost:8000/api/estadisticas/
```

---

# PARTE VI: CREDENCIALES Y URLs

## Usuarios de Prueba
| Email | Password | Rol |
|-------|----------|-----|
| admin@curxo.com | admin123 | admin |
| estudiante@curxo.com | test123 | estudiante |
| profesor@curxo.com | test123 | profesor |
| estudiante2@curxo.com | test123 | estudiante |
| profesor2@curxo.com | test123 | profesor |

## URLs de Producción
| Servicio | URL |
|----------|-----|
| Frontend | https://academia-curxo-26-47c4e.web.app |
| Backend API | https://web-production-b9874.up.railway.app/api/ |
| Backend Admin | https://web-production-b9874.up.railway.app/admin/ |

## URLs de Desarrollo
| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000/api/ |
| Backend Admin | http://localhost:8000/admin/ |

## Firebase
| Campo | Valor |
|-------|-------|
| Project ID | academia-curxo-26-47c4e |
| API Key | AIzaSyA357uvu8AV2lGpm7l8lBfQtFbbLNqXfkg |
| Auth Domain | academia-curxo-26-47c4e.firebaseapp.com |

## GitHub
| Repo | URL |
|------|-----|
| Backend | https://github.com/elizarongas-cmd/curxo-backend |

## Railway
| Campo | Valor |
|-------|-------|
| URL | https://web-production-b9874.up.railway.app |
| PostgreSQL | postgresql://postgres:KlndoEdplPauRKuDstzLtKZOrdXRNdgq@postgres.railway.internal:5432/railway |

---

# PARTE VII: BUGS CONOCIDOS Y SOLUCIONES

## Backend
| # | Bug | Solución |
|---|-----|----------|
| 1 | `token_blacklist` falta en `backend/` | Copiar de `curxo-backend-temp/` |
| 2 | `seed_*.py` en `.gitignore` | Renombrar a `seeddata.py` |
| 3 | `.env` tiene contenido TOML | Restaurar variables de entorno |
| 4 | DB Railway se limpia | Re-seed tras cada deploy |
| 5 | `DEBUG = True` en producción | Usar env var `DEBUG=False` |

## Frontend
| # | Bug | Solución |
|---|-----|----------|
| 1 | `/verificar` usa `api.verificarCertificado()` que no existe | Agregar método a api.js |
| 2 | `/chat` envía a `POST /api/chat` inexistente | Crear endpoint o remover |
| 3 | `/perfil` guarda con URL incorrecta | Corregir `${API_URL}/usuarios/` |
| 4 | No hay route protection server-side | Usar redirect client-side |
| 5 | Navbar.jsx no se importa | Importar en layout.jsx |
| 6 | Quiz.jsx existe pero no se usa | Conectar a página de quiz |
| 7 | Admin.module.css no se importa | Conectar a páginas admin |

---

# PARTE VIII: ROADMAP FUTURO

## Corto Plazo (1-2 semanas)
- [ ] Limpiar código (Fase 0)
- [ ] Backend completo con token_blacklist (Fase 1)
- [ ] Frontend sin bugs (Fase 2)
- [ ] Deploy limpio (Fases 3-4)
- [ ] Integración end-to-end (Fase 5)
- [ ] Content seeding (Fase 6)
- [ ] Testing completo (Fase 7)

## Mediano Plazo (1-2 meses)
- [ ] Sistema de servicios VPS/Hosting (Fase 8)
- [ ] Pagos con Stripe
- [ ] Email transaccional
- [ ] PWA configuration
- [ ] Analytics

## Largo Plazo (3-6 meses)
- [ ] Sistema de desarrollo software (Fase 9)
- [ ] App móvil (React Native)
- [ ] API pública documentada
- [ ] Blog/Tutoriales SEO
- [ ] Marketplace plugins

---

*Documento generado: 25/Junio/2026*
*Última actualización: 25/Junio/2026*
*Versión: 2.0*
