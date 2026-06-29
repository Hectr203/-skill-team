# Lectura de Proyecto Existente

## Objetivo
Guiar la comprension inicial de cualquier proyecto ya avanzado antes de modificarlo.

## Orden recomendado de lectura
1. Archivos raiz: `README`, `package`, `pyproject`, `composer`, `pom`, `go.mod`, `Cargo`, `Dockerfile`, `docker-compose`, archivos de entorno de ejemplo y configuraciones principales.
2. Estructura de carpetas: identificar frontend, backend, servicios, scripts, migraciones, tests y documentacion.
3. Convenciones locales: nombres, estilo, capas, patrones, componentes, servicios, repositorios, rutas y controladores.
4. Puntos de entrada: servidor, aplicacion principal, router, CLI, workers, jobs o funciones cloud.
5. Base de datos: modelos, migraciones, seeds, repositorios, consultas y reglas de integridad.
6. Pruebas: framework usado, comandos, cobertura y patrones de mocks.
7. Documentacion funcional: reglas de negocio, ADRs, tickets, guias operativas y comentarios relevantes.
8. Entrega y operación: pipelines, infraestructura como código, contenedores, artefactos, variables de build/runtime, puertos, health checks, almacenamiento, jobs, observabilidad y despliegues previos.

## Resultado esperado
Al terminar la lectura, el agente debe poder responder:
- Que tecnologias usa el proyecto.
- Como esta organizada la arquitectura.
- Donde vive la funcionalidad afectada.
- Que patrones deben respetarse.
- Que riesgos existen si se cambia esa zona.
- Que pruebas o validaciones son necesarias.
- Cómo se construye, inicia, configura y opera cada componente.
- Qué datos siguen desconocidos o presentan evidencia conflictiva.

## Regla de conservacion
Si el proyecto ya tiene una forma consistente de resolver un problema, se debe seguir esa forma aunque no sea la preferencia generica del agente.
