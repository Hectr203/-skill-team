# 03 — Solución Implementada

Este documento expone la estrategia técnica elegida para solucionar el error de CORS de forma definitiva en producción, las alternativas descartadas con sus respectivas justificaciones, y las ventajas y limitaciones del enfoque seleccionado.

---

## 1. La Solución Seleccionada

La solución consistió en **centralizar el manejo de CORS dentro de la propia aplicación Express (a nivel de código de Node.js)** y **desactivar por completo el CORS a nivel de plataforma de Azure App Service**.

### Puntos Clave de la Solución:
- **Middleware CORS Manual:** Se agregó un middleware en `src/app.js` encargado de interceptar todas las peticiones entrantes.
- **Validación Dinámica de Orígenes:** El middleware lee la variable de entorno `CORS_ALLOWED_ORIGINS` (que almacena una lista de dominios permitidos separada por comas) y verifica si la petición proviene de un origen autorizado.
- **Respuesta Inmediata a Preflight (`OPTIONS`):** Si la petición entrante es de tipo `OPTIONS`, el middleware inyecta los encabezados CORS correspondientes y finaliza la petición inmediatamente retornando un estado `204 No Content`, asegurando que no continúe por el enrutador de Express ni retorne un `200` limpio de CORS.
- **Desactivación de CORS en Azure CLI / Bicep:** Se desactivó el CORS de plataforma de Azure para evitar conflictos de cabeceras duplicadas (cuando el frontend realiza peticiones simples de tipo GET que no requieren preflight).

---

## 2. Alternativas Consideradas y Descartadas

### Alternativa A: Mantener el CORS en Azure y modificar Express para omitir OPTIONS
- **Descripción:** Mantener la eliminación del middleware de CORS del código y reconfigurar el servidor Express para no procesar o responder a ninguna petición con el método `OPTIONS`, dejando pasar estas directamente al proxy frontal de Azure.
- **Por qué se descartó:** Express tiene un comportamiento de enrutamiento por defecto que responde a los verbos HTTP no mapeados explícitamente en una ruta. Modificar esto requería alterar profundamente el manejo de errores y enrutamiento global del servidor, lo que aumentaba el riesgo de introducir fallos y hacía que el código fuera menos mantenible. Además, esta alternativa impedía probar peticiones CORS de forma local, ya que la plataforma local de desarrollo no cuenta con el proxy frontal de Azure.

### Alternativa B: Usar el paquete npm `cors` estándar de Express
- **Descripción:** Volver a instalar y configurar el middleware clásico `app.use(cors())`.
- **Por qué se descartó:** Aunque funcional, requería volver a introducir una dependencia externa en `package.json` e incrementar el tamaño del paquete. Implementar el middleware directamente en Node.js de forma manual requiere menos de 15 líneas de código, ofrece control absoluto sobre el ciclo de vida de la petición OPTIONS y reduce las dependencias del proyecto.

---

## 3. Ventajas y Limitaciones de la Solución Seleccionada

### Ventajas:
- **Portabilidad Absoluta:** La lógica de CORS ahora vive en la aplicación Node.js. Si el sistema se migra de Azure a AWS, Docker, Kubernetes o un VPS tradicional con Nginx, el CORS seguirá funcionando exactamente igual sin configuraciones adicionales de la nube.
- **Consistencia en Desarrollo Local:** Permite depurar problemas de CORS directamente en la máquina local si se desactivan temporalmente los proxies de desarrollo.
- **Cero Dependencias Externas:** Se logró sin reinstalar el paquete `cors`, manteniendo el backend liviano.
- **Prevención de Headers Duplicados:** Al apagar el CORS en Azure, evitamos el clásico problema donde se inyectan dos cabeceras `Access-Control-Allow-Origin` para peticiones `GET` (una por Express y otra por Azure), lo cual también es rechazado por los navegadores.

### Limitaciones:
- **Sobrecarga Mínima de CPU:** El backend procesa en la capa de la aplicación la validación de orígenes del preflight, en lugar de descartarlo en el balanceador o proxy frontal de Azure. No obstante, para el volumen de peticiones esperado en este sistema, la sobrecarga es despreciable.
- **Mantenimiento Manual:** Si cambian los dominios permitidos del frontend, se debe asegurar que se actualice la variable de entorno `CORS_ALLOWED_ORIGINS` en el App Service (administrada convenientemente mediante `main.bicep` en los aprovisionamientos).
