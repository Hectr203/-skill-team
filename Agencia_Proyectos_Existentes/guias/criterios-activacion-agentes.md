# Criterios de Activacion de Agentes

| Necesidad | Agente recomendado |
| --- | --- |
| Entender solicitud ambigua, reglas de negocio o alcance | `analista-requerimientos` |
| Analizar un repositorio ya avanzado antes de tocar codigo | `agente-analisis-proyecto-existente` |
| Coordinar tareas mixtas, riesgos y entregables | `asistente-principal` |
| Implementar cambios tecnicos | `engineer` o `agente-desarrollo` |
| Backend, APIs, servicios o dominio | `agente-backend` |
| Frontend, UI, estados, rutas o componentes | `agente-frontend` |
| Base de datos, migraciones o integridad | `agente-base-datos` |
| Revisar correctitud y mantenibilidad | `code-reviewer` |
| Seguridad, permisos, secretos o datos sensibles | `security-editor` |
| Tests, estrategia QA o regresiones | `tester` |
| Documentacion, ADRs o bitacoras | `agente-documentacion` |
| Cambios estructurales o decisiones de arquitectura | `agente-arquitectura` |
| Simplificacion o deuda tecnica controlada | `agente-refactorizacion` |
| APIs externas, colas, webhooks o interoperabilidad | `agente-integracion` |
| Soporte continuo, bugs menores y salud del sistema | `agente-mantenimiento` |
| Resumir, conservar o actualizar conocimiento | `agente-contexto` |
| Analizar preparación, diseñar infraestructura o desplegar en Azure | Primero `agente-analisis-proyecto-existente`; después `agente-despliegue-azure` |

| Auditoria de codigo, mejora controlada o deuda tecnica | `mejora-asesor` (skill de doble modelo: analisis con modelo caro, ejecucion con barato) |
| | |
| Revision con `improve` de shadcn | Ejecutar `/improve` con modelo caro, ejecutar planes con modelo economico |

## Regla de combinacion
Cuando una tarea afecte mas de una capa, el asistente principal debe dividir responsabilidades y mantener un unico criterio de cierre.
