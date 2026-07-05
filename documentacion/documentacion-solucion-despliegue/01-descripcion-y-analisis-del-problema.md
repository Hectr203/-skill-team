# 01 — Descripción y Análisis del Problema

Este documento detalla el comportamiento incorrecto que se presentó en el entorno de producción del sistema **VTP Transporte**, su impacto operativo en el negocio, los síntomas observados en la consola del cliente y los disparadores del fallo.

---

## 1. El Comportamiento Incorrecto

El sistema de autenticación del frontend no permitía la comunicación cruzada con el backend en el entorno de producción. Al realizar cualquier petición que requiriera un método HTTP como `POST`, el navegador del usuario bloqueaba la solicitud de inmediato.

El fallo se hizo evidente inicialmente en la funcionalidad de **recuperación de contraseña (`forgot-password`)**, donde al ingresar el correo electrónico del usuario y presionar el botón de envío, el sistema no completaba el proceso y devolvía un error genérico de conexión en la interfaz visual.

---

## 2. Componente y Etapa Afectada

El error ocurrió en la frontera de comunicación entre:
- **El cliente web (Frontend):** Ejecutándose en el navegador del usuario desde el origen de Azure Static Web Apps (`https://blue-bush-0d9760810.7.azurestaticapps.net`).
- **La API HTTP (Backend):** Alojada en Azure App Service (`https://smt-transportes-api.azurewebsites.net`).

El fallo se producía durante la etapa de **despliegue productivo**. En el entorno de desarrollo local, el error no se presentaba debido al uso del servidor proxy de desarrollo provisto por Vite, el cual encubría la petición de origen cruzado convirtiéndola en una petición del mismo origen ante los ojos del navegador.

---

## 3. Impacto en el Sistema

El impacto de este problema fue crítico:
- **Bloqueo Total del Flujo de Usuarios:** Los usuarios no podían restablecer sus contraseñas olvidadas, lo que les impedía acceder a la plataforma.
- **Inoperabilidad de la API:** Al ser un problema de políticas de CORS a nivel global, cualquier endpoint de la API (`/api/auth/login`, `/api/viajes`, etc.) invocado directamente desde un origen distinto al del propio App Service sufría el mismo bloqueo.
- **Degradación de la Experiencia del Usuario:** La interfaz mostraba un error de tipo `TypeError: Failed to fetch`, traduciéndose en el frontend como "Error de conexión. Intenta nuevamente", sin mayor explicación del problema real de infraestructura.

---

## 4. Síntomas y Evidencias del Error

El problema se detectó mediante el análisis de la consola de herramientas de desarrollador (Developer Tools) del navegador Chrome/Edge al interactuar con el formulario `ForgotPasswordForm.vue`.

### Trazas del Log del Navegador:
```text
Access to fetch at 'https://smt-transportes-api.azurewebsites.net/api/auth/forgot-password' from origin 'https://blue-bush-0d9760810.7.azurestaticapps.net' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource.

POST https://smt-transportes-api.azurewebsites.net/api/auth/forgot-password net::ERR_FAILED

ForgotPasswordForm.vue:33 Error al recuperar contraseña: TypeError: Failed to fetch
    at Object.apply (hook.js:1:329)
    at window.fetch (fetchInterceptor.js:23:24)
    at Object.post (authService.js:56:28)
    at Object.forgotPassword (authService.js:197:22)
    at ForgotPasswordForm.vue:29:25
```

---

## 5. Condiciones de Reproducción

El problema se reproducía de manera consistente bajo las siguientes condiciones:
1. **Entorno Productivo Activo:** Peticiones HTTP reales emitidas desde el dominio HTTPS de Azure Static Web Apps hacia el dominio HTTPS de Azure App Service.
2. **Métodos que requieran Preflight (Solicitud de Vuelo Previo):** Peticiones como `POST` con la cabecera `Content-Type: application/json` que obligan al navegador a realizar una petición inicial con el método `OPTIONS` (Preflight) para validar las reglas CORS permitidas por el servidor.
3. **Petición Directa (sin Proxy intermedio en producción):** Al no contar con una regla de redirección o proxy inverso en la capa CDN de la Static Web App, la llamada se hacía directamente hacia el dominio de Azure App Service.
