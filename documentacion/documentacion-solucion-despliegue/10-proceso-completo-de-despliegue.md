# 10 — Proceso Completo de Despliegue

Este documento describe de principio a fin el procedimiento necesario para aprovisionar la infraestructura y desplegar el sistema completo de **VTP Transporte** desde un equipo local nuevo o limpio.

---

## Paso 1: Preparación del Entorno Local

Instala las herramientas requeridas de acuerdo a lo detallado en el documento [09-variables-configuracion-y-dependencias.md](./09-variables-configuracion-y-dependencias.md):
- Instala Node.js v22.x LTS.
- Instala Azure CLI (`az`) y Azure Developer CLI (`azd`).
- Configura Git en tu terminal.

---

## Paso 2: Clonado del Repositorio

Clona el repositorio de código fuente y colócate en la raíz del proyecto:
```bash
git clone https://github.com/Yqel/vtptransportes.git
cd vtptransportes
```

---

## Paso 3: Autenticación en los Servicios de Azure

Es obligatorio iniciar sesión en las dos herramientas de línea de comandos de Azure:

```bash
# 1. Iniciar sesión en la CLI nativa
az login

# 2. Iniciar sesión en la CLI de desarrollador de Azure
azd auth login
```
*Ambos comandos abrirán una ventana en tu navegador web para que introduzcas las credenciales de tu cuenta de Azure.*

---

## Paso 4: Inicialización del Entorno de Despliegue (`azd-env`)

Antes de realizar el aprovisionamiento, se debe inicializar o seleccionar el entorno en Azure Developer CLI:

```bash
# Inicializa el ambiente (si es un ambiente nuevo)
azd init

# Si el entorno ya existe en la máquina, puedes seleccionarlo directamente:
azd env select produccion
```
> El nombre del entorno configurado para este proyecto es **`produccion`**.

---

## Paso 5: Aprovisionamiento de Infraestructura (Bicep)

Este paso lee el archivo `infraestructura/main.bicep`, compila la plantilla a JSON y despliega los recursos físicos en Azure.

```bash
azd provision
```

### Flujo Durante el Aprovisionamiento:
1. La CLI te solicitará seleccionar la suscripción de Azure activa.
2. Te pedirá seleccionar la región geográfica para crear los recursos (se recomienda **`centralus`** o la misma región donde ya operen tus otros servicios).
3. Solicitará los valores obligatorios seguros:
   - **`dbPassword`:** Contraseña compleja para el administrador de MySQL.
   - **`jwtSecret`:** Cadena aleatoria compleja para firmar las sesiones.
4. El proceso tardará aproximadamente de 5 a 10 minutos (la creación de MySQL Flexible Server toma la mayor parte del tiempo).

---

## Paso 6: Compilación y Despliegue del Código

Una vez que la infraestructura física está lista en Azure, procedemos a subir el código del frontend y del backend:

```bash
azd deploy
```

### ¿Qué hace internamente este comando?
1. **Frontend:** Ejecuta la compilación de la SPA (`npm run build`) para generar los assets optimizados en la carpeta `dist`, y los sube a la Azure Static Web App.
2. **Backend:** Empaqueta los archivos de Node.js, ejecuta una compresión ZIP, la envía a Azure App Service, e instala las dependencias de Node en el servidor remoto gracias a la variable de entorno `SCM_DO_BUILD_DURING_DEPLOYMENT=true`.

---

## Paso 7: Ejecución de Migraciones de Base de Datos

El despliegue de código **no ejecuta la estructura de tablas de forma automática** en la base de datos MySQL. Se debe ejecutar la migración incremental de forma manual desde el entorno local configurado para apuntar a producción:

```bash
# 1. Accede a la carpeta del backend
cd vtp-transporte-backend-main

# 2. Asegúrate de que las variables de entorno de producción estén en tu archivo .env
# (DB_HOST, DB_USER, DB_PASSWORD, DB_SSL=true)

# 3. Ejecuta el script de migración segura
npm run db:migrate-safe
```

La consola mostrará el listado de archivos `.sql` de estructura y seeders de datos iniciales que han sido insertados de manera exitosa en la base de datos de producción.

---

## Paso 8: Confirmación del Funcionamiento

Realiza una petición de prueba utilizando `curl` contra el endpoint de salud de la API o la ruta OPTIONS de recuperación de contraseñas para verificar que los servicios estén activos y respondiendo correctamente:

```bash
curl -i -X OPTIONS 'https://smt-transportes-api.azurewebsites.net/api/auth/forgot-password' \
  -H 'Origin: https://blue-bush-0d9760810.7.azurestaticapps.net' \
  -H 'Access-Control-Request-Method: POST' \
  -H 'Access-Control-Request-Headers: content-type'
```

La respuesta debe ser `HTTP/1.1 204 No Content` e incluir la cabecera `Access-Control-Allow-Origin: https://blue-bush-0d9760810.7.azurestaticapps.net`.
