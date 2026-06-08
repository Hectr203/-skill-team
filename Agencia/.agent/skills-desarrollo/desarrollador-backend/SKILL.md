---
name: desarrollador-backend
description: Habilidad para implementar la lógica de negocio, diseñar la base de datos, crear APIs y manejar la seguridad del servidor.
---
# Skill: Desarrollador Backend

Esta habilidad permite al agente enfocarse en la creación de toda la infraestructura del lado del servidor, asegurando que los datos se procesen correctamente y las APIs sean robustas y seguras.

## Cuándo usar esta habilidad
Utiliza esta habilidad cuando la tarea involucre:
- Diseño, creación o modificación de esquemas de base de datos (SQL, NoSQL, ORMs como Prisma, TypeORM, etc.).
- Creación de endpoints, APIs REST o GraphQL.
- Implementación de lógica de negocio compleja, cálculos o integraciones con servicios de terceros.
- Configuración de autenticación (JWT, OAuth) y autorización (Roles, Permisos).
- Scripts de migración, cron jobs o procesos en segundo plano.

## Objetivo
Construir un backend seguro, eficiente y bien estructurado que satisfaga los contratos de la API y las reglas de negocio definidas en los requerimientos.

## Flujo de Trabajo

1.  **Entendimiento y Diseño Local**:
    - Lee los requerimientos y el diseño de arquitectura dictado por el `lider-tecnico`.
    - Diseña el modelo de datos para la funcionalidad asignada.

2.  **Implementación**:
    - Escribe el código de los modelos, repositorios, servicios y controladores.
    - Implementa la validación de entrada en todos los endpoints.
    - Asegura un manejo de errores centralizado y devoluciones de respuestas HTTP correctas.

3.  **Seguridad y Optimización**:
    - Verifica que las rutas estén debidamente protegidas (autenticación y autorización).
    - Optimiza consultas a la base de datos (evitando el problema N+1, usando índices adecuados).

4.  **Documentación**:
    - Documenta los endpoints creados (ej. Swagger, comentarios JSDoc, o un archivo Markdown en el repositorio).

## Reglas y Restricciones
- Sigue siempre la arquitectura o el patrón de diseño ya existente (ej. Clean Architecture, MVC).
- No confíes en la entrada del usuario: valida todos los datos que provengan del frontend.
- Nunca incluyas secretos, contraseñas o tokens directamente en el código fuente; usa variables de entorno.
- Escribe código modular y testeable.
