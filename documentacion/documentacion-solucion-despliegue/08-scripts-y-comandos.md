# 08 — Scripts y Comandos

Este documento recopila todos los scripts de base de datos, automatizaciones y comandos administrativos utilizados en el ciclo de vida del proyecto **VTP Transporte**, detallando sus rutas, objetivos, parámetros y formas de ejecución.

---

## 1. Scripts de Base de Datos (vtp-transporte-backend-main)

Los scripts están ubicados en `vtp-transporte-backend-main/scripts/` y se ejecutan a través de comandos `npm run` desde la raíz de la carpeta del backend.

### A. Migración Segura (`migrate-safe.js`)
- **Comando:** `npm run db:migrate-safe`
- **Ubicación:** `vtp-transporte-backend-main/scripts/migrate-safe.js`
- **Objetivo:** Conectarse a la base de datos MySQL, crearla si no existe, verificar los archivos de migración (`.sql`) y seeders pendientes y aplicarlos secuencialmente registrándolos en la tabla `_migrations_log` para no duplicar ejecuciones.
- **Forma de ejecución:**
  ```bash
  # Desde vtp-transporte-backend-main/
  npm run db:migrate-safe
  ```
- **Errores Frecuentes:** `ECONNREFUSED` (servidor MySQL apagado o variables de entorno incorrectas).

### B. Vista Previa de Migraciones (Dry-Run)
- **Comando:** `npm run db:migrate-safe:dry-run`
- **Objetivo:** Ejecutar la lógica de verificación de migración pero **sin aplicar cambios SQL reales**. Permite ver qué archivos están pendientes antes de ejecutarlos en producción.
- **Forma de ejecución:**
  ```bash
  npm run db:migrate-safe:dry-run
  ```

### C. Registro Inicial de Tablas Existentes (`migrate-register-existing.js`)
- **Comando:** `npm run db:register-existing`
- **Ubicación:** `vtp-transporte-backend-main/scripts/migrate-register-existing.js`
- **Objetivo:** Utilizado una sola vez cuando se hereda una base de datos que ya tiene tablas creadas manualmente pero que no cuenta con la tabla `_migrations_log`. Ejecuta el análisis y registra las tablas existentes para no fallar por tablas duplicadas en futuras migraciones seguras.
- **Forma de ejecución:**
  ```bash
  npm run db:register-existing
  ```

### D. Reset de Base de Datos Local (`migrate-local.js`)
- **Comando:** `npm run db:migrate:reset`
- **Ubicación:** `vtp-transporte-backend-main/scripts/migrate-local.js`
- **Objetivo:** Elimina y recrea la base de datos MySQL local desde cero, aplicando todas las migraciones y seeders en limpio.
- **Advertencia:** **NUNCA ejecutar en producción o staging.** Destruirá todos los datos almacenados.
- **Forma de ejecución:**
  ```bash
  npm run db:migrate:reset
  ```

---

## 2. Scripts de Memoria del Proyecto (Agencia)

Ubicados en la carpeta del orquestador, son utilizados para registrar el estado e historial del proyecto de forma local.

### Gestor de Memoria (`memoria_proyecto.py`)
- **Ubicación:** `Agencia_Proyectos_Existentes/scripts/memoria_proyecto.py`
- **Objetivo:** Administrar los archivos de memoria encriptada y registros del proyecto.
- **Comandos Principales:**
  - **Inicializar memoria:** `python3 Agencia_Proyectos_Existentes/scripts/memoria_proyecto.py --proyecto "." init`
  - **Ver historial y pendientes:** `python3 Agencia_Proyectos_Existentes/scripts/memoria_proyecto.py --proyecto "." start`
  - **Cerrar tarea y guardar cambios:**
    ```bash
    python3 Agencia_Proyectos_Existentes/scripts/memoria_proyecto.py \
      --proyecto "." \
      close \
      --tareas "Descripción de tareas" \
      --decisiones "Decisión tomada" \
      --cloud-resumen "Resumen" \
      --archivos "archivos,modificados"
    ```

---

## 3. Comandos de Azure y Despliegue (`azd` / `az`)

Ejecutados desde la raíz del proyecto (`vtptransportes/`) para la administración de recursos en Azure.

### A. Despliegue Completo (`azd up`)
- **Propósito:** Ejecuta tanto el aprovisionamiento de infraestructura Bicep como la compilación y subida del código fuente de frontend y backend.
- **Ejecución:**
  ```bash
  azd up
  ```

### B. Solo Despliegue de Código (`azd deploy`)
- **Propósito:** Sube el código fuente de las aplicaciones sin volver a ejecutar los archivos Bicep de infraestructura.
- **Ejecución:**
  ```bash
  # Desplegar backend y frontend
  azd deploy
  
  # Desplegar solo el backend
  azd deploy backend --no-prompt
  
  # Desplegar solo el frontend
  azd deploy frontend --no-prompt
  ```

### C. Solo Aprovisionamiento de Infraestructura (`azd provision`)
- **Propósito:** Aplica los cambios realizados únicamente en el archivo `main.bicep` en los recursos de Azure.
- **Ejecución:**
  ```bash
  azd provision
  ```

### D. Eliminación de CORS de Plataforma de Azure
- **Propósito:** Remueve el dominio indicado de las reglas CORS de Azure App Service para delegar el control a Express.
- **Ejecución:**
  ```bash
  az webapp cors remove \
    --name smt-transportes-api \
    --resource-group SMT-TRASPORTE-PRODUCCION \
    --allowed-origins 'https://blue-bush-0d9760810.7.azurestaticapps.net'
  ```
