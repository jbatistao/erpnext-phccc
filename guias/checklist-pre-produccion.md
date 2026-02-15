# Checklist de Pre-Producción ERPNext

Lista de verificación completa antes de lanzar ERPNext a producción.

## 📋 Checklist General

### Infraestructura
- [ ] VPS con especificaciones correctas (mínimo 8 GB RAM, 4 vCores)
- [ ] Ubuntu 24.04 LTS instalado y actualizado
- [ ] Firewall configurado (UFW con puertos 22, 80, 443)
- [ ] Swap configurado (mínimo 4 GB)
- [ ] Hostname configurado correctamente
- [ ] Timezone configurado según ubicación

### DNS y Dominio
- [ ] Dominio registrado
- [ ] Registro A apuntando a IP del VPS
- [ ] Registro AAAA configurado (si hay IPv6)
- [ ] Propagación DNS verificada (dnschecker.org)
- [ ] TTL configurado (300-600 segundos recomendado)

### Docker y Coolify
- [ ] Docker instalado y funcionando
- [ ] Coolify instalado y accesible
- [ ] Usuario admin de Coolify configurado
- [ ] SMTP configurado en Coolify (para notificaciones)

### ERPNext
- [ ] Servicios de ERPNext desplegados
- [ ] Todos los contenedores "healthy" y "running"
- [ ] Sitio creado con dominio correcto
- [ ] Scheduler habilitado
- [ ] Apps instaladas verificadas (frappe, erpnext)

### SSL/TLS
- [ ] Certificado SSL instalado
- [ ] HTTPS funcionando correctamente
- [ ] Redirección HTTP → HTTPS habilitada
- [ ] Certificado válido y no auto-firmado
- [ ] Auto-renovación de certificado configurada

### Seguridad
- [ ] Contraseña de admin cambiada (no usar "admin")
- [ ] Contraseña de base de datos segura (min 20 caracteres)
- [ ] SSH con autenticación por clave (opcional pero recomendado)
- [ ] Root login deshabilitado en SSH (opcional)
- [ ] Fail2ban instalado (opcional pero recomendado)
- [ ] Acceso a Coolify protegido con contraseña fuerte

### Backups
- [ ] Script de backup automático configurado
- [ ] Backup programado en crontab (diario)
- [ ] Backup remoto configurado (S3, Google Drive, etc.)
- [ ] Backup manual probado y restaurado exitosamente
- [ ] Retención de backups configurada (ej: 30 días)

### Email
- [ ] SMTP configurado en ERPNext
- [ ] Email de prueba enviado y recibido
- [ ] Plantillas de email personalizadas
- [ ] Dominio verificado para emails (SPF, DKIM, DMARC)

### Performance
- [ ] Caché funcionando (Redis)
- [ ] Workers activos (short, long)
- [ ] Scheduler funcionando
- [ ] Tiempo de carga < 3 segundos
- [ ] Recursos monitoreados (CPU, RAM, Disco)

### Monitoreo
- [ ] Logs accesibles y rotando correctamente
- [ ] Alertas configuradas (email, Slack, etc.)
- [ ] Uptime monitoring configurado (UptimeRobot, etc.)
- [ ] Dashboard de monitoreo configurado (Netdata, Grafana)

---

## 🔐 Checklist de Seguridad Avanzada

### Sistema Operativo
- [ ] Actualizaciones automáticas habilitadas
- [ ] Solo paquetes esenciales instalados
- [ ] Logs de sistema monitoreados
- [ ] Auditd configurado (opcional)

### Docker
- [ ] Imágenes oficiales únicamente
- [ ] Volúmenes con permisos correctos
- [ ] Red interna configurada
- [ ] Secrets para contraseñas sensibles (opcional)

### Aplicación
- [ ] Modo desarrollador DESHABILITADO
- [ ] API keys rotadas regularmente
- [ ] Permisos de usuario revisados
- [ ] Autenticación de dos factores habilitada para admins
- [ ] Login attempts limitados

### Base de Datos
- [ ] Usuario root NO usado por la aplicación
- [ ] Conexión solo desde localhost o red interna
- [ ] Backups encriptados
- [ ] Logs de consultas deshabilitados (prevenir leaks)

---

## 📊 Checklist de Configuración ERPNext

### Información de la Empresa
- [ ] Nombre de empresa configurado
- [ ] Logo de empresa subido
- [ ] Información fiscal configurada
- [ ] Moneda por defecto establecida
- [ ] País y zona horaria correctos

### Usuarios y Permisos
- [ ] Roles creados según organigrama
- [ ] Usuarios creados con emails correctos
- [ ] Permisos asignados por rol
- [ ] Usuarios de prueba eliminados
- [ ] Administrator como último recurso

