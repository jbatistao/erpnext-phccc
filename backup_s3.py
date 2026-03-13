#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
import glob
from datetime import datetime

def run_cmd(cmd, check=True):
    print(f"\n> {cmd}")
    return subprocess.run(cmd, shell=True, check=check, text=True, capture_output=True)

def main():
    parser = argparse.ArgumentParser(description="Backup de ERPNext hacia AWS S3")
    parser.add_argument("--site", help="Nombre del sitio (si no se provee, se auto-detecta)")
    parser.add_argument("--filename", help="Nombre personalizado para los archivos (opcional)")
    
    args = parser.parse_args()

    # 1. Validar entorno
    bucket = os.environ.get("S3_BUCKET")
    if not bucket:
        print("❌ ERROR: La variable de entorno S3_BUCKET no esta configurada.")
        sys.exit(1)

    site_name = args.site
    if not site_name:
        site_name = os.environ.get("FRAPPE_SITE_NAME_HEADER", "").strip()

    if not site_name:
        print("❌ ERROR: No se pudo detectar el nombre del sitio. Usar --site [nombre]")
        sys.exit(1)

    print(f"=== 🚀 Iniciando Backup para el sitio: {site_name} ===")

    # 2. Ejecutar bench backup
    bench_dir = "/home/frappe/frappe-bench"
    backup_cmd = f"bench --site {site_name} backup --with-files"
    
    # Ejecutamos como usuario frappe
    su_cmd = f"su frappe -s /bin/bash -c \"cd {bench_dir} && {backup_cmd}\""
    
    res = run_cmd(su_cmd)
    if res.returncode != 0:
        print("❌ ERROR: El comando bench backup fallo.")
        print(res.stderr)
        sys.exit(1)
    
    print(res.stdout)

    # 3. Detectar archivos generados (Frappe los guarda en sitios/{site}/private/backups/)
    backup_path = f"{bench_dir}/sites/{site_name}/private/backups"
    
    # Buscamos los archivos mas recientes creados hoy
    # Usamos el patron de nombre de Frappe: YYYYMMDD_HHMMSS-site-database.sql.gz
    db_files = sorted(glob.glob(f"{backup_path}/*-database.sql.gz"), key=os.path.getmtime)
    
    if not db_files:
        print("❌ ERROR: No se encontraron los archivos de backup generados.")
        sys.exit(1)
        
    db_file = db_files[-1]
    # Extraer el timestamp del nombre del archivo (ej: 20260312_171530)
    filename_base = os.path.basename(db_file)
    timestamp = filename_base.split("-")[0]
    
    print(f"✅ Backup detectado con timestamp: {timestamp}")

    # Identificar el resto de archivos con ese mismo timestamp
    files_to_upload = glob.glob(f"{backup_path}/{timestamp}-*")
    
    if not files_to_upload:
        print(f"❌ ERROR: No se encontraron archivos para el timestamp {timestamp}")
        sys.exit(1)

    # 4. Subir a S3
    s3_target = f"{bucket}/{site_name}/{timestamp}/"
    print(f"\n=== 📤 Subiendo archivos a S3: {s3_target} ===")
    
    for f in files_to_upload:
        fname = os.path.basename(f)
        upload_cmd = f"aws s3 cp {f} {s3_target}{fname}"
        res = run_cmd(upload_cmd)
        if res.returncode == 0:
            print(f"  OK: {fname}")
        else:
            print(f"  FALLO: {fname}")
            sys.exit(1)

    # 5. Limpiar archivos locales
    print("\n🧹 Limpiando backups locales...")
    for f in files_to_upload:
        os.remove(f)
        
    # 6. Limpiar backups antiguos en S3 (Retención)
    retention_days = int(os.environ.get("RETENTION_DAYS", "30"))
    print(f"\n🗑️ Revisando retención en S3 (más de {retention_days} días)...")
    
    # Listar objetos en el prefijo del sitio
    res = run_cmd(f"aws s3 ls {bucket}/{site_name}/ --recursive", check=False)
    if res.returncode == 0:
        from datetime import datetime, timezone, timedelta
        now = datetime.now(timezone.utc)
        
        for line in res.stdout.strip().split('\n'):
            parts = line.split()
            if len(parts) >= 4:
                # El formato de ls es: 2026-03-12 17:15:30 12345 site/timestamp/file
                date_str = f"{parts[0]} {parts[1]}"
                file_path = parts[3]
                file_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                
                if now - file_date > timedelta(days=retention_days):
                    print(f"  Eliminando antiguo: {file_path}")
                    run_cmd(f"aws s3 rm s3://{bucket.replace('s3://', '')}/{file_path}", check=False)

    print("\n🎉 BACKUP COMPLETADO Y LIMPIEZA REALIZADA 🎉")

if __name__ == "__main__":
    main()
