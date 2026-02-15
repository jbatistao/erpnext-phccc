@echo off
setlocal
cd /d "%~dp0"
cd ..\..

echo ==========================================
echo   Crear Sitio ERPNext
echo ==========================================

set /p SITE_NAME="Nombre del sitio (ej: erp.local o localhost): "
set /p ADMIN_PASS="Contraseña de admin (dejar vacio para 'admin'): "

if "%ADMIN_PASS%"=="" set ADMIN_PASS=admin

echo.
echo [INFO] Creando sitio: %SITE_NAME%
echo [INFO] Contraseña admin: %ADMIN_PASS%
echo.

docker compose -f compose.yaml ^
  -f overrides/compose.mariadb.yaml ^
  -f overrides/compose.redis.yaml ^
  -f overrides/compose.noproxy.yaml ^
  exec backend bench new-site %SITE_NAME% ^
  --mariadb-root-password=123 ^
  --admin-password=%ADMIN_PASS% ^
  --install-app erpnext ^
  --set-default

if %ERRORLEVEL% equ 0 (
    echo.
    echo [EXITO] Sitio creado exitosamente
    echo [INFO] Accede a: http://localhost:8080
    echo [INFO] Usuario: Administrator
    echo [INFO] Contraseña: %ADMIN_PASS%
) else (
    echo.
    echo [ERROR] Hubo un error al crear el sitio
)

echo ==========================================
pause
