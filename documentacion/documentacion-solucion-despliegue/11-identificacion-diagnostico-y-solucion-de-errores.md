# 11 — Identificación, Diagnóstico y Solución de Errores

Este documento recopila un catálogo de los fallos técnicos reales identificados durante el desarrollo, despliegue y puesta en marcha del proyecto **VTP Transporte**, ofreciendo los métodos de diagnóstico y las soluciones aplicadas para cada uno de ellos.

---

## 1. Categoría: Redes y Políticas de Origen Cruzado (CORS)

### Fallo: Bloqueo de CORS en Producción (Preflight OPTIONS Fallido)
- **Mensaje de Error:** 
  `Access to fetch at 'https://smt-transportes-api.azurewebsites.net/api/auth/forgot-password' from origin 'https://blue-bush-0d9760810.7.azurestaticapps.net' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource.`
- **Síntomas:** Las llamadas del frontend al backend fallaban de inmediato en producción, retornando un error de tipo `Failed to fetch`. Las operaciones de login y recuperación de contraseña no funcionaban.
- **Causa Raíz:** El enrutador nativo de Express procesaba la petición `OPTIONS` y respondía antes de que la capa de configuración CORS de la plataforma de Azure pudiera inyectar las cabeceras de origen cruzado. Al no tener Express configurado un middleware de CORS, la respuesta salía sin cabeceras.
- **Método de Diagnóstico:** Ejecutar un comando `curl` simulando el preflight `OPTIONS` y validar la respuesta de cabeceras HTTP:
  ```bash
  curl -i -X OPTIONS 'https://smt-transportes-api.azurewebsites.net/api/auth/forgot-password' \
    -H 'Origin: https://blue-bush-0d9760810.7.azurestaticapps.net' \
    -H 'Access-Control-Request-Method: POST' \
    -H 'Access-Control-Request-Headers: content-type'
  ```
- **Solución:**
  1. Implementar un middleware manual en Express (`src/app.js`) que capture peticiones `OPTIONS` y devuelva de inmediato un estado `204 No Content` junto con las cabeceras CORS dinámicas basadas en `CORS_ALLOWED_ORIGINS`.
  2. Eliminar la configuración CORS en el portal de Azure y del archivo `main.bicep` para evitar conflictos por cabeceras duplicadas.

---

## 2. Categoría: Base de Datos y Conexión

### Fallo: Pérdida de Conexión y Timeout de MySQL (servidor Flexible)
- **Mensaje de Error:** `Error: connect ETIMEDOUT` o `Connection lost` al iniciar el backend.
- **Síntomas:** El backend tardaba demasiado en levantar o fallaba a los pocos segundos de iniciar, provocando que Azure App Service reiniciara continuamente el contenedor de Node.js.
- **Causa Raíz:** El tiempo de espera de conexión por defecto de MySQL (`connectTimeout`) era muy bajo para la latencia inicial que experimenta el servidor flexible de Azure Database for MySQL al salir del estado de reposo (idle).
- **Método de Diagnóstico:** Monitorear los logs en tiempo real del contenedor en Azure App Service usando:
  ```bash
  az webapp log tail --name smt-transportes-api --resource-group SMT-TRASPORTE-PRODUCCION
  ```
- **Solución:**
  1. Incrementar el tiempo de espera de conexión a **`10000ms`** (10 segundos) o superior en el archivo de entorno mediante la variable `DB_CONNECT_TIMEOUT_MS`.
  2. Configurar la inicialización de la conexión de base de datos como no bloqueante durante el arranque del backend en `src/server.js`, permitiendo que el servidor escuche peticiones en el puerto asignado mientras establece la conexión con MySQL en segundo plano.

### Fallo: Acceso Denegado por Reglas de Firewall de MySQL
- **Mensaje de Error:** `Error: ER_DBACCESS_DENIED_ERROR` o bloqueos de red al conectar a la base de datos de producción.
- **Síntomas:** El backend local de desarrollo o el backend remoto en Azure App Service no lograban conectar con la base de datos MySQL, a pesar de que el usuario y la contraseña eran correctos.
- **Causa Raíz:** Azure Database for MySQL Flexible Server bloquea por defecto todo el tráfico entrante a menos que se defina explícitamente una regla de firewall.
- **Método de Diagnóstico:** Intentar conectar a la base de datos mediante un cliente MySQL externo (ej. DBeaver) o validar las reglas de firewall en el recurso de Azure.
- **Solución:**
  1. Para el App Service en Azure: Agregar la regla de firewall en `main.bicep` con IP de inicio `0.0.0.0` y fin `0.0.0.0` (lo cual es el identificador de Azure para "Permitir acceso a servicios de Azure").
  2. Para desarrollo local: Si necesitas conectar tu máquina local a la base de datos de producción para tareas de mantenimiento, debes agregar temporalmente tu dirección IP pública en el panel de redes del servidor flexible de MySQL en Azure Portal.

---

## 3. Categoría: Despliegue e Infraestructura

### Fallo: Advertencia de compilación ausente en App Service Linux (`az webapp deploy`)
- **Mensaje de Advertencia:** `'az webapp deploy' does not run build automation (dependency installation, compilation, etc.) by default for Linux web apps.`
- **Síntomas:** Al realizar despliegues usando ZIP directo, el servidor no encontraba los módulos de Node (`node_modules`) y fallaba al arrancar.
- **Causa Raíz:** Azure App Service en Linux no ejecuta `npm install` al recibir un archivo ZIP a menos que se le indique explícitamente a través de variables de entorno del sistema de compilación de Kudu.
- **Solución:** Configurar la variable de entorno **`SCM_DO_BUILD_DURING_DEPLOYMENT=true`** en los *App Settings* de la aplicación web (definida dentro del bloque de variables de `main.bicep`). Esto indica a Azure que ejecute la compilación remota automáticamente al recibir los archivos empaquetados.
