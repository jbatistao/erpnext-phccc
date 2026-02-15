# Comandos Útiles para ERPNext en Producción

Referencia rápida de comandos frecuentemente usados para administrar ERPNext en producción.

## 🔍 Información del Sistema

### Ver estado de servicios
```bash
docker compose ps
```

### Ver uso de recursos
```bash
docker stats
```

### Ver versión de ERPNext
```bash
docker compose exec backend bench version
```

### Listar sitios
```bash
docker compose exec backend bench --site all list-sites
```

### Ver apps instaladas en un sitio
```bash
docker compose exec backend bench --site NOMBRE_SITIO list-apps
```

---

## 📊 Monitoreo y Logs

### Ver logs en tiempo real
```bash
# Todos los servicios
docker compose logs -f

# Solo backend
docker compose logs -f backend

# Solo base de datos
docker compose logs -f db

# Últimas 100 líneas
docker compose logs --tail=100 backend
```

### Ver logs de ERPNext dentro del contenedor
```bash
docker compose exec backend tail -f /home/frappe/frappe-bench/logs/web.error.log
docker compose exec backend tail -f /home/frappe/frappe-bench/logs/worker.error.log
```

---

## 🔄 Reiniciar Servicios

### Reiniciar todos los servicios
```bash
docker compose restart
```

### Reiniciar servicio específico
```bash
docker compose restart backend
docker compose restart frontend
docker compose restart db
```

### Reiniciar con rebuild (después de cambios en configuración)
```bash
docker compose up -d --force-recreate
```

---

## 💾 Backups

### Backup manual
```bash
# Dentro del contenedor backend
docker compose exec backend bench --site NOMBRE_SITIO backup --with-files
```

### Listar backups disponibles
```bash
docker compose exec backend ls -lh /home/frappe/frappe-bench/sites/NOMBRE_SITIO/private/backups/
```

### Descargar backup al host
```bash
docker cp CONTAINER_NAME:/home/frappe/frappe-bench/sites/NOMBRE_SITIO/private/backups/ ./backups-$(date +%Y%m%d)
```

### Restaurar desde backup
```bash
docker compose exec backend bench --site NOMBRE_SITIO restore \
  --mariadb-root-password CONTRASEÑA \
  /path/to/backup.sql.gz \
  --with-private-files /path/to/files.tar \
  --with-public-files /path/to/public.tar
```

---

## 🔧 Mantenimiento

### Limpiar bench cache
```bash
docker compose exec backend bench --site NOMBRE_SITIO clear-cache
```

### Reconstruir índices de búsqueda
```bash
docker compose exec backend bench --site NOMBRE_SITIO rebuild-global-search
```

### Migrar después de actualización
```bash
docker compose exec backend bench --site NOMBRE_SITIO migrate
```

### Optimizar base de datos
```bash
docker compose exec db mysqlcheck -u root -p --optimize --all-databases
```

---

## 👥 Gestión de Usuarios

### Crear usuario admin
```bash
docker compose exec backend bench --site NOMBRE_SITIO add-system-manager usuario@email.com
```

### Resetear contraseña de usuario
```bash
docker compose exec backend bench --site NOMBRE_SITIO set-admin-password NUEVA_PASSWORD
```

### Listar usuarios
```bash
docker compose exec backend bench --site NOMBRE_SITIO console
```
Luego en la consola Python:
```python
frappe.get_all('User', fields=['name', 'email', 'enabled'])
```

---

## 📦 Gestión de Apps

### Instalar nueva app en un sitio
```bash
docker compose exec backend bench --site NOMBRE_SITIO install-app nombre_app
```

### Desinstalar app
```bash
docker compose exec backend bench --site NOMBRE_SITIO uninstall-app nombre_app
```

### Actualizar app específica
```bash
docker compose exec backend bench update --apps nombre_app
```

---

## 🔄 Actualizaciones

### Actualizar ERPNext (imágenes Docker)
```bash
# 1. Hacer backup primero
docker compose exec backend bench --site NOMBRE_SITIO backup --with-files

# 2. Descargar nuevas imágenes
docker compose pull

# 3. Recrear contenedores
docker compose up -d

# 4. Migrar base de datos
docker compose exec backend bench --site NOMBRE_SITIO migrate
```

### Ver cambios pendientes de migración
```bash
docker compose exec backend bench --site NOMBRE_SITIO migrate --dry-run
```

---

## 🗄️ Base de Datos

### Acceder a MySQL/MariaDB
```bash
docker compose exec db mysql -u root -p
```

### Backup manual de base de datos
```bash
docker compose exec db mysqldump -u root -p NOMBRE_DB > backup_$(date +%Y%m%d).sql
```

### Ver tamaño de bases de datos
```bash
docker compose exec db mysql -u root -p -e "SELECT table_schema AS 'Database', ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)' FROM information_schema.TABLES GROUP BY table_schema;"
```

---

## 🐛 Debugging

### Entrar en consola Python de Frappe
```bash
docker compose exec backend bench --site NOMBRE_SITIO console
```

### Activar modo debug
```bash
docker compose exec backend bench --site NOMBRE_SITIO set-config developer_mode 1
docker compose restart backend
```

### Desactivar modo debug
```bash
docker compose exec backend bench --site NOMBRE_SITIO set-config developer_mode 0
docker compose restart backend
```

### Ver configuración del sitio
```bash
docker compose exec backend cat /home/frappe/frappe-bench/sites/NOMBRE_SITIO/site_config.json
```

