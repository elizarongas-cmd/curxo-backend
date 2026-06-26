# BITÁCORA DEL SISTEMA AULA VIRTUAL
## Migración: PHP (Indutech) → Next.js + Django + Firebase (CURXO)

### Fecha de Inicio: 24 de Junio de 2026
### Estado: EN PROCESO

---

## 1. SISTEMA ACTUAL (PHP)

### 1.1 Arquitectura
- **Stack:** PHP 8.4 + MySQL (MariaDB 10.6) + Bootstrap 5.3 + jQuery
- **Base de datos:** 16+ tablas
- **Roles:** Admin, Profesor, Estudiante
- **Ubicación:** `C:\CURXO\aula\AlianzaHerith_JXMU\aula_virtual\`

### 1.2 Funcionalidades Existentes
| Categoría | Funcionalidades |
|-----------|-----------------|
| Auth | Login, registro, recuperar contraseña, tokens |
| Admin | CRUD usuarios, cursos, contenidos, quizzes, certificados |
| Profesor | Ver cursos, calificar tareas, chat |
| Estudiante | Explorar cursos, inscribirse, quizzes, certificados, perfil |
| Chat | AJAX polling, indicadores, notificaciones sonoras |
| Certificados | HTML dinámico, QR, verificación pública |
| Quizzes | Opción múltiple, autocorrección, límite intentos |

---

## 2. SISTEMA NUEVO (Next.js + Django + Firebase)

### 2.1 Stack
| Componente | Tecnología |
|------------|------------|
| Frontend | Next.js 15 (App Router) + React 19 |
| Backend | Django 6 + Django REST Framework |
| Base de datos | SQLite (local) + Firebase Firestore (nube) |
| Autenticación | JWT (Simple JWT) + Email-based |
| CSS | CSS Modules + Variables CSS |
| Hosting | Firebase Hosting (estático) |
| Almacenamiento | Firebase Storage |

### 2.2 Colores
| Variable | Hex | Uso |
|----------|-----|-----|
| `--primary-400` | `#38bdf8` | Acento principal |
| `--primary-500` | `#0284c7` | Botones primarios |
| `--primary-800` | `#1e3a5f` | Fondos oscuros |
| `--slate-800` | `#1e293b` | Tarjetas/paneles |
| `--slate-900` | `#0f172a` | Fondo página |

---

## 3. FASES COMPLETADAS

### FASE 1: CSS Unificado ✅ (24/06/2026)
- 13 archivos CSS Modules
- global.css con variables y reset

### FASE 2: Estructura Proyecto ✅ (24/06/2026)
- Next.js 15 App Router, `output: 'export'`
- .env.local con Firebase credentials

### FASE 3: Django Backend ✅ (24/06/2026)
- 10 modelos: Usuario, Curso, Modulo, Leccion, Inscripcion, Quiz, Pregunta, Opcion, IntentoQuiz, Certificado, Mensaje
- JWT auth con CustomTokenObtainPairSerializer (email-based)
- CustomEmailBackend para login por email
- Endpoints: login, registro, me, logout, CRUD ViewSets

### FASE 4: Componentes React ✅ (24/06/2026)
- Navbar, Dashboard, Chat, Quiz, Certificado, CursosList, Perfil

### FASE 5: Certificados ✅ (24/06/2026)
- API route para generación PNG + QR
- Chat API con FAQ 12 preguntas

