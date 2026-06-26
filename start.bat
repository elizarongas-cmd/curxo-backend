@echo off
echo ========================================
echo   CURXO - Iniciar Servidores
echo ========================================
echo.

:: Verificar que existe el backend
if not exist "backend\manage.py" (
    echo ERROR: No se encontro backend\manage.py
    pause
    exit /b 1
)

:: Iniciar Django backend
echo [1/2] Iniciando Django backend en http://localhost:8000...
start "CURXO Backend" cmd /c "cd backend && python manage.py runserver"

:: Esperar un momento
timeout /t 3 /nobreak >nul

:: Verificar que hay frontend para iniciar
if exist "aula_virtual_nextjs\package.json" (
    echo [2/2] Iniciando Next.js frontend en http://localhost:3000...
    start "CURXO Frontend" cmd /c "cd aula_virtual_nextjs && npm run dev"
) else (
    echo [2/2] Frontend no encontrado en aula_virtual_nextjs/
    echo       Solo backend disponible en http://localhost:8000
)

echo.
echo ========================================
echo   Servidores iniciados:
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000 (si esta disponible)
echo ========================================
echo.
echo Presiona Ctrl+C en cada ventana para detener
pause
