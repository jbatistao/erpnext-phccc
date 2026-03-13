# Deploy

## Paso 1 - Convertir apps.json a base64

```powershell
$APPS_JSON_BASE64 = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes("C:\Users\josse\Documents\Proyectos\PHCCC\ERPNext-PHCCC\apps.json"))
```

## Paso 2 - Construir la imagen

```powershell
docker build --no-cache `
  --build-arg=FRAPPE_PATH=https://github.com/frappe/frappe `
  --build-arg=FRAPPE_BRANCH=version-15 `
  --build-arg=PYTHON_VERSION=3.12.0 `
  --build-arg=NODE_VERSION=20.19.0 `
  --build-arg=APPS_JSON_BASE64=$APPS_JSON_BASE64 `
  --tag=jbatistao/erpnext-3d-full:v15 `
  --file=images/custom/Containerfile .
```

## Paso 3 - Levantar el servicio localmente para pruebas

```bash
docker compose -f pwd.yml up -d
```

===============================================================================


# Restore desde S3

## Paso R1 - Identificar el nombre del contenedor backend

docker ps --filter "ancestor=jbatistao/erpnext-3c-full:v15" --format "table {{.Names}}\t{{.Status}}"

# Buscar el contenedor cuyo COMMAND sea gunicorn (ese es el backend)
# El nombre suele ser algo como: erpnext-phccc-backend-1

## Paso R2 - Verificar backups disponibles en S3

# Listar los timestamps disponibles para el sitio "frontend"
docker exec -it erpnext-phccc-backend-1 restore_s3.py

# Si el sitio no se detecta automaticamente, especificarlo con --site
docker exec -it erpnext-phccc-backend-1 restore_s3.py --site frontend

## Paso R3 - Detener los workers para evitar escrituras durante el restore

docker compose -f pwd.yml stop queue-long queue-short scheduler

## Paso R4 - Ejecutar el restore

# Sustituir el timestamp por el que se quiere restaurar (obtenido en Paso R2)
# El --db-password corresponde a MYSQL_ROOT_PASSWORD del pwd.yml (actualmente: admin)
docker exec -it erpnext-phccc-backend-1 restore_s3.py `
  --site frontend `
  --timestamp 20260303_102214 `
  --db-password admin

# El script descarga el backup de S3, restaura la BD y los archivos,
# luego ejecuta automaticamente: bench migrate + bench clear-cache

## Paso R5 - Reiniciar los workers

docker compose -f pwd.yml start queue-long queue-short scheduler

## Paso R6 - Verificar que el sitio responde correctamente

# Abrir http://localhost:8080 o la URL del sitio en el navegador

================================================================================

# Backup

## Paso B1 - Identificar el nombre del contenedor backend

docker ps --filter "ancestor=jbatistao/erpnext-3c-full:v15" --format "table {{.Names}}\t{{.Status}}"

# Buscar el contenedor cuyo COMMAND sea gunicorn (ese es el backend)
# El nombre suele ser algo como: erpnext-phccc-backend-1

## Paso B2 - Detener los workers para evitar escrituras durante el backup

docker compose -f pwd.yml stop queue-long queue-short scheduler

## Paso B3 - Ejecutar el backup

# El script crea un backup completo (BD + archivos) en la carpeta "sites/backup"
# y lo sube automaticamente a S3
docker exec -it erpnext-phccc-backend-1 backup_s3.py --site frontend

# Para especificar un nombre de archivo personalizado:
docker exec -it erpnext-phccc-backend-1 backup_s3.py \
  --site frontend \
  --filename "mi-backup-personalizado"

## Paso B4 - Reiniciar los workers

docker compose -f pwd.yml start queue-long queue-short scheduler

## Paso B5 - Verificar que el backup se subio correctamente

# Revisar los logs del contenedor backend para ver el mensaje de confirmacion
docker logs erpnext-phccc-backend-1 | grep "Backup completed"

# Opcional: listar los archivos en el bucket S3 para confirmar
aws s3 ls s3://erpnext-phccc/backups/frontend/

================================================================================

# Opcional: listar los archivos en el bucket S3 para confirmar

aws s3 ls s3://erpnext-phccc/backups/frontend/


