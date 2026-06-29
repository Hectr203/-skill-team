# 09 — Variables de Entorno, Configuración y Dependencias

Este documento lista de forma exhaustiva las variables de entorno que requiere el backend del proyecto **VTP Transporte**, su propósito, componentes involucrados y confidencialidad, así como las herramientas y prerrequisitos del sistema de desarrollo y producción.

---

## 1. Tabla de Variables de Entorno (Backend)

Estas variables se configuran en el archivo `.env` en desarrollo local y en la sección *App Settings* de Azure App Service en producción.

| Nombre de la Variable | Requerido | Sensible | Propósito | Ejemplo / Ficticio | Componente |
|---|---|---|---|---|---|
| `NODE_ENV` | Sí | No | Define el entorno de ejecución (`production` o `development`). | `production` | Core Express |
| `PORT` | Sí | No | Puerto en el que escucha el servidor Node.js. | `8080` (Azure) / `3000` (Local) | Core Express |
| `CORS_ALLOWED_ORIGINS` | Sí | No | Lista separada por comas de los orígenes web permitidos para conectar al backend. | `http://localhost:5173,https://static-web.net` | CORS Middleware |
| `API_BASE_URL` | Sí | No | URL pública base de la propia API, utilizada para redirecciones y metadatos. | `https://smt-api.azurewebsites.net` | Core Express |
| `DB_HOST` | Sí | No | Nombre del servidor (host) de la base de datos MySQL. | `mysql-server.mysql.database.azure.com` | Base de Datos |
| `DB_PORT` | Sí | No | Puerto de conexión a la base de datos. | `3306` | Base de Datos |
| `DB_NAME` | Sí | No | Nombre de la base de datos MySQL. | `vtptransporte` | Base de Datos |
| `DB_USER` | Sí | No | Usuario administrador de la base de datos. | `smtadmin` | Base de Datos |
| `DB_PASSWORD` | Sí | **Sí** | Contraseña de conexión a la base de datos MySQL. | `*ContraseñaSegura123*` | Base de Datos |
| `DB_SSL` | Sí | No | Booleano para activar la encriptación SSL en la conexión de BD. | `true` (Azure) / `false` (Local) | Base de Datos |
| `DB_CONNECT_TIMEOUT_MS` | No | No | Tiempo máximo de espera en milisegundos para conectar con la base de datos. | `15000` | Base de Datos |
| `JWT_SECRET` | Sí | **Sí** | Llave privada secreta utilizada para cifrar y verificar tokens JWT. | `*ClaveSecretaSuperCompleja*` | Autenticación |
| `JWT_EXPIRES_IN` | No | No | Tiempo de expiración de las sesiones JWT. | `8h` | Autenticación |
| `AZURE_STORAGE_CONNECTION_STRING` | Sí | **Sí** | Cadena de conexión para subir archivos a Azure Blob Storage. | `DefaultEndpointsProtocol=https;AccountName=...` | Storage / Uploads |
| `AZURE_STORAGE_CONTAINER_NAME` | Sí | No | Nombre del contenedor de Blob Storage para guardar los archivos. | `vtptransporte-archivos` | Storage / Uploads |
| `FACTURAMA_BASE_URL` | Sí | No | URL de la API de Facturama para timbrado de facturas. | `https://apisandbox.facturama.mx/` | Facturación (CFDI) |
| `FACTURAMA_USERNAME` | Sí | No | Usuario de la API de Facturama. | `UsuarioFacturama` | Facturación (CFDI) |
| `FACTURAMA_PASSWORD` | Sí | **Sí** | Contraseña de acceso a la API de Facturama. | `*PasswordFacturama*` | Facturación (CFDI) |
| `SMTP_HOST` | Sí | No | Host del servidor SMTP para el envío de notificaciones por correo. | `smtp.gmail.com` | Correo de Salida |
| `SMTP_PORT` | Sí | No | Puerto SMTP (ej. 465 SSL, 587 TLS). | `587` | Correo de Salida |
| `SMTP_USER` | Sí | No | Cuenta de correo emisora de las notificaciones. | `correo-emisor@gmail.com` | Correo de Salida |
| `SMTP_PASSWORD` | Sí | **Sí** | Contraseña de la cuenta de correo emisora (ej. Contraseña de Aplicación de Google). | `*PasswordDeAplicacion*` | Correo de Salida |
| `SMTP_FROM_EMAIL` | No | No | Dirección de correo de retorno que se muestra al usuario receptor. | `correo-emisor@gmail.com` | Correo de Salida |

---

## 2. Dependencias del Entorno y Prerrequisitos

Para operar y compilar el proyecto en cualquier máquina local o servidor de integración continua (CI), se deben instalar las siguientes herramientas:

### A. Herramientas Locales Obligatorias:
- **Node.js (Versión v22.x LTS):** Es fundamental usar Node 22 para garantizar compatibilidad con el entorno de Azure App Service.
  - *Validación:* `node --version` (debe retornar `v22.x.x`).
- **npm (Versión v10.x o superior):** Administrador de paquetes de Node.js.
  - *Validación:* `npm --version`.
- **Azure CLI (`az`):** Interfaz de línea de comandos oficial de Azure.
  - *Validación:* `az --version` (debe mostrar información del CLI y bicep).
- **Azure Developer CLI (`azd`):** Requerido para orquestar y desplegar mediante `azure.yaml`.
  - *Validación:* `azd version`.

### B. Cuentas y Accesos en la Nube:
- **Suscripción de Azure:** Se requiere una suscripción activa con permisos de Colaborador (Contributor) o Propietario (Owner) sobre el Grupo de Recursos `SMT-TRASPORTE-PRODUCCION` para poder desplegar infraestructura y código.
- **Acceso SMTP:** Una cuenta de correo configurada para SMTP con accesos de autenticación activados (como contraseñas de aplicación).
- **Acceso a Facturama:** Cuenta activa en el entorno Sandbox o Producción de Facturama para la validación de CFDI.
