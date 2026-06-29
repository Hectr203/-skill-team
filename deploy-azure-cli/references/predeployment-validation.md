# Validaciones previas al despliegue

## Formato de cada hallazgo

Registrar:

1. severidad: bloqueante, alta, media o informativa;
2. componente y evidencia;
3. comportamiento local y comportamiento esperado en Azure;
4. causa técnica;
5. corrección general, no una receta rígida;
6. forma de verificar antes y después.

## Configuración y seguridad

- Detectar credenciales, tokens, llaves, cadenas de conexión y datos personales versionados. No mostrar valores.
- Detectar URLs locales, `localhost`, loopback, IPs y rutas absolutas incorporadas.
- Comparar variables utilizadas contra variables provistas en cada entorno.
- Distinguir secretos de configuración no sensible y valores públicos compilados.
- Verificar que los secretos se obtengan en runtime cuando el framework lo permita.
- Preferir identidad administrada y referencias a Key Vault frente a credenciales compartidas.
- Verificar TLS, certificados, dominios, expiración, políticas de acceso y mínimo privilegio.
- Rechazar reglas `0.0.0.0/0`, acceso público general o “permitir todos los servicios Azure” como valor por defecto. Aceptarlos solo con justificación y riesgo explícito.

La infraestructura de referencia contenía credenciales con apariencia real dentro de App Settings declarativos. Convertir esta experiencia en una regla: inspeccionar IaC y configuración como código fuente sensible, redactar hallazgos y rotar credenciales expuestas.

## Build, artefacto y arranque

- Reproducir mentalmente o ejecutar, tras autorización, el build desde un entorno limpio usando el lockfile.
- Confirmar versión de runtime, arquitectura, dependencias nativas y salida real.
- Verificar que el contexto desplegado incluya archivos requeridos y excluya secretos, cachés y dependencias locales incorrectas.
- Confirmar directorio de trabajo y comando de inicio.
- Confirmar que el proceso escuche en todas las interfaces necesarias y en el puerto que la plataforma inyecta.
- No fijar `PORT` sin comprobar el contrato del servicio elegido.
- Asegurar que el proceso principal permanezca en foreground y gestione señales de terminación.
- Verificar health/readiness y que el arranque no falle permanentemente por una dependencia transitoria.
- Si se usa build remoto de App Service, comprobar explícitamente su configuración; no asumir que una carga ZIP instala o compila dependencias.

## Frontend, URL de API y SPA

- Determinar si el frontend es estático, SSR o híbrido antes de elegir hosting.
- Buscar llamadas de red y calcular la URL final usada por el navegador.
- Comprobar que no queden URLs locales ni rutas relativas que dependan de un proxy inexistente.
- Confirmar cuándo se resuelve la variable de API: build o runtime.
- Verificar fallback de rutas SPA, archivos estáticos, base path, caché y errores 404 al recargar rutas profundas.
- Confirmar HTTPS, dominio final y política de contenido si existe.

## Regla específica para React/Vite y otros builds Vite

Revisar `vite.config.*`, archivos `.env*` no secretos y usos de `import.meta.env`:

- Tratar `server.proxy` como ayuda de desarrollo, no como infraestructura productiva.
- Comprobar que el bundle productivo no dependa del target local del proxy.
- Exigir prefijo público `VITE_` para variables expuestas al cliente, salvo configuración explícita distinta de `envPrefix`.
- Confirmar que la URL de API esté disponible durante el build; cambiar App Settings después no modifica un bundle ya compilado.
- Evitar colocar secretos en variables `VITE_*`: quedan visibles en el JavaScript entregado.
- Verificar desarrollo y producción por separado.
- Configurar el origen real del frontend en el propietario de CORS elegido.

Aplicar el mismo principio a otros bundlers: identificar su prefijo público y el momento de sustitución.

## CORS

Determinar un único propietario efectivo de CORS: aplicación, gateway/reverse proxy o plataforma. Evitar capas simultáneas que produzcan cabeceras duplicadas o políticas divergentes.

Validar:

- origen exacto, sin confundir URL con ruta;
- métodos, cabeceras y credenciales;
- respuesta preflight `OPTIONS`;
- `Vary: Origin` cuando el origen sea dinámico;
- ausencia de comodín con credenciales;
- dominios de producción y staging;
- orden de middleware y rutas;
- respuestas de error, no solo respuestas exitosas.

Lección generalizada de la referencia: un proxy de Vite ocultó CORS en local, mientras el backend y el CORS de App Service competían por `OPTIONS` en producción. No imponer siempre CORS en la aplicación; reproducir el flujo real, elegir una capa responsable y desactivar las demás.

## Datos, persistencia y migraciones

- Confirmar motor, versión, extensiones, collation, zona horaria y compatibilidad del driver.
- Confirmar cifrado, DNS, puerto, pool, límites, reintentos y timeouts.
- No recomendar un timeout fijo universal. Ajustarlo con evidencia de latencia y usar reintentos con backoff cuando sean seguros.
- Evitar bloquear todo el servidor durante el arranque si la arquitectura puede ofrecer readiness separado; no ocultar una dependencia esencial rota.
- Confirmar que archivos subidos no residan únicamente en filesystem efímero o por instancia.
- Revisar migraciones y seeders como operaciones independientes del despliegue.
- Exigir inventario de cambios, dry-run si existe, backup/PITR, compatibilidad hacia atrás, responsable, ventana y rollback.
- No ejecutar resets ni seeders destructivos en producción.

## Procesos especiales

- Workers: comprobar idempotencia, visibilidad, reintentos, poison messages y apagado seguro.
- Jobs programados: comprobar zona horaria, solapamiento, singleton y recuperación.
- Tiempo real: comprobar WebSockets, afinidad, duración, límites y escalado.
- Contenedores: comprobar usuario no root, puertos, health, filesystem, imagen inmutable y registro.
- Servicios externos: comprobar allowlists, egress, DNS, cuotas, callbacks y secretos.

## Validación posterior que debe planearse antes

Definir criterios concretos:

- recurso provisionado y configuración efectiva;
- revisión de logs de arranque sin secretos;
- health/readiness;
- conectividad a cada dependencia;
- migraciones y versión de esquema;
- flujo frontend→API;
- preflight CORS desde el origen real;
- recarga de ruta SPA;
- carga/lectura de archivos;
- ejecución de worker/job;
- telemetría y alertas;
- rollback probado o ejecutable.