### Ver errores recientes
```bash
docker compose exec backend bench --site NOMBRE_SITIO show-config
docker compose exec backend bench --site NOMBRE_SITIO mariadb
```

---

## 📈 Performance

### Ver procesos en ejecución
```bash
docker compose exec backend bench doctor
```

### Ver cola de trabajos
```bash
docker compose exec backend bench --site NOMBRE_SITIO show-pending-jobs
```

### Limpiar trabajos fallidos
```bash
docker compose exec backend bench --site NOMBRE_SITIO purge-jobs --event all
```

### Ver estadísticas de uso
```bash
docker compose exec backend bench --site NOMBRE_SITIO console
```
```python
from frappe.utils import get_system_managers
print(get_system_managers())
```

---

## 🔒 Seguridad

### Cambiar contraseña de admin
```bash
docker compose exec backend bench --site NOMBRE_SITIO set-admin-password NUEVA_PASSWORD
```

### Ver intentos de login fallidos
```bash
docker compose exec backend bench --site NOMBRE_SITIO mariadb
```
```sql
SELECT * FROM `tabActivity Log` WHERE status = 'Failed' ORDER BY creation DESC LIMIT 50;
```

### Habilitar autenticación de dos factores
En ERPNext UI: Usuario → Preferencias → Two Factor Auth

---

## 🌐 Configuración de Dominio

### Cambiar dominio del sitio
```bash
# 1. Añadir nuevo dominio
docker compose exec backend bench --site VIEJO_DOMINIO add-to-hosts NUEVO_DOMINIO

# 2. Actualizar DNS a nivel de sistema
docker compose exec backend bench setup add-domain NUEVO_DOMINIO --site VIEJO_DOMINIO
```

### Ver dominios configurados
```bash
docker compose exec backend cat /home/frappe/frappe-bench/sites/currentsite.txt
```

---

## 🔢 Scheduler

### Habilitar/deshabilitar scheduler
```bash
# Habilitar
docker compose exec backend bench --site NOMBRE_SITIO scheduler enable

# Deshabilitar
docker compose exec backend bench --site NOMBRE_SITIO scheduler disable

# Ver estado
docker compose exec backend bench --site NOMBRE_SITIO scheduler status
```

### Ver trabajos programados
```bash
docker compose exec backend bench --site NOMBRE_SITIO show-pending-jobs
```

---

## 📧 Email

### Probar configuración de email
```bash
docker compose exec backend bench --site NOMBRE_SITIO send-test-email usuario@ejemplo.com
```

### Ver cola de emails pendientes
```bash
docker compose exec backend bench --site NOMBRE_SITIO console
```
```python
frappe.get_all('Email Queue', fields=['*'], filters={'status': 'Not Sent'})
```

---

## 🧹 Limpieza

### Limpiar archivos temporales
```bash
docker compose exec backend bench --site NOMBRE_SITIO clear-cache
docker compose exec backend bench --site NOMBRE_SITIO clear-website-cache
```

### Limpiar logs viejos
```bash
docker compose exec backend find /home/frappe/frappe-bench/logs -name "*.log" -mtime +30 -delete
```

### Limpiar Docker (imágenes no usadas)
```bash
docker system prune -a
```

---

## 📦 Volúmenes Docker

### Ver volúmenes
```bash
docker volume ls
```

### Inspeccionar volumen
```bash
docker volume inspect NOMBRE_VOLUMEN
```

### Backup de volumen
```bash
docker run --rm -v NOMBRE_VOLUMEN:/data -v $(pwd):/backup ubuntu tar czf /backup/volumen-backup.tar.gz /data
```

---

## 🔍 Aliases Útiles (Añadir a ~/.bashrc)

```bash
# Añadir estos aliases para comandos más rápidos
alias dc='docker compose'
alias dcl='docker compose logs -f'
alias dps='docker compose ps'
alias drestart='docker compose restart'
alias bench-exec='docker compose exec backend bench'
alias bench-console='docker compose exec backend bench --site NOMBRE_SITIO console'
alias bench-migrate='docker compose exec backend bench --site NOMBRE_SITIO migrate'
alias bench-backup='docker compose exec backend bench --site NOMBRE_SITIO backup --with-files'
```

Aplicar cambios:
```bash
source ~/.bashrc
```

---

## 🚨 Comandos de Emergencia

### Sitio no responde - Reinicio completo
```bash
docker compose down
docker compose up -d
```

### Base de datos corrupta - Reparar tablas
```bash
docker compose exec db mysqlcheck -u root -p --auto-repair --all-databases
```

### Espacio en disco lleno
```bash
# Ver uso de disco
df -h

# Limpiar logs de Docker
docker system prune -a --volumes

# Limpiar logs de ERPNext
docker compose exec backend find /home/frappe/frappe-bench/logs -name "*.log" -delete
```

### Restaurar desde último backup automático
```bash
# 1. Detener servicios
docker compose stop backend frontend websocket

# 2. Restaurar
docker compose exec backend bench --site NOMBRE_SITIO restore /ruta/al/ultimo/backup.sql.gz

# 3. Reiniciar
docker compose start backend frontend websocket
```

---

## 📝 Notas Importantes

- Siempre hacer backup antes de operaciones críticas
- Probar comandos en entorno de desarrollo primero
- Documentar cambios de configuración
- Monitorear logs después de cambios importantes
- Mantener credenciales en lugar seguro

---

*Última actualización: Febrero 2026*