### FASE 6: Git y Docs ✅ (24/06/2026)
- Branches: main, develop, feature/*

### FASE 7: Páginas ✅ (24/06/2026)
- 19 páginas: auth, admin, profesor, estudiante, cursos, chat, perfil, certificados, verificar

### FASE 8: JWT Auth ✅ (24-25/06/2026)
- simplejwt configurado
- Login con email funcional
- Test users creados

### FASE 9: Landing Page ✅ (25/06/2026)
- Hero, features, cursos destacados, CTA, footer

### FASE 10: Servidores ✅ (25/06/2026)
- start.bat, stop.bat, deploy.bat
- Fix de puertos y rutas

### FASE 11: API Service ✅ (25/06/2026)
- src/services/api.js con JWT token management

### FASE 12: ServiceHub + AcademyHub ✅ (25/06/2026)
- ServiceHub (izquierdo): VPS, Hosting, Dominios, Desarrollo, Ciberseguridad, Soporte IA
- AcademyHub (derecho): Cursos, Programación, Ciberseguridad, IA, Quizzes, Certificados
- Auto-open 10s → compacto píldora con cycling cada 5s
- InfiniteBanner: métricas + scroll infinito tecnologías
- Registro "Modo Pro": layout 2 columnas, iconos en inputs
- Firebase Auth removido (causaba popup de permisos)

---

## 4. ROADMAP - LO QUE SE TIENE vs LO QUE FALTA

### 🔴 PRIORIDAD ALTA (Hacer primero)

| # | Tarea | Estado | Notas |
|---|-------|--------|-------|
| 1 | Fix registro → apuntar a Django API | ✅ | Error "Unexpected token <" por route inexistente |
| 2 | Google Login | 🔲 | Firebase Auth en login + registro |
| 3 | Poblar cursos reales en Django | 🔲 | 8-12 cursos con módulos e imágenes |
| 4 | Conectar páginas al API Django | 🔲 | Admin, Profesor, Estudiante → fetch real |
| 5 | Desplegar Django backend | 🔲 | Railway o Render para producción |
| 6 | CRUD cursos admin funcional | 🔲 | Crear, editar, eliminar contra Django |

### 🟡 PRIORIDAD MEDIA (Después)

| # | Tarea | Estado | Notas |
|---|-------|--------|-------|
| 7 | Sistema de inscripciones | 🔲 | Estudiante se inscribe → "Mis Cursos" |
| 8 | Quizzes funcionales | 🔲 | Crear, tomar, calificar desde Django |
| 9 | Certificados reales | 🔲 | Generar PNG + QR al completar curso |
| 10 | Chat en tiempo real | 🔲 | WebSocket o polling mejorado |
| 11 | Email transaccional | 🔲 | Nodemailer o Resend |
| 12 | Iconos sociales landing | 🔲 | WhatsApp, Telegram, YouTube, TikTok |

### 🟢 PRIORIDAD BAJA (Cuando haya tiempo)

| # | Tarea | Estado | Notas |
|---|-------|--------|-------|
| 13 | PWA configuration | 🔲 | Service worker, manifest, offline |
| 14 | Tests unitarios | 🔲 | Jest + React Testing Library |
| 15 | Analytics | 🔲 | Google Analytics o Plausible |
| 16 | SEO optimization | 🔲 | Meta tags, sitemap, robots.txt |
| 17 | Blog/Tutoriales | 🔲 | MDX para SEO |

### 💡 IDEAS NUEVAS (Futuro)

| # | Idea | Complejidad | Descripción |
|---|------|-------------|-------------|
| 18 | Panel de Control VPS | Alta | Dashboard para gestionar servidores |
| 19 | Billing/Pagos | Alta | Integración Stripe |
| 20 | Marketplace plugins | Media | Vender plugins ecosistema CURXO |
| 21 | Programa afiliados | Media | Links de referido con comisiones |
| 22 | AI Tutor personalizado | Media | Ollama local o OpenAI |
| 23 | LMS completo | Alta | Progreso, hitos, rutas de aprendizaje |
| 24 | API pública | Baja | Documentación Swagger |
| 25 | App móvil | Alta | React Native o Capacitor |

---

## 5. ESTRUCTURA DEL PROYECTO

```
C:\CURXO\
├── aula\AlianzaHerith_JXMU\    ← PHP original (NO tocar)
├── backend\                     ← Django backend
│   ├── manage.py
│   ├── academia/settings.py
│   ├── api/models.py (10 modelos)
│   ├── api/serializers.py
│   ├── api/views.py (JWT + CRUD)
│   ├── api/urls.py
│   ├── api/backends.py (EmailBackend)
│   └── api/admin.py
├── aula_virtual_nextjs\         ← Next.js frontend
│   ├── app/                     ← 19 páginas
│   ├── src/components/          ← 11+ componentes
│   ├── src/services/api.js      ← API client JWT
│   ├── src/styles/              ← 14 CSS modules
│   ├── src/lib/firebase.js
│   ├── out/                     ← Build estático
│   ├── start.bat
│   ├── stop.bat
│   └── deploy.bat
├── BITACORA_AULA.md             ← Este archivo
└── public/                      ← Proyecto viejo
```

---

## 6. GIT

```
main                    ← Producción
├── develop             ← Desarrollo (ACTUAL)
│   ├── feature/css
│   ├── feature/auth
│   ├── feature/django
│   ├── feature/certs
│   ├── feature/landing
│   ├── feature/hubs
│   └── feature/contenido  ← NUEVO: poblar cursos/servicios
└── hotfix/*
```

---

## 7. COMANDOS ÚTILES

```bash
start.bat              # Iniciar servidores
stop.bat               # Detener servidores
deploy.bat             # Build + deploy
firebase deploy --only hosting
cd backend && python manage.py runserver
```

---

## 8. DEPLOY

| Servicio | URL | Estado |
|----------|-----|--------|
| Firebase Hosting | https://academia-curxo-26-47c4e.web.app | ACTIVO |
| Django Backend | http://localhost:8000/api | LOCAL |

---

*Última actualización: 25 de Junio de 2026*
