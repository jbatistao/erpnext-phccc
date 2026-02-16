bash
## Busca el contenedor del backend
docker ps | grep backend

## Entra al contenedor
docker exec -it [BACKEND_CONTAINER_NAME] bash

## Ver el password de la BD
echo $DB_PASSWORD

## El BD Name es el nombre del servicio para la BD

## Crea el sitio
bench new-site ph.puntospanama.net --admin-password [ADMIN_PASSWORD] --db-root-password [DB_PASSWORD]

## Instala ERP Next
bench --site ph.puntospanama.net install-app erpnext

## Habilita el schedule
bench --site ph.puntospanama.net scheduler enable



-------------------

Para estructurar la contabilidad de una administradora de edificios en ERPNext 16, la clave no es solo registrar gastos, sino mantener la **trazabilidad por unidad de negocio (edificio)**. Al ser una administradora, probablemente manejes fondos propios y fondos de terceros (los edificios), lo cual requiere una separación clara.

Aquí tienes la hoja de ruta para configurar tu estructura contable:

---

## 1. El Plan de Cuentas (Chart of Accounts)

ERPNext crea un plan estándar, pero para 3 edificios necesitas una segmentación específica. Tienes dos caminos:

* **Opción A (Cuentas por Edificio):** Crear subcuentas dentro del Activo y Pasivo para cada edificio (ej. "Caja Edificio A", "Caja Edificio B"). Es muy detallado pero puede volverse rígido si creces.
* **Opción B (Dimensiones Contables - Recomendado):** Mantener cuentas generales (ej. "Mantenimiento y Reparaciones") y usar la función de **Accounting Dimensions** para etiquetar cada transacción con el nombre del edificio.

### Estructura sugerida de Cuentas:

* **Activos Corrientes:**
* Cuentas Bancarias (Una por edificio si tienen cuentas separadas).
* Cuentas por Cobrar (Clientes/Condóminos).


* **Ingresos:**
* Cuotas de Mantenimiento / Expensas.
* Alquiler de Áreas Comunes.
* Multas e Intereses.


* **Gastos:**
* Servicios Públicos (Luz, Agua del edificio).
* Nómina (Conserjes, Seguridad).
* Mantenimiento de Elevadores/Áreas Verdes.



---

## 2. Dimensiones Contables (La pieza clave)

En lugar de multiplicar tus cuentas de gastos por tres, activa las **Accounting Dimensions**.

1. Ve a **Accounting Dimension** en la barra de búsqueda.
2. Crea una dimensión llamada **"Edificio"**.
3. Agrega los valores: `Edificio 01`, `Edificio 02`, `Edificio 03`.
4. Marca esta dimensión como **Mandatoria** en las cuentas de Ingresos y Gastos.

Esto te permitirá generar un **Estado de Resultados (P&L)** filtrado por edificio con un solo clic, sin ensuciar el catálogo de cuentas.

---

## 3. Centros de Costos (Cost Centers)

Configura una jerarquía de Centros de Costos que refleje la operación:

* **Principal (Root)**
* Administradora (Gastos de tu oficina central).
* Edificios (Grupo)
* Edificio A
* Edificio B
* Edificio C





---

## 4. Gestión de Condóminos y Facturación

Para la parte operativa, utiliza el módulo de **Selling** (Ventas) adaptado:

* **Customer (Cliente):** Cada propietario o unidad (Ej: "Apto 101 - Edificio A").
* **Subscription (Suscripciones):** Úsalas para automatizar la generación mensual de la factura de mantenimiento/expensas.
* **Payment Entry:** Para registrar los pagos y que se apliquen correctamente a la cuenta por cobrar de cada dueño.

---

## 5. Reportes Financieros

Una vez configurado lo anterior, podrás obtener:

* **Balance Sheet por Edificio:** Si usas cuentas bancarias separadas.
* **Profit and Loss por Dimensión:** Para ver cuál edificio es más costoso de mantener o cuál tiene mayor morosidad.
* **General Ledger:** Filtrado por la dimensión "Edificio" para auditorías rápidas.

---

### ¿Cómo vas a manejar los pagos?

¿Los inquilinos pagan a una cuenta única de la administradora o cada edificio tiene su propia cuenta bancaria legalmente constituida? Esto definirá si debemos configurar **Cuentas de Banco** independientes o usar **Cuentas de Contrapartida**.

¿Te gustaría que te ayude a definir el flujo de automatización para el cobro mensual de las expensas?
