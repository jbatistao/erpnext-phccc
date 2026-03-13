#!/bin/bash
# =============================================================================
# ERPNext Backup Script → AWS S3
# Corre como root dentro del contenedor backup-s3
# bench se ejecuta como usuario 'frappe' (su frappe -c "bench ...")
# =============================================================================

set -uo pipefail   # sin -e para manejar errores manualmente y dar mensajes claros

# --- Variables (vienen de /root/backup.env inyectado por el docker-compose) ---
SITE_NAME="${FRAPPE_SITE_NAME_HEADER:-ph.puntospanama.net}"
S3_BUCKET="${S3_BUCKET:-}"
AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-}"
AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-}"
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"

BENCH_DIR="/home/frappe/frappe-bench"
SITES_DIR="$BENCH_DIR/sites"
BACKUP_DIR="$SITES_DIR/$SITE_NAME/private/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_PREFIX="[BACKUP $TIMESTAMP]"

echo "========================================================"
echo "$LOG_PREFIX Iniciando backup de ERPNext"
echo "$LOG_PREFIX Sitio     : $SITE_NAME"
echo "$LOG_PREFIX Destino S3: ${S3_BUCKET:-'(no configurado)'}"
echo "========================================================"

# --- 1. Generar backup con bench (como usuario frappe) ---
echo "$LOG_PREFIX Paso 1/4: Generando backup con bench..."

# bench está en el virtualenv de frappe, hay que ejecutarlo como ese usuario
# El contenedor corre como root, así que usamos 'su frappe -c ...'
if su frappe -c "cd $BENCH_DIR && bench --site '$SITE_NAME' backup --with-files --compress"; then
    echo "$LOG_PREFIX ✓ Backup generado correctamente"
else
    echo "$LOG_PREFIX ❌ Error generando backup con bench. Abortando."
    exit 1
fi

# --- 2. Copiar site_config.json (contiene encryption_key) ---
echo "$LOG_PREFIX Paso 2/4: Respaldando site_config.json..."
SITE_CONFIG="$SITES_DIR/$SITE_NAME/site_config.json"
if [ -f "$SITE_CONFIG" ]; then
    cp "$SITE_CONFIG" "$BACKUP_DIR/${TIMESTAMP}-site_config.json"
    echo "$LOG_PREFIX ✓ site_config.json copiado"
else
    echo "$LOG_PREFIX ⚠️  site_config.json no encontrado, omitiendo..."
fi

# --- 3. Validar credenciales S3 antes de intentar subir ---
echo "$LOG_PREFIX Paso 3/4: Subiendo archivos a S3..."

if [ -z "$S3_BUCKET" ]; then
    echo "$LOG_PREFIX ⚠️  S3_BUCKET no configurado. Los backups quedaron en: $BACKUP_DIR"
    echo "$LOG_PREFIX    Para activar la subida a S3, configura las variables en Coolify:"
    echo "$LOG_PREFIX      S3_BUCKET, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY"
    exit 0
fi

if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "$LOG_PREFIX ⚠️  Credenciales AWS no configuradas (AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY)."
    echo "$LOG_PREFIX    Backup local completado pero NO se subió a S3."
    exit 0
fi

export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION

# Subir archivos del backup de hoy
TODAY=$(date +"%Y%m%d")
FILES_UPLOADED=0

for f in "$BACKUP_DIR"/*; do
    filename=$(basename "$f")
    if [[ "$filename" == "${TODAY}"* ]] || [[ "$filename" == "${TIMESTAMP}"* ]]; then
        echo "$LOG_PREFIX   Subiendo: $filename"
        if aws s3 cp "$f" "$S3_BUCKET/$SITE_NAME/$filename" \
            --storage-class STANDARD_IA \
            --only-show-errors; then
            FILES_UPLOADED=$((FILES_UPLOADED + 1))
        else
            echo "$LOG_PREFIX   ❌ Error subiendo: $filename"
        fi
    fi
done

echo "$LOG_PREFIX ✓ $FILES_UPLOADED archivos subidos a S3"

# --- 4. Limpiar backups antiguos en S3 (retención) ---
echo "$LOG_PREFIX Paso 4/4: Limpiando backups de más de $RETENTION_DAYS días en S3..."
CUTOFF_DATE=$(date -d "$RETENTION_DAYS days ago" +"%Y-%m-%d" 2>/dev/null || echo "1970-01-01")

aws s3 ls "$S3_BUCKET/$SITE_NAME/" --recursive 2>/dev/null | while read -r line; do
    FILE_DATE=$(echo "$line" | awk '{print $1}')
    FILE_PATH=$(echo "$line" | awk '{print $4}')
    if [[ -n "$FILE_PATH" ]] && [[ "$FILE_DATE" < "$CUTOFF_DATE" ]]; then
        BUCKET_NAME=$(echo "$S3_BUCKET" | sed 's|s3://||' | cut -d'/' -f1)
        echo "$LOG_PREFIX   Eliminando antiguo: $FILE_PATH"
        aws s3 rm "s3://$BUCKET_NAME/$FILE_PATH" --only-show-errors 2>/dev/null || true
    fi
done

echo "========================================================"
echo "$LOG_PREFIX ✅ Backup completado exitosamente"
echo "$LOG_PREFIX Archivos locales en : $BACKUP_DIR"
echo "$LOG_PREFIX Archivos en S3      : $S3_BUCKET/$SITE_NAME/"
echo "========================================================"
