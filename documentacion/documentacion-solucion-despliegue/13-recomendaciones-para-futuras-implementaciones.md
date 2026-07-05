# 13 — Recomendaciones para Futuras Implementaciones

Este documento presenta una serie de lecciones aprendidas y mejores prácticas arquitectónicas, de infraestructura y de despliegue derivadas de la resolución de problemas en el proyecto **VTP Transporte**, con la finalidad de prevenir fallos similares y optimizar el desarrollo futuro.

---

## 1. Prevención de Errores de CORS

- **CORS Centralizado:** Se aconseja fuertemente mantener el manejo de CORS en el código fuente del backend en lugar de distribuirlo o delegarlo en la plataforma del proveedor de nube. Esto garantiza portabilidad y evita que cambios en la configuración del proxy de la nube rompan de forma silenciosa la aplicación.
- **Validación Estricta de Orígenes:** No utilizar comodines (`*`) en producción. Siempre utilizar variables de entorno para poblar la lista blanca de orígenes permitidos.
- **Evitar Cabeceras Duplicadas:** Si se centraliza CORS en la aplicación, se debe garantizar que los filtros de CORS del App Service o del API Gateway estén apagados para el origen cruzado de modo que no dupliquen cabeceras en peticiones simples.

---

## 2. Gestión de Entornos y Desacoplamiento (Local vs Nube)

- **Proxy Local de Vite:** Mantener la configuración de `vite.config.js` para simular llamadas locales mediante proxies. Esto simplifica el desarrollo inicial, pero es mandatorio simular peticiones con dominios cruzados en la fase de pruebas previas al lanzamiento (staging) para validar las políticas de CORS del servidor.
- **Configuración Dinámica:** Asegurarse de que ninguna URL o IP productiva quede hardcodeada en el código fuente. Toda ruta de API o dirección IP externa debe leerse a través de `process.env`.

---

## 3. Administración Segura de Infraestructura (Bicep)

- **Versionado de IaC:** Mantener el archivo `main.bicep` sincronizado en el control de versiones (Git) y evitar hacer modificaciones directas manuales en Azure Portal. Los cambios manuales generan un fenómeno conocido como *Infrastructure Drift* (desviación de infraestructura), lo cual causa que futuras ejecuciones de `azd provision` cancelen o sobreescriban configuraciones operativas.
- **Uso de Parámetros Seguros:** Todo secreto, llave criptográfica o contraseña de bases de datos debe declararse como `@secure()` en Bicep, evitando escribir valores sensibles en texto plano en el repositorio.

---

## 4. Gestión de Secretos en Producción

- **Azure Key Vault:** Para proyectos en crecimiento o corporativos, se recomienda migrar el almacenamiento de variables sensibles de la sección *App Settings* hacia un almacén seguro administrado como **Azure Key Vault**. Los secretos en Key Vault se pueden referenciar en Bicep y en el App Service mediante identidades administradas (Managed Identities) de forma nativa sin exponer las contraseñas en variables de entorno legibles por cualquier desarrollador con accesos de consola.

---

## 5. Observabilidad y Diagnóstico Continuo

- **Monitoreo APM:** Utilizar activamente Application Insights (ya aprovisionado por `main.bicep`). Configurar alertas para monitorear errores de conexión de base de datos (`connect ETIMEDOUT`) y respuestas con código HTTP `4xx` y `5xx`.
- **Registro de Preflight:** Monitorear logs de solicitudes `OPTIONS` fallidas para identificar de forma proactiva bloqueos de CORS antes de que afecten a usuarios de manera masiva.
