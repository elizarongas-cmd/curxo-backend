# ARCHITECTURE.md — CURXO Academy
## Documento Maestro de Arquitectura
### Fecha: 25/Junio/2026

---

## 1. STACK TECNOLÓGICO

| Capa | Tecnología | Versión | Hosting |
|------|-----------|---------|---------|
| Frontend | Next.js (App Router) + React 19 | 15.x | Firebase Hosting (estático) |
| Backend | Django + Django REST Framework | 6.0.6 + 3.17.1 | Railway |
| DB Local | SQLite | — | Tu PC |
| DB Prod | PostgreSQL | — | Railway PostgreSQL |
| Auth | JWT (Simple JWT) + Email backend | 5.5.1 | — |
| Google Auth | Firebase Auth (signInWithPopup) | 11.x | — |
| Estilos | CSS Modules + Variables CSS | — | — |

### URLs Activas
- **Frontend (producción):** https://academia-curxo-26-47c4e.web.app
- **Backend (producción):** https://web-production-b9874.up.railway.app/api/
- **Backend (local):** http://localhost:8000/api
- **Frontend (local):** http://localhost:3000

---

## 2. DISEÑO VISUAL

### Paleta de Colores
| Variable | Hex | Uso |
|----------|-----|-----|
| `--primary-400` | `#38bdf8` | Acento principal, links |
| `--primary-500` | `#0284c7` | Botones primarios |
| `--primary-600` | `#0369a1` | Hover botones |
| `--primary-800` | `#1e3a5f` | Fondos oscuros |
| `--slate-50` | `#f8fafc` | Texto principal |
| `--slate-800` | `#1e293b` | Tarjetas/paneles |
| `--slate-900` | `#0f172a` | Fondo página |
| `--purple-500` | `#8b5cf6` | AcademyHub, mensajes bienvenida |
| `--success-400` | `#4ade80` | Estados activos, pass quizzes |
| `--error-400` | `#f87171` | Errores, eliminar |

### Tema: Dark mode forzado (slate-900 de fondo)

---

## 3. MODELOS DE DATOS (Django)

### Jerarquía de Relaciones
```
Usuario (UUID PK, email login, 3 roles: admin/profesor/estudiante)
  ├── Curso.profesor (FK)
  │     ├── Modulo.curso
  │     │     ├── Leccion.modulo
  │     │     ├── Quiz.modulo (nullable)
  │     ├── Quiz.curso
  │     │     ├── Pregunta.quiz
  │     │     │     └── Opcion.pregunta (es_correcta write_only)
  │     │     ├── IntentoQuiz.quiz
  │     │     │     └── RespuestaQuiz.intento
  │     ├── Inscripcion.curso (unique_together: estudiante+curso)
  │     └── Certificado.curso
  ├── Inscripcion.estudiante
  ├── IntentoQuiz.estudiante
  ├── Certificado.estudiante
  └── Mensaje.remitente (SET_NULL)
```

### Modelo Usuario (AbstractUser extendido)
| Campo | Tipo | Notas |
|-------|------|-------|
| id | UUID PK | uuid4 auto-generado |
| email | EmailField | unique=True, usado para login |
| username | CharField | unique, auto-generado del email |
| first_name, last_name | CharField | |
| telefono | CharField(20) | |
| avatar | URLField | |
| rol | CharField | estudiante/profesor/admin |
| USERNAME_FIELD | — | 'email' |

### 12 Modelos Totales
Usuario, Curso, Modulo, Leccion, Inscripcion, Quiz, Pregunta, Opcion, IntentoQuiz, RespuestaQuiz, Certificado, Mensaje

---

## 4. BACKEND — ENDPOINTS COMPLETOS

### Auth
| Método | URL | Auth | Descripción |
|--------|-----|------|-------------|
| POST | `/api/auth/login/` | No | Login por email+password → tokens JWT |
| POST | `/api/auth/registro/` | No | Crear cuenta estudiante → tokens JWT |
| POST | `/api/auth/google/` | No | Login/registro via Firebase Google |
| GET | `/api/auth/me/` | Sí | Datos del usuario actual |
| POST | `/api/auth/logout/` | No | Cerrar sesión, blacklist refresh token |
| POST | `/api/auth/token/refresh/` | No | Renovar access token usando refresh cookie |

