@echo off
setlocal
cd /d "%~dp0"
cd ..\..

echo ==========================================
echo   Ver Logs de ERPNext
echo ==========================================
echo.
echo Mostrando logs en tiempo real...
echo Presiona Ctrl+C para salir
echo.

docker compose ^
  -f compose.yaml ^
  -f overrides/compose.mariadb.yaml ^
  -f overrides/compose.redis.yaml ^
  -f overrides/compose.noproxy.yaml ^
  logs -f
