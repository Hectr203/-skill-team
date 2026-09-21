---
name: despliegue-azure-proyecto-nuevo
description: Integrar arquitectura de despliegue y ejecución en Azure al ciclo de proyectos nuevos de la Agencia SMT. Usar al definir infraestructura, preparar producción, desplegar o documentar proyectos nuevos cuyo stack aprobado es React/TypeScript, Node.js 22/Express/TypeScript y PostgreSQL/Prisma, aplicando la skill compartida deploy-azure-cli sin volver a descubrir ni reemplazar arbitrariamente esas tecnologías.
---

# Desplegar un proyecto nuevo de la Agencia SMT

## Núcleo obligatorio

Leer y aplicar `../../../deploy-azure-cli/SKILL.md` y sus referencias. Este archivo solo adapta su flujo a la agencia; no reemplaza sus reglas de seguridad, Azure CLI, validación ni documentación.

Si la ruta compartida no está disponible, detener el despliegue y reportar la dependencia. No reconstruir una versión parcial de memoria.

## Contexto tecnológico aprobado

Partir de estas decisiones de agencia:

- frontend: React y TypeScript con las librerías aprobadas por la propuesta unificada;
- backend: Node.js 22 LTS, Express.js y TypeScript;
- persistencia: PostgreSQL y Prisma;
- idioma y arquitectura: las reglas vigentes de la agencia.

No repetir un descubrimiento abierto de tecnologías ni proponer sustituirlas. Verificar en el repositorio que la implementación coincide con el manifiesto y registrar desviaciones. Evaluar servicios Azure según requisitos no funcionales, topología real, artefacto, red, costo y restricción de despliegue exclusivo con `az`.

## Momento de activación

Activar en dos momentos:

1. **Diseño inicial:** después de aprobar requerimientos, stack y arquitectura de software; antes de consolidar configuración, persistencia, archivos, jobs o contratos de entorno.
2. **Preparación de entrega:** después de implementar y validar localmente; antes de crear o modificar Azure.

No aprovisionar recursos durante el diseño inicial.

## Flujo adaptado

1. Leer requerimientos, manifiesto y arquitectura aprobada.
2. Derivar perfil de despliegue: SPA o renderizado servidor, API, jobs, tiempo real, almacenamiento, volumen, disponibilidad, seguridad, región y presupuesto.
3. Comparar servicios compatibles. No asumir Static Web Apps o App Service.
4. Registrar la decisión de infraestructura y sus implicaciones para desarrollo.
5. Durante la implementación, exigir puerto configurable, health/readiness, variables por entorno, CORS de un solo propietario, almacenamiento persistente y migraciones Prisma seguras.
6. Ejecutar la compuerta previa de `deploy-azure-cli`; verificar el stack conocido en vez de redescubrirlo.
7. Presentar correcciones y plan Azure CLI. Obtener aprobación humana para costo, producción, red, secretos y migraciones.
8. Aprovisionar, configurar y desplegar únicamente mediante comandos directos `az`.
9. Validar administración, aplicación y experiencia externa.
10. Encargar al agente de documentación la guía final basada en comandos y resultados realmente ejecutados.

## Selección orientativa, no automática

- React SPA: evaluar Static Web Apps frente a Storage static website más entrega perimetral. Descartar cualquier opción que no permita publicar exclusivamente con `az` en el entorno disponible.
- Express/Node: evaluar App Service frente a Container Apps según contenedor, escalado, jobs, red y operación.
- PostgreSQL: evaluar PostgreSQL Flexible Server con conectividad, versión, HA, backup y restauración acordes al entorno.
- Prisma: separar generación/build de migraciones productivas; no ejecutar resets y no acoplar migraciones destructivas al arranque.
- Secretos y acceso: priorizar Managed Identity y Key Vault cuando sean compatibles.
- Observabilidad: dimensionar Application Insights y Log Analytics según necesidad y costo, no por plantilla.

## Entregables

- perfil de despliegue añadido al manifiesto;
- decisión de arquitectura Azure justificada;
- matriz de variables sin valores secretos;
- evaluación previa y correcciones;
- plan y registro de comandos `az`;
- validaciones y rollback;
- documentación operativa final.
