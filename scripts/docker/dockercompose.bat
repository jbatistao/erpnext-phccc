@echo off
setlocal
:: Cambiar al directorio donde se encuentra el script
cd /d "%~dp0"
:: Subir dos niveles para llegar a la raiz del proyecto
cd ..\..

echo ==========================================
echo   Levantando ERPNext Local (Docker)
echo ==========================================

:: Verificar si existe el archivo .env, si no, crearlo desde example.env
if not exist .env (
    echo [INFO] No se encontro el archivo .env. Creando uno desde example.env...
    copy example.env .env
)

echo [INFO] Ejecutando docker compose con configuracion de desarrollo local...
echo [INFO] - Base: compose.yaml
echo [INFO] - MariaDB local: overrides/compose.mariadb.yaml
echo [INFO] - Redis local: overrides/compose.redis.yaml
echo [INFO] - Acceso directo (sin proxy): overrides/compose.noproxy.yaml
docker compose -f compose.yaml -f overrides/compose.mariadb.yaml -f overrides/compose.redis.yaml -f overrides/compose.noproxy.yaml up -d

if %ERRORLEVEL% equ 0 (
    echo.
    echo [EXITO] Los contenedores se estan ejecutando correctamente.
    echo [INFO] Puedes revisar los logs con: docker compose logs -f
) else (
    echo.
    echo [ERROR] Hubo un fallo al intentar levantar los servicios.
    echo [INFO] Asegurate de que Docker Desktop este iniciado.
)

echo ==========================================
pause
