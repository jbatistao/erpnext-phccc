# Guías de ERPNext - PHCCC

Documentación completa para desarrollo local y despliegue en producción de ERPNext.

## 📚 Índice de Guías

### 🚀 Despliegue en Producción

#### [Despliegue en Contabo con Coolify](./despliegue-produccion-contabo-coolify.md)
Guía paso a paso completa para desplegar ERPNext en un VPS de Contabo usando Ubuntu 24.04 LTS y Coolify.

**Contenido:**
- Preparación del VPS
- Instalación de Coolify
- Configuración de DNS y SSL
- Despliegue de ERPNext
- Backups automáticos
- Monitoreo y troubleshooting

**Recomendado para:**
- Primera vez desplegando en producción
- Equipos que prefieren interfaz web para gestionar Docker
- Proyectos que requieren SSL automático

---

### 🔧 Referencia Rápida

#### [Comandos Útiles](./comandos-utiles.md)
Referencia rápida de comandos frecuentemente usados para administrar ERPNext.

**Contenido:**
- Monitoreo y logs
- Backups y restauración
- Gestión de usuarios
- Actualización de ERPNext
- Debugging
- Comandos de emergencia

**Recomendado para:**
- Administradores de sistemas
- DevOps
- Consultas rápidas durante operaciones

---

### ✅ Verificación Pre-Producción

#### [Checklist de Pre-Producción](./checklist-pre-produccion.md)
Lista de verificación completa antes de lanzar a producción.

**Contenido:**
- Infraestructura y seguridad
- Configuración de ERPNext
- Pruebas funcionales
- Plan de contingencia
- Documentación necesaria

**Recomendado para:**
- Antes de cada deploy mayor
- Auditorías de seguridad
- Validación de compliance

---

## 🎯 ¿Por Dónde Empezar?

### Si estás en Desarrollo Local
1. Usa los scripts en `/scripts/docker/`
2. Lee el [README de scripts](/scripts/docker/README.md)
3. Consulta [Comandos Útiles](./comandos-utiles.md) según necesites

### Si vas a Producción
1. **Lee completa** la [Guía de Despliegue en Contabo](./despliegue-produccion-contabo-coolify.md)
2. Completa el [Checklist de Pre-Producción](./checklist-pre-produccion.md)
3. Marca como favorito [Comandos Útiles](./comandos-utiles.md)

---

## 📖 Recursos Adicionales

### Documentación Oficial
- [ERPNext Documentation](https://docs.erpnext.com/)
- [Frappe Framework Documentation](https://frappeframework.com/docs)
- [Frappe Docker GitHub](https://github.com/frappe/frappe_docker)

### Comunidad
- [Frappe Forum](https://discuss.frappe.io/)
- [ERPNext GitHub Issues](https://github.com/frappe/erpnext/issues)
- [Frappe School](https://frappe.school/) - Cursos y tutoriales

### Herramientas Relacionadas
- [Coolify](https://coolify.io/) - PaaS self-hosted
- [Contabo](https://contabo.com/) - Provedor VPS
- [MariaDB Docs](https://mariadb.org/documentation/)
- [Redis Documentation](https://redis.io/documentation)

---

## 🔄 Actualizaciones

Este directorio se actualiza regularmente con:
- Nuevas guías según necesidades
- Actualizaciones de versiones de ERPNext
- Mejores prácticas de la comunidad
- Soluciones a problemas comunes

**Última actualización:** Febrero 2026  
**Versión de ERPNext:** v16.5.0  
**Versión de Frappe:** v16.6.0

---

## 🤝 Contribuciones

Si encuentras errores o tienes sugerencias:
1. Documenta el issue claramente
2. Propón solución (si la tienes)
3. Actualiza la guía correspondiente

---

## 📋 Plantillas Útiles

### Formato de Reporte de Incidencia

```markdown
## Descripción del Problema
[Describe brevemente qué está fallando]

## Pasos para Reproducir
1. [Primer paso]
2. [Segundo paso]
3. [etc.]

## Comportamiento Esperado
[Qué debería ocurrir]

## Comportamiento Actual
[Qué está ocurriendo]

## Logs Relevantes
```
[Pega logs aquí]
```

## Entorno
- ERPNext Version: 
- Frappe Version:
- OS: 
- Docker Version:
```

### Formato de Solicitud de Cambio

```markdown
## Objetivo
[Qué se quiere lograr]

## Justificación
[Por qué es necesario]

## Impacto
- [ ] Afecta a usuarios finales
- [ ] Requiere downtime
- [ ] Requiere migración de datos
- [ ] Afecta integraciones

## Plan de Implementación
1. [Paso 1]
2. [Paso 2]
3. [etc.]

## Plan de Rollback
[Cómo revertir si algo sale mal]

## Verificación Post-Deploy
- [ ] [Check 1]
- [ ] [Check 2]
```

---

## 📞 Soporte

### Soporte Técnico
- **GitHub Issues**: Para bugs y features de ERPNext
- **Frappe Forum**: Para preguntas generales
- **Coolify Discord**: Para issues específicos de Coolify

### Soporte de Infraestructura
- **Contabo Support**: Email desde el panel de control
- **Docs de Ubuntu**: [Ubuntu Releases](https://releases.ubuntu.com/)

### Consultoría y Desarrollo
Para implementaciones personalizadas o desarrollo de apps custom, considera contactar:
- Certified Frappe Partners
- Freelancers en Frappe Forum
- Empresas de consultoría ERPNext

---

## ⚠️ Disclaimer

Estas guías son proporcionadas "tal cual" sin garantías. Siempre:
- Prueba en entorno de desarrollo primero
- Haz backups antes de cambios importantes
- Lee documentación oficial para casos específicos
- Adapta según tus necesidades particulares

---

*Desarrollado para PHCCC - Clínica Al Día*  
*Proyecto: ERPNext Implementation*
