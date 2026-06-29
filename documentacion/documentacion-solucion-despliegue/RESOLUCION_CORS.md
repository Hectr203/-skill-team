# Resolución de Problemas de CORS en Producción

Este documento detalla el diagnóstico, la causa raíz, la solución implementada y el procedimiento de despliegue para solucionar el problema de política de CORS (Cross-Origin Resource Sharing) detectado en el entorno de producción al realizar peticiones desde el frontend hacia el backend.

---

## 1. El Problema Presentado

Al intentar utilizar funciones que requieren peticiones HTTP desde el frontend en producción (alojado en Azure Static Web Apps) hacia el backend (alojado en Azure App Service), el navegador bloqueaba las solicitudes de forma inmediata.

### Síntoma en la Consola del Navegador
```text
Access to fetch at 'https://smt-transportes-api.azurewebsites.net/api/auth/forgot-password' from origin 'https://blue-bush-0d9760810.7.azurestaticapps.net' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

Este error impedía operaciones críticas de la aplicación, como la recuperación de contraseña (`forgot-password`), el inicio de sesión y cualquier otra comunicación cliente-servidor en el entorno productivo.

---

## 2. Causa Raíz

El origen del problema residía en la interacción conflictiva entre la configuración de CORS de la plataforma de Azure y el enrutamiento interno de la aplicación Express (Node.js).

### Flujo Conflictivo:
1. El navegador del usuario inicia una petición **Preflight (OPTIONS)** antes de realizar el `POST` real a `/api/auth/forgot-password`.
2. El servidor Node.js/Express interceptaba la petición `OPTIONS` directamente mediante sus middlewares o controladores de rutas genéricos.
3. Al procesar la solicitud, Express respondía directamente con un código de estado (usualmente un `200 OK` con la cabecera `Allow: POST`), pero **sin incluir** las cabeceras CORS necesarias (`Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, etc.).
4. Debido a que Express respondía y cerraba la petición de forma activa, la capa de CORS de Azure App Service no intervenía o no lograba sobreescribir la respuesta para inyectar las cabeceras correctas.
5. El navegador, al recibir una respuesta preflight vacía de cabeceras CORS, determinaba que el servidor no permitía el origen cruzado y bloqueaba la petición real `POST` (generando el error `TypeError: Failed to fetch`).

---

## 3. Proceso de Diagnóstico y Detección

Para identificar este comportamiento y descartar bloqueos de red o errores de aplicación internos, se realizaron los siguientes pasos:

### Paso A: Simulación de Petición Preflight (OPTIONS)
Se ejecutó un comando `curl` simulando el comportamiento del navegador al enviar una petición preflight desde el origen del frontend hacia el backend productivo:

```bash
curl -i -m 30 -X OPTIONS 'https://smt-transportes-api.azurewebsites.net/api/auth/forgot-password' \
  -H 'Origin: https://blue-bush-0d9760810.7.azurestaticapps.net' \
  -H 'Access-Control-Request-Method: POST' \
  -H 'Access-Control-Request-Headers: content-type'
```

**Resultado obtenido inicialmente:**
La respuesta retornaba un código de estado `200 OK` pero carecía por completo del encabezado `Access-Control-Allow-Origin`, confirmando que el servidor de aplicación (Express) estaba respondiendo antes de que la plataforma de Azure pudiese actuar.

### Paso B: Inspección de Configuración en Azure
Se consultó la configuración de CORS de la plataforma de Azure App Service mediante la CLI:

```bash
az webapp cors show --name smt-transportes-api --resource-group SMT-TRASPORTE-PRODUCCION -o json
```

Se validó que el origen `https://blue-bush-0d9760810.7.azurestaticapps.net` estaba configurado en la lista de permitidos en Azure. Sin embargo, debido a la intercepción nativa de Express, esta configuración de plataforma resultaba inoperante.

---

## 4. Solución Implementada

La solución óptima y más robusta consiste en **centralizar la gestión de CORS directamente en el código del servidor Express**, en lugar de depender de la plataforma Azure App Service. Esto garantiza consistencia tanto en desarrollo local como en producción.

### Acciones Realizadas:

1. **Restaurar Middleware de CORS en Express (`src/app.js`):**
   Se implementó un middleware manual de CORS antes de la definición de cualquier ruta. Este middleware:
   - Extrae el origen de la petición.
   - Verifica si se encuentra en la lista de permitidos (provista por variables de entorno).
   - Inyecta dinámicamente las cabeceras requeridas.
   - Responde inmediatamente con `204 No Content` si la petición es un método `OPTIONS`.

2. **Eliminar CORS de la Plataforma Azure:**
   Para prevenir cabeceras duplicadas y conflictos futuros, se eliminó la lista de permitidos en Azure App Service:
   ```bash
   az webapp cors remove --name smt-transportes-api --resource-group SMT-TRASPORTE-PRODUCCION --allowed-origins 'https://blue-bush-0d9760810.7.azurestaticapps.net'
   ```
   También se desactivó la opción de credenciales cruzadas (`supportCredentials`) a nivel plataforma:
   ```bash
   az resource update --ids /subscriptions/22ec4e8e-d285-43a0-8096-2f95a8d16527/resourceGroups/SMT-TRASPORTE-PRODUCCION/providers/Microsoft.Web/sites/smt-transportes-api/config/web --set properties.cors.supportCredentials=false
   ```

3. **Limpieza de Infraestructura como Código (`main.bicep`):**
   Se removió el bloque `cors` dentro de la especificación de `siteConfig` en el recurso de Azure Web App. Con esto, futuros aprovisionamientos de infraestructura no reactivarán el CORS de plataforma innecesariamente.

