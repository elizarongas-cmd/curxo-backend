@echo off
echo ========================================
echo   CURXO - Detener Servidores
echo ========================================
echo.

:: Matar procesos de Python (Django)
echo Deteniendo Django backend...
taskkill /F /IM python.exe 2>nul
if errorlevel 1 (
    echo   No se encontro proceso de Python ejecutandose
) else (
    echo   Django detenido
)

:: Matar procesos de Node (Next.js)
echo Deteniendo Next.js frontend...
taskkill /F /IM node.exe 2>nul
if errorlevel 1 (
    echo   No se encontro proceso de Node ejecutandose
) else (
    echo   Next.js detenido
)

echo.
echo ========================================
echo   Todos los servidores detenidos
echo ========================================
pause
