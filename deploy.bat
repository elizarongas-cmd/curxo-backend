@echo off
echo ========================================
echo   CURXO - Deploy Firebase
echo ========================================
echo.

:: Verificar que existe el frontend
if not exist "aula_virtual_nextjs\package.json" (
    echo ERROR: No se encontro aula_virtual_nextjs\package.json
    echo Asegurate de que el frontend este en la carpeta correcta
    pause
    exit /b 1
)

:: Verificar que existe .firebaserc
if not exist ".firebaserc" (
    echo ERROR: No se encontro .firebaserc en la raiz
    echo Asegurate de estar en la carpeta C:\CURXO
    pause
    exit /b 1
)

echo [1/3] Building Next.js...
cd aula_virtual_nextjs
call npm run build
if errorlevel 1 (
    echo ERROR: Build fallo
    pause
    exit /b 1
)
cd ..

echo.
echo [2/3] Deploying a Firebase Hosting...
call firebase deploy --only hosting
if errorlevel 1 (
    echo ERROR: Deploy fallo
    pause
    exit /b 1
)

echo.
echo [3/3] Deploy completado!
echo.
echo ========================================
echo   URL: https://academia-curxo-26-47c4e.web.app
echo ========================================
pause