---

## 5. Justificación Técnica

- **Control Absoluto:** Express es el servidor de aplicaciones y, al recibir la petición en primera instancia, es el componente más adecuado para gestionar y validar los encabezados antes de procesar la lógica de negocio.
- **Portabilidad:** La configuración no depende de características propietarias del proveedor de nube (Azure), lo que facilita portar o replicar el backend en entornos locales, Docker, AWS, GCP, etc.
- **Seguridad:** Los orígenes válidos no se exponen como comodines (`*`). Se leen dinámicamente desde la variable de entorno `CORS_ALLOWED_ORIGINS`, permitiendo configurar múltiples orígenes en producción y localhost en desarrollo de manera segura.

---

## 6. Detalles de la Implementación

### Código del Servidor Backend ([app.js](file:///mnt/nvme/api%20de%20autos/vtptransportes/vtp-transporte-backend-main/src/app.js))
Se inyectó el siguiente middleware en el flujo inicial de solicitudes:

```javascript
const allowedOrigins = new Set(env.corsAllowedOrigins);

app.use((req, res, next) => {
  const origin = (req.headers.origin || "").trim().replace(/\/+$/, "");

  if (origin && allowedOrigins.has(origin)) {
    res.setHeader("Access-Control-Allow-Origin", origin);
    res.setHeader("Vary", "Origin");
    res.setHeader("Access-Control-Allow-Methods", "GET,POST,PUT,PATCH,DELETE,OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization, X-API-Key");
    res.setHeader("Access-Control-Max-Age", "86400"); // 24 horas de caché de preflight
  }

  // Responder inmediatamente al navegador para solicitudes Preflight
  if (req.method === "OPTIONS") {
    return res.status(204).end();
  }

  return next();
});
```

### Configuración del Entorno ([env.js](file:///mnt/nvme/api%20de%20autos/vtptransportes/vtp-transporte-backend-main/src/config/env.js))
Los orígenes se extraen de la variable de entorno `CORS_ALLOWED_ORIGINS`:
```javascript
const corsAllowedOrigins = parseCsv(
  process.env.CORS_ALLOWED_ORIGINS || process.env.FRONTEND_URL || "http://localhost:5173"
);
```

### Infraestructura Bicep ([main.bicep](file:///mnt/nvme/api%20de%20autos/vtptransportes/infraestructura/main.bicep))
Se eliminó la sección `cors` en el recurso de la aplicación web:

```bicep
// Antes:
// siteConfig: {
//   linuxFxVersion: 'NODE|22-lts'
//   cors: {
//     allowedOrigins: frontendUrls
//     supportCredentials: false
//   }
// }

// Ahora:
siteConfig: {
  linuxFxVersion: 'NODE|22-lts'
  appSettings: [
    { name: 'CORS_ALLOWED_ORIGINS', value: join(frontendUrls, ',') }
    // ... rest of settings ...
  ]
}
```

---

## 7. Resultados Obtenidos

Tras aplicar el middleware en el backend y redesplegarlo en Azure, se repitió la validación externa de solicitudes `OPTIONS`:

### Prueba Externa de Preflight
```bash
curl -i -m 30 -X OPTIONS 'https://smt-transportes-api.azurewebsites.net/api/auth/forgot-password' \
  -H 'Origin: https://blue-bush-0d9760810.7.azurestaticapps.net' \
  -H 'Access-Control-Request-Method: POST' \
  -H 'Access-Control-Request-Headers: content-type'
```

### Respuesta Recibida
```http
HTTP/1.1 204 No Content
Date: Fri, 19 Jun 2026 21:32:10 GMT
Connection: keep-alive
Access-Control-Allow-Origin: https://blue-bush-0d9760810.7.azurestaticapps.net
Vary: Origin
Access-Control-Allow-Methods: GET,POST,PUT,PATCH,DELETE,OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization, X-API-Key
Access-Control-Max-Age: 86400
```

**Resultado:** Éxito absoluto. El preflight responde con un código de estado `204` (sin cuerpo) y proporciona los encabezados CORS correctos, lo que permite al navegador dar luz verde a las peticiones reales `POST`, `GET`, etc.

---

## 8. Procedimiento de Despliegue

Para desplegar esta configuración a entornos de producción o staging de manera correcta, sigue las siguientes pautas de Azure Developer CLI:

### Despliegue del Código Modificado (Recomendado)
Dado que los cambios de CORS se resuelven en el código del servidor, solo es necesario redesplegar el servicio del backend:

```bash
# 1. Asegúrate de estar autenticado en Azure y en azd
az login
azd auth login

# 2. Despliega únicamente el backend para acelerar el proceso
azd deploy backend --no-prompt
```

### Aprovisionamiento de Infraestructura (Si cambia de dominio el Frontend)
Si en el futuro se modifica la URL del frontend (ejemplo: se adquiere un dominio personalizado), se debe actualizar la variable `frontendUrls` en `main.bicep` y aprovisionar la infraestructura para actualizar la variable de entorno `CORS_ALLOWED_ORIGINS` en la App Service:

```bash
# 1. Edita la variable 'frontendUrls' en 'infraestructura/main.bicep'
# 2. Aplica los cambios de infraestructura en Azure sin alterar el código actual
azd provision
```
*Nota: Después de ejecutar `azd provision`, se recomienda reiniciar la App Service para asegurar la correcta lectura de las nuevas variables de entorno.*
