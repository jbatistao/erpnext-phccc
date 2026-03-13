# Guía de Recuperación ante Desastres: ERPNext v15

Esta guía detalla cómo restablecer completamente tu instancia de ERPNext v15 en Contabo/Coolify tras un fallo crítico, utilizando los backups automáticos almacenados en S3.

## 1. Preparación de la Infraestructura
Si el servidor fue reinstalado o Coolify fue borrado, sigue estos pasos:

1.  **Reinstalar Coolify:** Ejecuta el script de instalación oficial en tu VPS de Contabo.
2.  **Configurar Recursos Base:**
    *   Crea un nuevo proyecto en Coolify.
    *   Agrega las **Bases de Datos** (Redis Cache, Redis Queue, Redis Socketio) y **MariaDB** tal como estaban anteriormente.
    *   **IMPORTANTE:** Asegúrate de que las contraseñas de MariaDB coincidan con las que tenías (se recomienda usar `admin` para pruebas o recuperarlas de tus notas).
3.  **Configurar Variables de Entorno:**
    *   **Paso Crítico - Sincronizar Password:** Como Coolify genera un password root aleatorio al crear la base de datos MariaDB, debes:
        1. Ir a la configuración de la base de datos MariaDB en Coolify.
        2. Copiar el valor de "Root Password".
        3. Ir a la configuración de tu servicio ERPNext y pegarlo en la variable `DB_ROOT_PASSWORD`.
    *   Asegúrate de tener también:
        *   `S3_BUCKET`: Tu bucket de backups.
        *   `AWS_ACCESS_KEY_ID`: Tu access key.
        *   `AWS_SECRET_ACCESS_KEY`: Tu secret key.
    > [!IMPORTANT]
    > **Sobre las contraseñas:** El script de restauración ([restore_s3.py](file:///c:/Users/josse/Documents/Proyectos/PHCCC/ERPNext-PHCCC/restore_s3.py)) usará el valor que pongas en `--db-password` (Paso R4). Este **debe coincidir** con el password que Coolify generó para MariaDB. Si no coinciden, la restauración fallará por problemas de permisos.

## 2. Despliegue del Servicio
Utiliza el `docker-compose.yaml` (el que tienes como "funcional"). Al desplegar:

1.  El servicio `configurator` preparará los archivos `common_site_config.json`.
2.  El servicio `create-site` detectará si ya existe una configuración en el volumen. Si es una instalación de cero, creará un sitio nuevo.
    > [!NOTE]
    > No te preocupes si `create-site` crea un sitio nuevo con datos vacíos; el proceso de restauración sobrescribirá estos datos.

---

## 3. Procedimiento de Restauración (Paso a Paso)

Sigue estos comandos desde la terminal de tu servidor o mediante la consola de Coolify:

### Paso R1: Identificar el contenedor backend
Debemos entrar al contenedor que tiene el script de restauración.
```bash
docker ps --filter "name=backend"
```
*(Anota el nombre completo del contenedor, ej: `project-backend-1`)*

### Paso R2: Ver Backups Disponibles en S3
Ejecuta el script para listar las carpetas de backup (timestamps) disponibles:
```bash
docker exec -it [NOMBRE_CONTENEDOR_BACKEND] restore_s3.py --site frontend
```
Verás una lista como esta:
`20260312_171530/`
`20260313_030000/`

### Paso R3: Detener Workers
Para evitar conflictos durante la restauración, detén temporalmente los workers:
```bash
docker stop [NOMBRE_CONTENEDOR_QUEUE_LONG] [NOMBRE_CONTENEDOR_QUEUE_SHORT] [NOMBRE_CONTENEDOR_SCHEDULER]
```

### Paso R4: Ejecutar Restauración
Sustituye el `timestamp` por el que elegiste en el Paso R2:
```bash
docker exec -it [NOMBRE_CONTENEDOR_BACKEND] restore_s3.py \
  --site frontend \
  --timestamp 20260313_030000 \
  --db-password [TU_PASSWORD_ROOT]
```
> [!IMPORTANT]
> El script descargará automáticamente la base de datos y todos los archivos (públicos y privados), ejecutará `bench restore` y luego `bench migrate`.

---

## 4. Verificación y Finalización

1.  **Reiniciar Workers:**
    ```bash
    docker start [NOMBRE_CONTENEDOR_QUEUE_LONG] [NOMBRE_CONTENEDOR_QUEUE_SHORT] [NOMBRE_CONTENEDOR_SCHEDULER]
    ```
2.  **Verificar Logs:** Revisa que las migraciones terminaron sin errores:
    ```bash
    docker logs [NOMBRE_CONTENEDOR_BACKEND]
    ```
3.  **Probar Acceso:** Ingresa a tu URL (ej: `test.condadocountryclub.com`) y verifica que tus datos, usuarios y archivos adjuntos estén presentes.

---

### ¿Qué hacer si hay un error?
*   **Error de conexión a S3:** Verifica que las credenciales de AWS en el servicio de Coolify sean correctas.
*   **Error de DB Password:** Asegúrate de que `--db-password` coincida con `MARIADB_ROOT_PASSWORD` configurado en Coolify.
