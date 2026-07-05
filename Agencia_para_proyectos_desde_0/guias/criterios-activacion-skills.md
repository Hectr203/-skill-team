# Criterios de Activacion de Skills

| Skill | Cuando usarla |
| --- | --- |
| `contextos` | Al leer, resumir, conservar o actualizar informacion relevante del proyecto. |
| `ahorro-contexto` | Al inicio de toda sesión para recuperar la memoria del proyecto y al cierre para registrar cambios. Obligatoria cuando se trabaja dentro de `proyectos/<nombre>/`. |
| `comunicacion-espanol` | Cuando la salida, documentacion o trazabilidad debe mantenerse en espanol claro. |
| `respuestas-simples` | Para respuestas directas, pasos concretos o explicaciones sin rodeos. |
| `adaptacion-proyectos-existentes` | En toda tarea sobre un repositorio ya iniciado. |
| `lectura-arquitectura-existente` | Antes de cambios que dependan de estructura, capas o convenciones. |
| `conservacion-estructura-actual` | Cuando exista riesgo de reestructurar innecesariamente. |
| `backend-dominio-limpio` | En backend con reglas de negocio, servicios, casos de uso, APIs o repositorios, adaptado al patron local. |
| `ux-pro-max` | En cambios de experiencia de usuario, interfaz, accesibilidad o flujos visuales. |
| `spec-driven-development` | Antes de implementar funcionalidades grandes o ambiguas. |
| `interview` | Cuando faltan datos del cliente o hay ambiguedad critica. |
| `analisis-requerimientos` | Para convertir informacion cruda en requerimientos accionables. |
| `revision-codigo` | Antes de cerrar cambios relevantes o revisar PRs. |
| `seguridad` | En autenticacion, autorizacion, datos sensibles, APIs, validaciones o dependencias. |
| `testing` | Para definir pruebas, cubrir bugs o validar regresiones. |
| `documentacion-tecnica` | Para ADRs, bitacoras, guias y reportes de cierre. |
| `refactorizacion-controlada` | Cuando se deba simplificar sin cambiar comportamiento externo. |
| `creador-habilidades` | Cuando una necesidad recurrente amerite una nueva skill documentada. |
| `referrals` | Cuando el proyecto requiera materiales, mensajes o seguimiento de referidos/candidatos, si aplica al dominio. |
| `ponytail` | Cuando se pida minimalismo, YAGNI, menos sobreingenieria, auditoria de complejidad o integracion segura de reglas de IDE/agente en un repositorio existente. |
| `despliegue-azure-proyecto-nuevo` | Al definir el perfil Azure de un proyecto nuevo, preparar producción, crear infraestructura, desplegar o documentar la operación. Consume la skill compartida `deploy-azure-cli` y respeta el stack obligatorio. |
| `playwright-mcp-testing` | Para pruebas E2E, integracion y regresion con Playwright en proyectos nuevos. Configuracion inicial, estructura de tests y CI. |
| `mejora-asesor` | Para auditoria de codigo, mejora de arquitectura, deteccion de bugs y deuda tecnica. Usa el flujo de dos modelos: caro para analisis, barato para ejecucion. Activa la skill `improve` de shadcn. |
| `agent-skills/skills/test-driven-development/SKILL.md` | TDD classico - Red/Green/Refactor. Para desarrollo guiado por pruebas. |
| `agent-skills/skills/browser-testing-with-devtools/SKILL.md` | Debugging visual con DevTools MCP. Para inspeccion de DOM, console, network y rendimiento. |
| `agent-skills/skills/code-review-and-quality/SKILL.md` | Revision de codigo en 5 ejes. Complemento de `revision-codigo`. |
| `agent-skills/skills/code-simplification/SKILL.md` | Simplificacion de codigo. Complemento de `ponytail` para reduccion de complejidad. |
| `agent-skills/skills/security-and-hardening/SKILL.md` | Endurecimiento de seguridad OWASP. Complemento de `seguridad`. |
| `agent-skills/skills/api-and-interface-design/SKILL.md` | Diseno de APIs contract-first. Para definir interfaces publicas. |
| `agent-skills/skills/spec-driven-development/SKILL.md` | Especificaciones antes de codigo. Para funcionalidades grandes. |
| `agent-skills/skills/incremental-implementation/SKILL.md` | Implementacion por slices verticales. Para cambios que tocan varios archivos. |
| `agent-skills/skills/context-engineering/SKILL.md` | Gestion de contexto para agentes. Complemento de `ahorro-contexto`. |
| `agent-skills/skills/frontend-ui-engineering/SKILL.md` | Ingenieria de UI profesional. Complemento de `ui-ux-pro-max`. |
| `agent-skills/skills/ci-cd-and-automation/SKILL.md` | Pipelines CI/CD. Para automatizar pruebas y despliegue. |
| `agent-skills/skills/documentation-and-adrs/SKILL.md` | ADRs y documentacion tecnica. Complemento de `documentacion-tecnica`. |

## Regla
Una skill no sustituye la lectura del proyecto. Toda skill debe adaptarse a las herramientas reales del repositorio.
En proyectos nuevos, `ponytail` nunca debe sobrescribir reglas previas sin diagnostico, propuesta y confirmacion cuando exista riesgo.