### CRUD (ViewSets con DRF Router)
| Prefijo | Modelo | Filtros |
|---------|--------|---------|
| `/api/cursos/` | Curso | `?profesor=`, `?nivel=`, `?activo=`, `?buscar=` |
| `/api/modulos/` | Modulo | `?curso=` |
| `/api/lecciones/` | Leccion | `?modulo=` |
| `/api/inscripciones/` | Inscripcion | `?estudiante=`, `?curso=` |
| `/api/quizzes/` | Quiz | — |
| `/api/intentos-quiz/` | IntentoQuiz | `?quiz=`, `?estudiante=` |
| `/api/certificados/` | Certificado | `?estudiante=` (solo GET/POST) |
| `/api/mensajes/` | Mensaje | `?canal=` |

### Públicos
| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/api/estadisticas/` | Conteos: cursos, estudiantes, profesores, inscripciones, certificados |
| GET | `/api/verificar/<codigo>/` | Verificar certificado por código único |

### Auth Flow (Dual)
1. **Bearer Header:** `Authorization: Bearer <access_token>` (principal, cross-origin)
2. **HttpOnly Cookie:** `access_token` cookie (fallback same-origin)
3. **CookieJWTAuthentication** intenta header primero, luego cookie

### JWT Config
- Access token: 60 minutos
- Refresh token: 7 días (se rota en cada refresh)
- Algoritmo: HS256
- Custom claims en token: email, rol, nombre

---

## 5. FRONTEND — PÁGINAS (19)

### Auth (4 páginas)
| Ruta | Página | Descripción |
|------|--------|-------------|
| `/` | page.js | Landing con Hero, ServiceHub, AcademyHub, InfiniteBanner |
| `/auth/login` | page.js | Login email+password + Google |
| `/auth/registro` | page.js | Registro con nombre, email, teléfono, password |
| `/auth/recuperar` | page.js | Recuperar contraseña por email |

### Admin (4 páginas)
| Ruta | Página | Descripción |
|------|--------|-------------|
| `/admin/dashboard` | page.js | Dashboard admin con estadísticas |
| `/admin/usuarios` | page.js | CRUD usuarios con búsqueda y filtro |
| `/admin/cursos` | page.js | Lista de cursos con búsqueda |
| `/admin/cursos/nuevo` | page.js | Crear curso |
| `/admin/cursos/editar` | page.js | Editar curso (?id=X) |

### Profesor (2 páginas)
| Ruta | Página | Descripción |
|------|--------|-------------|
| `/profesor/dashboard` | page.js | Dashboard profesor con sus cursos |
| `/profesor/cursos` | page.js | Lista de cursos del profesor |

### Estudiante (2 páginas)
| Ruta | Página | Descripción |
|------|--------|-------------|
| `/estudiante/dashboard` | page.js | Dashboard con inscripciones, progreso, certificados |
| `/estudiante/certificados` | page.js | Mis certificados |

### Públicas (6 páginas)
| Ruta | Página | Descripción |
|------|--------|-------------|
| `/cursos` | page.js | Catálogo de cursos con filtros |
| `/cursos/detalle` | page.js | Detalle de curso (?id=X) |
| `/certificados` | page.js | Lista de certificados |
| `/chat` | page.js | Chat IA |
| `/perfil` | page.js | Editar perfil |
| `/verificar` | page.js | Verificar certificado público (?codigo=X) |

### Componentes (10)
| Componente | Props | Estado |
|-----------|-------|--------|
| AcademyHub | — | auto-open, cycling announcements |
| ServiceHub | — | auto-open, cycling announcements |
| InfiniteBanner | — | métricas + scroll infinito |
| Navbar | usuario | role-based nav, logout |
| Dashboard | usuario, cursos | greeting, stats, courses grid |
| Chat | usuario, mensajes | send/receive messages |
| CursosList | cursos[] | grid de tarjetas de curso |
| Certificado | certificado, onDescargar | card con código, fecha, badge |
| Perfil | usuario, onGuardar | form editable |
| Quiz | quiz, onCompletar | timer, questions, scoring |

---

## 6. BUGS CONOCIDOS

### Backend
1. `rest_framework_simplejwt.token_blacklist` falta en `backend/` (sí está en `curxo-backend-temp/`)
2. `seed_*.py` está en `.gitignore` — management commands no se subían a git
3. `.env` en `curxo-backend-temp/` tiene contenido TOML en vez de variables de entorno
4. DB Railway se limpia en cada deploy (no tiene persistencia configurada)
5. `DEBUG = True` por defecto (debería ser False en Railway)

### Frontend
1. `/verificar` llama `api.verificarCertificado()` que NO existe en api.js
2. `/chat` envía a `POST /api/chat` que NO existe (no hay app/api/)
3. `/perfil` guarda con URL incorrecta (`/api/usuarios/` en vez de `${API_URL}/usuarios/`)
4. No hay route protection server-side (solo redirect client-side con localStorage)
5. Navbar.jsx no se importa por ninguna página (cada página crea su nav inline)
6. Quiz.jsx existe pero ninguna página lo renderiza
7. Admin.module.css no se importa por nada
8. No hay loading states consistentes

---

## 7. ESTRUCTURA DE ARCHIVOS ACTUAL

```
C:\CURXO\
├── aula\AlianzaHerith_JXMU\     ← PHP original (NO tocar)
├── backend\                      ← Django LOCAL (el que editamos)
│   ├── manage.py
│   ├── academia/settings.py      ← FALTA token_blacklist
│   ├── api/
│   │   ├── models.py             ← 12 modelos UUID
│   │   ├── serializers.py        ← 15 serializers
│   │   ├── views.py              ← Auth + ViewSets
│   │   ├── urls.py               ← Router + auth endpoints
│   │   ├── backends.py           ← EmailBackend + CookieJWTAuthentication
│   │   ├── admin.py              ← Config completa
│   │   ├── firebase_sync.py      ← OBSOLETO (usa modelos viejos)
│   │   └── migrations/           ← 2 migrations (0001 + 0002)
│   ├── requirements.txt          ← 8 dependencias
│   ├── Procfile
│   ├── seed_completo.py          ← Seed con módulos/lecciones
│   └── seed_cursos.py            ← Seed simple
├── curxo-backend-temp\           ← Django DEPLOY (copia separada en GitHub)
│   ├── .git/                     ← repo: github.com/elizarongas-cmd/curxo-backend
│   ├── railway.toml              ← startCommand + releaseCommand
│   ├── academia/settings.py      ← CON token_blacklist
│   ├── api/management/commands/seeddata.py  ← Management command
│   └── (resto idéntico a backend/)
├── aula_virtual_nextjs\          ← Next.js FRONTEND
│   ├── app/                      ← 19 páginas (todas 'use client')
│   ├── src/components/           ← 10 componentes
│   ├── src/services/api.js       ← API client JWT
│   ├── src/hooks/useGoogleAuth.js
│   ├── src/styles/               ← 15 CSS modules + globals.css
│   ├── src/lib/firebase.js
│   ├── next.config.mjs           ← output: 'export' (static)
│   ├── .env.local                ← NEXT_PUBLIC_API_URL=localhost:8000/api
│   └── firebase.json             ← hosting: out/
├── data/                         ← Legacy: db.json, faq.json
├── BITACORA_AULA.md              ← Documentación completa
├── start.bat                     ← Inicia ambos servidores
├── deploy.bat                    ← Build + deploy Firebase
└── .env                          ← Legacy Vite config
```

---

## 8. DIFERENCIAS BACKEND (backend/ vs curxo-backend-temp/)

| Aspecto | backend/ (local) | curxo-backend-temp/ (deploy) |
|---------|-----------------|---------------------------|
| token_blacklist | FALTA | SÍ |
| management commands | No | seeddata.py |
| railway.toml | No | SÍ |
| db.sqlite3 | SÍ (activo) | No |
| .git | No (parte del root) | SÍ (repo separado) |
| .env | No | SÍ (misfiled) |

---

## 9. CREDENCIALES

### Usuarios de Prueba
| Email | Password | Rol |
|-------|----------|-----|
| admin@curxo.com | admin123 | admin |
| estudiante@curxo.com | test123 | estudiante |
| profesor@curxo.com | test123 | profesor |
| estudiante2@curxo.com | test123 | estudiante |
| profesor2@curxo.com | test123 | profesor |

### Firebase Project
- Project ID: `academia-curxo-26-47c4e`
- API Key: `AIzaSyA357uvu8AV2lGpm7l8lBfQtFbbLNqXfkg`

### Railway
- URL: `https://web-production-b9874.up.railway.app`
- PostgreSQL: `postgresql://postgres:KlndoEdplPauRKuDstzLtKZOrdXRNdgq@postgres.railway.internal:5432/railway`
- GitHub repo: `https://github.com/elizarongas-cmd/curxo-backend`

---

*Última actualización: 25/Junio/2026*
