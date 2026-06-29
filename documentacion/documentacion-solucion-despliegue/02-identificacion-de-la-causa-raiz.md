# 02 — Identificación de la Causa Raíz

Este documento describe el análisis técnico detallado que condujo a identificar el origen real del fallo de CORS en producción, distinguiendo la causa inmediata de la causa raíz profunda de infraestructura y código.

---

## 1. La Causa Inmediata

La causa inmediata por la que el navegador bloqueaba las llamadas fue la **ausencia del encabezado `Access-Control-Allow-Origin`** en la respuesta a la petición de preflight `OPTIONS` enviada por el cliente.

El navegador realizaba la petición de preflight correspondiente para un método `POST` con tipo de contenido JSON. Al recibir la respuesta del servidor y no encontrar la cabecera CORS que autorizara el origen del frontend (`https://blue-bush-0d9760810.7.azurestaticapps.net`), el motor de seguridad del navegador abortaba inmediatamente la conexión.

---

## 2. La Causa Raíz

La causa raíz del problema fue el **conflicto de intercepción de peticiones `OPTIONS` entre la plataforma Azure App Service y el servidor Node.js/Express**.

### El Mecanismo en Conflicto:

1. **Intención Original del Proyecto:**
   En el commit `b857d08cfbe2fe96964b2574fc5ddb4c8ec9941f` se tomó la decisión de eliminar el middleware `cors` del código del backend Express, bajo la suposición de que Azure App Service (a nivel de infraestructura/plataforma) se encargaría de interceptar todas las peticiones y añadir los encabezados CORS correspondientes.
   
2. **El Bloqueo en Azure App Service:**
   Azure App Service permite definir orígenes permitidos de CORS en su panel de configuración (o mediante el bloque `cors` en el archivo `main.bicep`). Cuando esto se activa, el proxy frontal de Azure (IIS/Nginx/Kudu Front-End) intercepta las peticiones y añade las cabeceras CORS.
   
3. **La Intercepción de Express:**
   En esta aplicación particular, el servidor Node/Express cuenta con un enrutador global y middlewares de captura que procesaban y respondían a cualquier solicitud HTTP entrante, incluyendo las peticiones con método `OPTIONS` (Preflight).
   
4. **El Resultado del Choque:**
   Cuando la petición `OPTIONS` llegaba a Azure App Service, esta era reenviada directamente al contenedor de Node.js. Node/Express, al recibir la petición en su enrutador, respondía de forma inmediata con un estado `200 OK` (o similar) sin que la capa de plataforma de Azure pudiera inyectar o modificar las cabeceras CORS de esa respuesta final. Como Express ya no tenía el middleware de CORS, la respuesta salía limpia de cabeceras, rompiendo la política en el cliente.

---

## 3. Componentes Involucrados

- **`infraestructura/main.bicep`:** Tenía originalmente configurada la sección de CORS de plataforma de Azure (`properties.cors`), lo que creaba una falsa sensación de que el entorno estaba configurado correctamente en el portal.
- **`vtp-transporte-backend-main/src/app.js`:** Carecía de un middleware capaz de inyectar las cabeceras CORS de forma manual tras la limpieza realizada en el commit `b857d08`.
- **Enrutamiento global de Express:** Respondía a peticiones no manejadas de tipo `OPTIONS` (Preflight) de forma directa, impidiendo el funcionamiento correcto del proxy frontal de Azure.

---

## 4. Por qué Ocurría en Producción y no en Desarrollo Local

- **En Producción:** Las peticiones cruzaban dominios reales (`blue-bush-0d9760810.7.azurestaticapps.net` -> `smt-transportes-api.azurewebsites.net`). Al no existir cabeceras CORS en la respuesta final de Express, el navegador bloqueaba las llamadas.
- **En Local:** El archivo `.env` del frontend en desarrollo local configuraba la variable `API_BASE_URL` apuntando a `http://localhost:3000` pero el servidor proxy dinámico de Vite (`vite.config.js`) redirigía el tráfico `/api` internamente en el mismo host (`localhost:5173` -> `localhost:3000`). Para el navegador, las peticiones salían y llegaban al mismo host y puerto de origen (`localhost:5173`), lo que omitía la necesidad de validar políticas de CORS.
