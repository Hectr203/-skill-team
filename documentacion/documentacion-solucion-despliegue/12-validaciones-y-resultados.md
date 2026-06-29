# 12 — Validaciones y Resultados

Este documento describe las pruebas ejecutadas para validar el comportamiento del sistema tras implementar las soluciones técnicas, incluyendo las trazas de red resultantes y la confirmación del correcto funcionamiento del flujo en producción.

---

## 1. Validación de CORS mediante Curl (Preflight OPTIONS)

Para verificar que el backend responda correctamente a las peticiones CORS sin depender de un navegador, se realizó una petición HTTP simulada desde la terminal local apuntando al endpoint productivo:

```bash
curl -i -X OPTIONS 'https://smt-transportes-api.azurewebsites.net/api/auth/forgot-password' \
  -H 'Origin: https://blue-bush-0d9760810.7.azurestaticapps.net' \
  -H 'Access-Control-Request-Method: POST' \
  -H 'Access-Control-Request-Headers: content-type'
```

### Respuesta del Servidor (Validada):
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

### Análisis del Resultado:
- **Código `204 No Content`:** Express interceptó la petición OPTIONS y la finalizó exitosamente sin intentar buscar una ruta `OPTIONS /api/auth/forgot-password` en el enrutador de controladores de Express.
- **`Access-Control-Allow-Origin`:** Contiene exactamente el origen del frontend autorizado en producción (`https://blue-bush-0d9760810.7.azurestaticapps.net`).
- **`Access-Control-Max-Age: 86400`:** Le indica al navegador que puede cachear esta validación de CORS durante 24 horas, evitando tener que realizar peticiones `OPTIONS` redundantes antes de cada `POST`/`GET` subsecuente, lo cual optimiza notablemente la latencia y rendimiento percibidos por el usuario final.

---

## 2. Validación en el Entorno del Cliente (Navegador)

Tras el redespliegue del backend:
1. Se accedió al sitio web de producción: `https://blue-bush-0d9760810.7.azurestaticapps.net/forgot-password`.
2. Se introdujo una dirección de correo válida en el formulario de recuperación.
3. Se presionó el botón de enviar.
4. **Comportamiento:**
   - La petición preflight `OPTIONS` fue enviada por el navegador y retornó un código `204` con cabeceras CORS válidas.
   - De inmediato, el navegador liberó la petición real `POST /api/auth/forgot-password`.
   - El servidor Express procesó la solicitud, envió el correo electrónico de recuperación de contraseña a través del servicio SMTP de Gmail configurado, y retornó un código de estado exitoso al frontend.
   - La interfaz de Vue.js mostró el mensaje de confirmación sin reportar fallos de red en consola.

---

## 3. Matriz de Resultados (Antes / Después)

| Funcionalidad | Comportamiento con Fallo (Antes) | Comportamiento Corregido (Después) | Estado |
|---|---|---|---|
| **Petición Preflight (`OPTIONS`)** | Código `200 OK` sin cabeceras `Access-Control-Allow-Origin`. | Código `204 No Content` con cabeceras CORS dinámicas correctas. | **Éxito** |
| **Envío de `POST` Cruzado** | Bloqueado por el navegador (`Failed to fetch`). | Permitido y procesado por el backend de manera segura. | **Éxito** |
| **Recuperación de Contraseña** | La interfaz mostraba error de conexión. | Se envía el correo de recuperación exitosamente en producción. | **Éxito** |
| **CORS en Desarrollo Local** | Operaba con normalidad mediante el proxy Vite. | Sigue operando con normalidad usando el proxy de desarrollo local. | **Éxito** |
