@echo off
setlocal
cd /d "%~dp0"
cd ..\..

echo ==========================================
echo   Detener ERPNext Local
echo ==========================================

docker compose ^
  -f compose.yaml ^
  -f overrides/compose.mariadb.yaml ^
  -f overrides/compose.redis.yaml ^
  -f overrides/compose.noproxy.yaml ^
  down

if %ERRORLEVEL% equ 0 (
    echo.
    echo [EXITO] Contenedores detenidos correctamente
) else (
    echo.
    echo [ERROR] Hubo un error al detener los contenedores
)

echo ==========================================
pause