### Módulos
- [ ] Módulos necesarios activados
- [ ] Módulos innecesarios desactivados
- [ ] Flujos de trabajo definidos
- [ ] Campos personalizados creados

### Integraciones
- [ ] Gateway de pago configurado (si aplica)
- [ ] Integración con contabilidad (si aplica)
- [ ] API habilitada y documentada
- [ ] Webhooks configurados (si aplica)

### Reportes y Dashboards
- [ ] Dashboards personalizados creados
- [ ] Reportes necesarios configurados
- [ ] Permisos de reportes asignados
- [ ] Exportaciones probadas

---

## 🧪 Checklist de Pruebas

### Funcionalidad Básica
- [ ] Login con usuario admin
- [ ] Login con usuario regular
- [ ] Crear, editar, eliminar registros
- [ ] Búsqueda funcionando
- [ ] Filtros funcionando
- [ ] Exportación de datos (PDF, Excel)

### Flujos de Trabajo
- [ ] Crear cotización → Orden de venta
- [ ] Facturación y pagos
- [ ] Inventario y stock
- [ ] Compras y proveedores
- [ ] RRHH (si aplica)

### Performance
- [ ] Carga de página < 3 segundos
- [ ] Búsqueda < 1 segundo
- [ ] Reportes grandes < 10 segundos
- [ ] Sin errores en consola JavaScript
- [ ] Sin errores 500 en logs

### Mobile
- [ ] Interfaz responsiva
- [ ] Login desde móvil
- [ ] Operaciones básicas desde móvil

---

## 📱 Checklist Post-Lanzamiento

### Primeras 24 Horas
- [ ] Monitorear logs continuamente
- [ ] Verificar backups automáticos ejecutados
- [ ] Revisar alertas y notificaciones
- [ ] Confirmar que usuarios pueden acceder
- [ ] Medir tiempos de respuesta

### Primera Semana
- [ ] Revisar feedback de usuarios
- [ ] Optimizar basado en uso real
- [ ] Verificar integridad de datos
- [ ] Confirmar backups restaurables
- [ ] Documentar incidencias

### Primer Mes
- [ ] Análisis de uso y adoption
- [ ] Ajustes de permisos basados en feedback
- [ ] Capacitación adicional si necesario
- [ ] Plan de mejora continua
- [ ] Revisión de seguridad

---

## 🚨 Plan de Contingencia

### Ante Caída del Servicio
1. **Identificar causa** (logs, monitoreo)
2. **Intentar reinicio** (`docker compose restart`)
3. **Escalar recursos** (si es problema de capacidad)
4. **Restaurar desde backup** (si hay corrupción)
5. **Comunicar a usuarios** (tiempo estimado)

### Ante Brecha de Seguridad
1. **Aislar sistema** (firewall)
2. **Cambiar todas las contraseñas**
3. **Revisar logs de acceso**
4. **Restaurar desde backup limpio**
5. **Notificar a afectados** (si aplica GDPR)

### Ante Pérdida de Datos
1. **NO entrar en pánico**
2. **Detener servicios** (prevenir más pérdida)
3. **Restaurar desde último backup**
4. **Verificar integridad de datos restaurados**
5. **Documentar incidente**

---

## 📞 Contactos de Emergencia

Mantén esta lista actualizada y accesible:

```
[ ] Admin del sistema: ___________________ Tel: _______________
[ ] Desarrollador: _______________________ Tel: _______________
[ ] Soporte Contabo: support@contabo.com
[ ] Soporte Frappe: GitHub Issues / Discuss Forum
[ ] Registrador de dominio: _______________ Tel: _______________
```

---

## 📝 Documentación a Mantener

- [ ] Credenciales en gestor de contraseñas (1Password, LastPass, etc.)
- [ ] Procedimientos de backup y restauración
- [ ] Diagrama de arquitectura actualizado
- [ ] Lista de cambios y versiones (changelog)
- [ ] Contactos de proveedores
- [ ] Guías de usuario para empleados

---

## ✅ Firma de Aprobación

Una vez completado todo el checklist:

```
Revisado por: ___________________
Fecha: __________________________
Firma: __________________________

Aprobado para producción: SÍ / NO
```

---

## 🔄 Frecuencia de Revisión

Este checklist debe revisarse:
- ✅ Antes de cada deploy mayor
- ✅ Mensualmente (seguridad)
- ✅ Trimestralmente (performance)
- ✅ Anualmente (arquitectura)

---

*Usa este checklist como guía. Adapta según las necesidades específicas de tu organización.*
