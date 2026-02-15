# Guía de Despliegue en Producción: ERPNext en Contabo con Coolify

Esta guía te llevará paso a paso para desplegar ERPNext en un VPS de Contabo usando Ubuntu 24.04 LTS y Coolify.

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Preparación del VPS](#preparación-del-vps)
3. [Instalación de Coolify](#instalación-de-coolify)
4. [Configuración de Dominio y DNS](#configuración-de-dominio-y-dns)
5. [Despliegue de ERPNext](#despliegue-de-erpnext)
6. [Creación del Sitio ERPNext](#creación-del-sitio-erpnext)
7. [Configuración SSL](#configuración-ssl)
8. [Backups Automáticos](#backups-automáticos)
9. [Monitoreo y Mantenimiento](#monitoreo-y-mantenimiento)
10. [Troubleshooting](#troubleshooting)

---

## 📋 Requisitos Previos

### Hardware Mínimo Recomendado (Contabo VPS)
- **CPU**: 4 vCores o más
- **RAM**: 8 GB mínimo (16 GB recomendado)
- **Almacenamiento**: 100 GB SSD
- **Ancho de banda**: Ilimitado (típico en Contabo)

**Plan recomendado**: VPS M (8 GB RAM, 4 vCores) o superior

### Software y Servicios
- ✅ VPS Contabo con Ubuntu 24.04 LTS
- ✅ Dominio propio (ej: `erp.miempresa.com`)
- ✅ Acceso SSH root al VPS
- ✅ Cliente SSH (PuTTY en Windows, Terminal en Mac/Linux)

---

## 🖥️ Preparación del VPS

### Paso 1: Contratar VPS en Contabo

1. Ve a [Contabo.com](https://contabo.com/)
2. Selecciona **VPS** → Elige plan (mínimo VPS M)
3. Configuración:
   - **OS**: Ubuntu 24.04 LTS
   - **Región**: Elige la más cercana a tus usuarios
   - **Opciones adicionales**: 
     - ✅ Habilita backups automáticos (recomendado)
     - ✅ Considera añadir almacenamiento extra si manejarás muchos archivos

4. Completa el pago y espera el email con:
   - IP del servidor
   - Usuario root
   - Contraseña inicial

### Paso 2: Conectarte al VPS vía SSH

**Windows (PowerShell o CMD):**
```bash
ssh root@TU_IP_DEL_VPS
```

**Linux/Mac (Terminal):**
```bash
ssh root@TU_IP_DEL_VPS
```

Acepta el fingerprint y ingresa la contraseña que recibiste por email.

### Paso 3: Actualizar el Sistema

```bash
# Actualizar repositorios
apt update && apt upgrade -y

# Reiniciar si hay actualizaciones del kernel
reboot
```

Espera 1-2 minutos y vuelve a conectarte.

### Paso 4: Configurar Firewall Básico

```bash
# Instalar UFW (Uncomplicated Firewall)
apt install ufw -y

# Permitir SSH
ufw allow 22/tcp

# Permitir HTTP y HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Habilitar firewall
ufw enable

# Verificar estado
ufw status
```

### Paso 5: Configurar Hostname

```bash
# Establecer hostname descriptivo
hostnamectl set-hostname erpnext-production

# Editar /etc/hosts
nano /etc/hosts
```

Añade esta línea (reemplaza con tu IP y dominio):
```
TU_IP_DEL_VPS    erpnext-production erp.tudominio.com
```

Guarda (`Ctrl+O`, `Enter`, `Ctrl+X`).

---

## 🚀 Instalación de Coolify

Coolify simplifica enormemente el despliegue de aplicaciones Docker con interfaz web.

### Paso 1: Requisitos Previos de Coolify

```bash
# Instalar curl si no está
apt install curl -y

# Verificar que tienes al menos 2 GB de RAM
free -h
```

### Paso 2: Instalar Coolify

```bash
# Comando de instalación oficial
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
```

Este script instalará automáticamente:
- ✅ Docker Engine
- ✅ Docker Compose
- ✅ Coolify y sus dependencias

**Tiempo estimado**: 5-10 minutos

### Paso 3: Acceder a Coolify

1. Abre tu navegador
2. Ve a: `http://TU_IP_DEL_VPS:8000`
3. **Primera configuración**:
   - Crea un usuario administrador
   - Establece contraseña segura
   - Completa el wizard de configuración inicial

### Paso 4: Configurar Email (Opcional pero Recomendado)

En Coolify, ve a:
- **Settings** → **Email Settings**
- Configura SMTP para notificaciones:
  - Gmail, SendGrid, Mailgun, etc.
  - Útil para alertas de errores y notificaciones

---

## 🌐 Configuración de Dominio y DNS

### Paso 1: Configurar Registros DNS

En tu proveedor de dominio (ej: Namecheap, GoDaddy, Cloudflare), añade estos registros:

**Registro A:**
```
Tipo: A
Nombre: erp (o @ si es dominio principal)
Valor: TU_IP_DEL_VPS
TTL: 300 o automático
```

**Opcional - Registro AAAA (IPv6):**
Si Contabo te dio una IPv6:
```
Tipo: AAAA
Nombre: erp
Valor: TU_IPv6_DEL_VPS
TTL: 300
```

### Paso 2: Verificar Propagación DNS

```bash
# Desde tu computadora local (no el VPS)
nslookup erp.tudominio.com

# O usar herramienta online
# https://dnschecker.org
```

Espera 5-30 minutos para propagación completa.

---

## 🐳 Despliegue de ERPNext

### Opción A: Despliegue con Coolify (Recomendado)

#### Paso 1: Crear Proyecto en Coolify

1. En Coolify, ve a **Projects** → **+ New Project**
2. Nombre: `ERPNext Production`
3. Guarda

#### Paso 2: Añadir Servicio Docker Compose

1. Dentro del proyecto, click **+ New Resource**
2. Selecciona **Docker Compose**
3. Configuración:
   - **Name**: `erpnext-stack`
   - **Git Repository**: Opcional (o pega compose directo)
   - **Domain**: `erp.tudominio.com`

#### Paso 3: Configurar Docker Compose

En Coolify, pega este `docker-compose.yml` optimizado para producción:

```yaml
services:
  configurator:
    image: frappe/erpnext:v16.5.0
    restart: "no"
    entrypoint:
      - bash
      - -c
    command:
      - >
        ls -1 apps > sites/apps.txt;
        bench set-config -g db_host $$DB_HOST;
        bench set-config -gp db_port $$DB_PORT;
        bench set-config -g redis_cache "redis://$$REDIS_CACHE";
        bench set-config -g redis_queue "redis://$$REDIS_QUEUE";
        bench set-config -g redis_socketio "redis://$$REDIS_QUEUE";
        bench set-config -gp socketio_port $$SOCKETIO_PORT;
    environment:
      DB_HOST: db
      DB_PORT: "3306"
      REDIS_CACHE: redis-cache:6379
      REDIS_QUEUE: redis-queue:6379
      SOCKETIO_PORT: "9000"
    volumes:
      - sites:/home/frappe/frappe-bench/sites
    depends_on:
      db:
        condition: service_healthy
      redis-cache:
        condition: service_started
      redis-queue:
        condition: service_started

  backend:
    image: frappe/erpnext:v16.5.0
    restart: unless-stopped
    volumes:
      - sites:/home/frappe/frappe-bench/sites
    depends_on:
      configurator:
        condition: service_completed_successfully

  frontend:
    image: frappe/erpnext:v16.5.0
    restart: unless-stopped
    command:
      - nginx-entrypoint.sh
    environment:
      BACKEND: backend:8000
      SOCKETIO: websocket:9000
      FRAPPE_SITE_NAME_HEADER: $$host
      UPSTREAM_REAL_IP_ADDRESS: 127.0.0.1
      UPSTREAM_REAL_IP_HEADER: X-Forwarded-For
      UPSTREAM_REAL_IP_RECURSIVE: "off"
      PROXY_READ_TIMEOUT: 120
      CLIENT_MAX_BODY_SIZE: 50m
    volumes:
      - sites:/home/frappe/frappe-bench/sites
    depends_on:
      - backend
      - websocket
    labels:
      - "coolify.managed=true"
      - "traefik.enable=true"
      - "traefik.http.routers.erpnext.rule=Host(\`erp.tudominio.com\`)"
      - "traefik.http.routers.erpnext.entrypoints=websecure"
      - "traefik.http.routers.erpnext.tls.certresolver=letsencrypt"
      - "traefik.http.services.erpnext.loadbalancer.server.port=8080"

  websocket:
    image: frappe/erpnext:v16.5.0
    restart: unless-stopped
    command:
      - node
      - /home/frappe/frappe-bench/apps/frappe/socketio.js
    volumes:
      - sites:/home/frappe/frappe-bench/sites
    depends_on:
      configurator:
        condition: service_completed_successfully

  queue-short:
    image: frappe/erpnext:v16.5.0
    restart: unless-stopped
    command: bench worker --queue short,default
    volumes:
      - sites:/home/frappe/frappe-bench/sites
    depends_on:
      configurator:
        condition: service_completed_successfully

  queue-long:
    image: frappe/erpnext:v16.5.0
    restart: unless-stopped
    command: bench worker --queue long,default,short
    volumes:
      - sites:/home/frappe/frappe-bench/sites
    depends_on:
      configurator:
        condition: service_completed_successfully

  scheduler:
    image: frappe/erpnext:v16.5.0
    restart: unless-stopped
    command: bench schedule
    volumes:
      - sites:/home/frappe/frappe-bench/sites
    depends_on:
      configurator:
        condition: service_completed_successfully

  db:
    image: mariadb:11.8
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "healthcheck.sh", "--connect", "--innodb_initialized"]
      start_period: 5s
      interval: 5s
      timeout: 5s
      retries: 5
    command:
      - --character-set-server=utf8mb4
      - --collation-server=utf8mb4_unicode_ci
      - --skip-character-set-client-handshake
      - --skip-innodb-read-only-compressed
      - --max-connections=500
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_PASSWORD}
      MARIADB_AUTO_UPGRADE: 1
    volumes:
      - db-data:/var/lib/mysql

  redis-cache:
    image: redis:6.2-alpine
    restart: unless-stopped

  redis-queue:
    image: redis:6.2-alpine
    restart: unless-stopped
    volumes:
      - redis-queue-data:/data

volumes:
  sites:
  db-data:
  redis-queue-data:
```

#### Paso 4: Configurar Variables de Entorno

En Coolify, sección **Environment Variables**, añade:

```env
DB_PASSWORD=TU_CONTRASEÑA_MYSQL_SEGURA_AQUI
ERPNEXT_VERSION=v16.5.0
```

**Genera contraseña segura:**
```bash
openssl rand -base64 32
```

#### Paso 5: Deploy

1. Click **Deploy**
2. Coolify descargará las imágenes y levantará los servicios
3. Monitorea los logs en tiempo real

**Tiempo estimado**: 5-10 minutos primera vez

---

### Opción B: Despliegue Manual (Sin Coolify)

Si prefieres no usar Coolify, puedes desplegar manualmente:

#### Paso 1: Instalar Docker

```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Habilitar Docker al inicio
systemctl enable docker
systemctl start docker

# Verificar
docker --version
```

#### Paso 2: Clonar el Proyecto

```bash
cd /opt
git clone https://github.com/frappe/frappe_docker.git
cd frappe_docker
```

#### Paso 3: Configurar Variables

```bash
cp example.env .env
nano .env
```

Edita:
```env
ERPNEXT_VERSION=v16.5.0
DB_PASSWORD=TU_CONTRASEÑA_MYSQL_SEGURA
LETSENCRYPT_EMAIL=tu@email.com
SITES_RULE=Host(`erp.tudominio.com`)
```

#### Paso 4: Levantar Servicios

```bash
docker compose \
  -f compose.yaml \
  -f overrides/compose.mariadb.yaml \
  -f overrides/compose.redis.yaml \
  -f overrides/compose.https.yaml \
  up -d
```

---

## 🏗️ Creación del Sitio ERPNext

Una vez que los servicios estén corriendo (con Coolify o manual):

### Paso 1: Acceder al Contenedor Backend

**Con Coolify:**
```bash
# Encuentra el nombre del contenedor
docker ps | grep backend

# Accede al contenedor
docker exec -it NOMBRE_CONTENEDOR_BACKEND bash
```

**Sin Coolify:**
```bash
docker compose exec backend bash
```

### Paso 2: Crear el Sitio

```bash
# Dentro del contenedor
bench new-site erp.tudominio.com \
  --mariadb-root-password=TU_DB_PASSWORD \
  --admin-password=TU_ADMIN_PASSWORD_SEGURO \
  --install-app erpnext \
  --set-default

# Habilitar scheduler
bench --site erp.tudominio.com scheduler enable

# Verificar instalación
bench --site erp.tudominio.com list-apps
```

### Paso 3: Configurar Multitenancy (Opcional)

Si quieres soportar múltiples sitios:

```bash
# Dentro del contenedor
bench config dns_multitenant on
```

En este caso, ERPNext usará el dominio del `Host` header para identificar el sitio.

---

## 🔒 Configuración SSL

### Con Coolify (Automático)

Coolify maneja SSL automáticamente con Let's Encrypt:

1. En Coolify, ve a tu servicio
2. **Settings** → **Domains**
3. Asegúrate que `erp.tudominio.com` esté configurado
4. Marca **Enable SSL** o **Force HTTPS**
5. Coolify generará el certificado automáticamente

### Sin Coolify (Manual con Certbot)

```bash
# Instalar Certbot
apt install certbot python3-certbot-nginx -y

# Obtener certificado
certbot --nginx -d erp.tudominio.com

# Renovación automática (crontab)
crontab -e
```

Añade:
```cron
0 3 * * * certbot renew --quiet
```

---

## 💾 Backups Automáticos

### Opción 1: Backups con Script Personalizado

```bash
# Crear directorio de backups
mkdir -p /opt/erpnext-backups

# Crear script de backup
nano /opt/erpnext-backups/backup.sh
```

Contenido del script:

```bash
#!/bin/bash
BACKUP_DIR="/opt/erpnext-backups"
SITE="erp.tudominio.com"
DATE=$(date +%Y%m%d_%H%M%S)
CONTAINER_NAME=$(docker ps --filter name=backend --format "{{.Names}}" | head -n 1)

# Backup de base de datos y archivos
docker exec $CONTAINER_NAME bench --site $SITE backup \
  --with-files \
  --backup-path /home/frappe/frappe-bench/sites/$SITE/private/backups

# Copiar backup al host
docker cp $CONTAINER_NAME:/home/frappe/frappe-bench/sites/$SITE/private/backups \
  $BACKUP_DIR/$DATE/

# Comprimir
cd $BACKUP_DIR
tar -czf backup_${DATE}.tar.gz $DATE/
rm -rf $DATE/

# Limpiar backups antiguos (mantener últimos 30 días)
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +30 -delete

echo "Backup completado: backup_${DATE}.tar.gz"
```

Hacer ejecutable:
```bash
chmod +x /opt/erpnext-backups/backup.sh
```

### Opción 2: Programar Backups Diarios

```bash
crontab -e
```

Añade:
```cron
# Backup diario a las 2 AM
0 2 * * * /opt/erpnext-backups/backup.sh >> /var/log/erpnext-backup.log 2>&1
```

### Opción 3: Backups Remotos con Rclone

```bash
# Instalar rclone
curl https://rclone.org/install.sh | bash

# Configurar (ej: Google Drive, S3, Dropbox)
rclone config

# Script de sync
nano /opt/erpnext-backups/sync-remote.sh
```

```bash
#!/bin/bash
# Sincronizar backups a la nube
rclone sync /opt/erpnext-backups remote:erpnext-backups \
  --progress \
  --transfers 4 \
  --checkers 8
```

---

## 📊 Monitoreo y Mantenimiento

### Monitoreo de Recursos

**Con Coolify:**
- Dashboard integrado muestra uso de CPU, RAM, disco
- Configurar alertas en **Settings** → **Notifications**

**Sin Coolify:**
```bash
# Ver uso de recursos
docker stats

# Ver logs de un servicio
docker compose logs -f backend

# Ver estado de servicios
docker compose ps
```

### Herramientas de Monitoreo Avanzado (Opcional)

**Instalar Netdata:**
```bash
bash <(curl -Ss https://my-netdata.io/kickstart.sh)
```

Accede a `http://TU_IP:19999` para dashboard en tiempo real.

### Actualizaciones de ERPNext

```bash
# 1. Backup antes de actualizar
/opt/erpnext-backups/backup.sh

# 2. Actualizar imágenes
docker compose pull

# 3. Recrear contenedores
docker compose up -d

# 4. Migrar sitio
docker compose exec backend bench --site erp.tudominio.com migrate
```

---

## 🔧 Troubleshooting

### Problema: Sitio no carga (502 Bad Gateway)

**Diagnóstico:**
```bash
# Ver logs del frontend
docker compose logs frontend

# Ver logs del backend
docker compose logs backend

# Verificar que todos los servicios estén "Up"
docker compose ps
```

**Soluciones comunes:**
- Esperar 2-3 minutos después del deploy inicial
- Reiniciar backend: `docker compose restart backend`
- Verificar que el sitio fue creado correctamente

---

### Problema: Base de datos no conecta

**Diagnóstico:**
```bash
# Ver logs de MariaDB
docker compose logs db

# Verificar health check
docker inspect CONTAINER_ID_DB | grep Health -A 10
```

**Soluciones:**
- Verificar contraseña en `.env` coincide con la usada en `bench new-site`
- Verificar que el volumen `db-data` tiene permisos correctos
- Reiniciar servicio: `docker compose restart db`

---

### Problema: SSL no funciona

**Diagnóstico:**
```bash
# Verificar certificado
certbot certificates

# Ver logs de renovación
tail -f /var/log/letsencrypt/letsencrypt.log
```

**Soluciones:**
- Verificar DNS apunta correctamente
- Verificar puertos 80 y 443 abiertos: `ufw status`
- Forzar renovación: `certbot renew --force-renewal`

---

### Problema: Sluggish performance

**Diagnóstico:**
```bash
# Ver uso de recursos
docker stats

# Ver procesos dentro del contenedor
docker exec BACKEND_CONTAINER top
```

**Soluciones:**
- Aumentar RAM del VPS
- Optimizar MariaDB: Aumentar `max-connections`, `innodb_buffer_pool_size`
- Considerar Redis persistente para cache

---

## 📚 Recursos Adicionales

- [Documentación oficial frappe_docker](https://github.com/frappe/frappe_docker)
- [Documentación ERPNext](https://docs.erpnext.com/)
- [Foros de la comunidad Frappe](https://discuss.frappe.io/)
- [Coolify Documentation](https://coolify.io/docs)
- [Contabo Support](https://contabo.com/support/)

---

## ✅ Checklist Final

Antes de considerar el despliegue completo:

- [ ] VPS configurado y actualizado
- [ ] Firewall configurado (puertos 22, 80, 443)
- [ ] DNS configurado y propagado
- [ ] Coolify instalado y accesible
- [ ] ERPNext desplegado y servicios corriendo
- [ ] Sitio creado y accesible
- [ ] SSL habilitado (HTTPS funcionando)
- [ ] Backups automáticos configurados
- [ ] Monitoreo configurado
- [ ] Credenciales guardadas en lugar seguro

---

## 🎉 ¡Felicidades!

Tu instancia de ERPNext ahora está en producción y lista para usar.

**Próximos pasos:**
1. Configura tu empresa en ERPNext
2. Importa datos iniciales (productos, clientes, etc.)
3. Configura usuarios y permisos
4. Personaliza según tus necesidades

**Recuerda:**
- Cambia las contraseñas por defecto
- Configura backups remotos
- Monitorea regularmente el servidor
- Mantén ERPNext actualizado

---

*¿Necesitas ayuda?* Consulta los recursos adicionales o contacta al soporte de la comunidad Frappe.
