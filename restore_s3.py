#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse

def run_cmd(cmd, check=True):
    print(f"\n> {cmd}")
    return subprocess.run(cmd, shell=True, check=check, text=True, capture_output=True)

def main():
    parser = argparse.ArgumentParser(description="Restaurar backup de ERPNext desde AWS S3")
    parser.add_argument("--timestamp", help="La fecha y hora del backup a restaurar (ej: 20260303_102214)")
    parser.add_argument("--site", help="Nombre del sitio (si no se provee, se auto-detecta)")
    parser.add_argument("--db-password", default="admin", help="Contrasena de root de la Base de Datos (default: admin)")
    
    args = parser.parse_args()

    bucket = os.environ.get("S3_BUCKET")
    if not bucket:
        print("❌ ERROR: La variable de entorno S3_BUCKET no esta configurada en este contenedor.")
        sys.exit(1)

    site_name = args.site
    if not site_name:
        site_name = os.environ.get("FRAPPE_SITE_NAME_HEADER", "").strip()

    if not site_name:
        print("❌ ERROR: No se pudo detectar el nombre del sitio. Usar --site [nombre]")
        sys.exit(1)

    # 1. Mostrar backups si no hay timestamp
    if not args.timestamp:
        print(f"=== Buscando backups disponibles para el sitio '{site_name}' en S3 ===")
        res = run_cmd(f"aws s3 ls {bucket}/{site_name}/", check=False)
        if res.returncode == 0 and res.stdout.strip():
            print("Carpetas de backup (timestamps) encontradas:")
            print(res.stdout)
            print("👉 Para restaurar uno, ejecuta:")
            print(f"python3 restore_s3.py --timestamp [NOMBRE_DE_LA_CARPETA]")
        else:
            print("❌ No se encontraron backups o error conectando a S3.")
            print(res.stderr)
        sys.exit(0)

    timestamp = args.timestamp.replace("/", "")
    s3_prefix = f"{bucket}/{site_name}/{timestamp}/"
    
    print(f"=== 📥 Descargando backup {timestamp} ===")
    res = run_cmd(f"aws s3 ls {s3_prefix}", check=False)
    if res.returncode != 0 or not res.stdout.strip():
        print(f"❌ ERROR: La ruta {s3_prefix} no existe en S3.")
        sys.exit(1)

    backup_tmp_dir = f"/tmp/restore_{timestamp}"
    os.makedirs(backup_tmp_dir, exist_ok=True)
    
    res = run_cmd(f"aws s3 cp {s3_prefix} {backup_tmp_dir}/ --recursive")
    if res.returncode != 0:
        print("❌ ERROR falló la descarga de S3.")
        sys.exit(1)

    # 2. Identificar los archivos
    db_file = None
    public_files = None
    private_files = None

    for f in os.listdir(backup_tmp_dir):
        path = os.path.join(backup_tmp_dir, f)
        if f.endswith("-database.sql.gz"):
            db_file = path
        elif f.endswith("-files.tgz") and "private-files" not in f:
            public_files = path
        elif f.endswith("-private-files.tgz"):
            private_files = path

    if not db_file:
        print("❌ ERROR: No se descargó ningún archivo -database.sql.gz desde S3.")
        sys.exit(1)

    print("\n✅ Archivos detectados:")
    print(f"  - Base de Datos: {db_file}")
    if public_files: print(f"  - Archivos Publicos: {public_files}")
    if private_files: print(f"  - Archivos Privados: {private_files}")

    # 3. Construir el comando bench restore
    print("\n=== 🔄 Iniciando Restauración (Bench Restore) ===")
    
    restore_cmd = f"bench --site {site_name} restore {db_file} --db-root-username root --db-root-password '{args.db_password}'"
    if public_files:
        restore_cmd += f" --with-public-files {public_files}"
    if private_files:
        restore_cmd += f" --with-private-files {private_files}"

    # En Docker ejecutamos bench como el usuario frappe
    bench_dir = "/home/frappe/frappe-bench"
    bash_cmd = f"cd {bench_dir} && {restore_cmd}"
    su_cmd = f"su frappe -s /bin/bash -c \"{bash_cmd}\""

    # Imprimir stdou/stderr en tiempo real
    print(f"\n> {su_cmd}")
    process = subprocess.Popen(su_cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr)
    process.communicate()

    if process.returncode == 0:
        print("\n✅ Base de datos y archivos restaurados exitosamente.")
        
        # 4. Tareas post-restore (migrate y clear-cache)
        print("\n=== ✨ Ejecutando migraciones y limpiando caché ===")
        subprocess.run(f"su frappe -s /bin/bash -c 'cd {bench_dir} && bench --site {site_name} migrate'", shell=True)
        subprocess.run(f"su frappe -s /bin/bash -c 'cd {bench_dir} && bench --site {site_name} clear-cache'", shell=True)
        
        print("\n🎉 RESTAURACIÓN COMPLETADA CON ÉXITO 🎉")
    else:
        print("\n❌ ERROR: Ocurrió un fallo durante la ejecución de bench restore.")

    # 5. Limpiar temporales
    print("\n🧹 Limpiando archivos descargados...")
    subprocess.run(f"rm -rf {backup_tmp_dir}", shell=True)
