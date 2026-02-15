# Scripts Docker para ERPNext

Esta carpeta contiene scripts para facilitar el desarrollo local de ERPNext usando Docker.

## Arquitectura

El proyecto usa el enfoque recomendado de **compose.yaml base + overrides** que replica la estructura de producción:

- **Base**: `compose.yaml` - Servicios de aplicación ERPNext
- **Override MariaDB**: `overrides/compose.mariadb.yaml` - Base de datos local
- **Override Redis**: `overrides/compose.redis.yaml` - Cache y colas local
- **Override No Proxy**: `overrides/compose.noproxy.yaml` - Acceso directo puerto 8080

## Scripts Disponibles

### 1. `dockercompose.bat` - Iniciar servicios
Levanta todos los contenedores necesarios (MariaDB, Redis, ERPNext).

```bash
.\scripts\docker\dockercompose.bat
```

**Nota**: Este script NO crea el sitio automáticamente, solo levanta la infraestructura.

### 2. `create-site.bat` - Crear nuevo sitio
Crea un nuevo sitio ERPNext. Ejecutar solo después de `dockercompose.bat`.

```bash
.\scripts\docker\create-site.bat
```

Te pedirá:
- Nombre del sitio (ej: `localhost`, `erp.local`)
- Contraseña de admin (por defecto: `admin`)

**Credenciales por defecto del sitio:**
- Usuario: `Administrator`
- Contraseña: la que ingreses (o `admin` si la dejas vacía)

### 3. `stop.bat` - Detener servicios
Detiene todos los contenedores sin eliminar datos.

```bash
.\scripts\docker\stop.bat
```

### 4. `logs.bat` - Ver logs
Muestra los logs de todos los contenedores en tiempo real.

```bash
.\scripts\docker\logs.bat
```

## Flujo de Trabajo

### Primera vez (Setup inicial)

1. **Levantar servicios**:
   ```bash
   .\scripts\docker\dockercompose.bat
   ```

2. **Crear sitio** (esperar ~30 segundos a que MariaDB esté listo):
   ```bash
   .\scripts\docker\create-site.bat
   ```
   - Ingresa nombre: `localhost`
   - Contraseña: `admin` (o la que prefieras)

3. **Acceder a ERPNext**:
   - URL: http://localhost:8080
   - Usuario: `Administrator`
   - Contraseña: la que configuraste

### Uso diario

**Iniciar** (después de reiniciar PC):
```bash
.\scripts\docker\dockercompose.bat
```

**Detener** (al terminar el día):
```bash
.\scripts\docker\stop.bat
```

**Ver logs** (si hay problemas):
```bash
.\scripts\docker\logs.bat
```

## Variables de Entorno

El archivo `.env` se crea automáticamente desde `example.env` si no existe.

Variables principales:
- `ERPNEXT_VERSION`: Versión de ERPNext (ej: `v16.5.0`)
- `DB_PASSWORD`: Contraseña root de MariaDB (por defecto: `123`)
- `HTTP_PUBLISH_PORT`: Puerto de acceso (por defecto: `8080`)

## Comandos Útiles

### Ejecutar comandos bench
```bash
docker compose -f compose.yaml -f overrides/compose.mariadb.yaml -f overrides/compose.redis.yaml -f overrides/compose.noproxy.yaml exec backend bench [comando]
```

Ejemplos:
```bash
# Listar aplicaciones instaladas
docker compose [...] exec backend bench --site localhost list-apps

# Habilitar/deshabilitar scheduler
docker compose [...] exec backend bench --site localhost scheduler enable
docker compose [...] exec backend bench --site localhost scheduler disable

# Consola IPython
docker compose [...] exec backend bench --site localhost console

# Actualizar aplicaciones
docker compose [...] exec backend bench --site localhost migrate
```

### Ver estado de contenedores
```bash
docker compose -f compose.yaml -f overrides/compose.mariadb.yaml -f overrides/compose.redis.yaml -f overrides/compose.noproxy.yaml ps
```

### Reiniciar un servicio específico
```bash
docker compose [...] restart backend
docker compose [...] restart frontend
```

## Solución de Problemas

### Error: Connection refused to localhost:6379
- **Causa**: Redis no está levantado
- **Solución**: Asegúrate de usar `dockercompose.bat` que incluye todos los overrides

### Error al crear sitio: Can't connect to MySQL
- **Causa**: MariaDB no terminó de inicializar
- **Solución**: Espera 30-60 segundos después de ejecutar `dockercompose.bat` antes de crear el sitio

### Página no carga en http://localhost:8080
- **Causa**: Frontend no está corriendo o sitio no está creado
- **Solución**: 
  1. Verifica que todos los contenedores estén "Up": `docker compose [...] ps`
  2. Verifica que creaste un sitio con `create-site.bat`
  3. Revisa logs: `.\scripts\docker\logs.bat`

### Scheduler is disabled
- **Solución**: 
  ```bash
  docker compose [...] exec backend bench --site localhost scheduler enable
  ```

## Limpieza Completa

Para eliminar TODO (contenedores, volúmenes, datos):
```bash
docker compose -f compose.yaml -f overrides/compose.mariadb.yaml -f overrides/compose.redis.yaml -f overrides/compose.noproxy.yaml down -v
```

⚠️ **Advertencia**: Esto eliminará la base de datos y todos los datos. Úsalo solo si quieres empezar de cero.

## Recursos

- [Documentación oficial frappe_docker](https://github.com/frappe/frappe_docker)
- [Documentación ERPNext](https://docs.erpnext.com/)
- [Documentación Frappe Framework](https://frappeframework.com/docs)
