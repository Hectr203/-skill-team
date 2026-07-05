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
| `despliegue-azure-proyecto-existente` | En toda evaluación, preparación, infraestructura, despliegue o diagnóstico Azure. Obliga a analizar primero el repositorio y consume la skill compartida `deploy-azure-cli`. |
| `playwright-mcp-testing` | Para pruebas E2E, regresion e integracion con Playwright en proyectos existentes. Se adapta al framework de pruebas actual. |
| `mejora-asesor` | Para auditoria de codigo y mejora controlada con dos modelos. El modelo caro planifica, el barato ejecuta. Conserva la arquitectura existente. |
| `agent-skills/skills/test-driven-development/SKILL.md` | TDD para proyectos existentes. Red/Green/Refactor respetando el setup actual. |
| `agent-skills/skills/browser-testing-with-devtools/SKILL.md` | Debugging visual con DevTools MCP en el proyecto actual. |
| `agent-skills/skills/code-review-and-quality/SKILL.md` | Revision de codigo en 5 ejes. Complemento de `revision-codigo`. |
| `agent-skills/skills/code-simplification/SKILL.md` | Simplificacion de codigo conservando comportamiento. |
| `agent-skills/skills/security-and-hardening/SKILL.md` | Endurecimiento de seguridad OWASP. Complemento de `seguridad`. |
| `agent-skills/skills/api-and-interface-design/SKILL.md` | Diseno contract-first para APIs. |
| `agent-skills/skills/spec-driven-development/SKILL.md` | Especificaciones antes de codigo. Para funcionalidades grandes o riesgosas. |
| `agent-skills/skills/incremental-implementation/SKILL.md` | Implementacion por slices. Para cambios seguros en proyectos existentes. |
| `agent-skills/skills/context-engineering/SKILL.md` | Gestion de contexto. Complemento de `ahorro-contexto`. |
| `agent-skills/skills/frontend-ui-engineering/SKILL.md` | Ingenieria de UI. Complemento de `ui-ux-pro-max`. |
| `agent-skills/skills/ci-cd-and-automation/SKILL.md` | Pipelines CI/CD adaptados al proyecto. |
| `agent-skills/skills/documentation-and-adrs/SKILL.md` | ADRs y documentacion. Complemento de `documentacion-tecnica`. |

## Regla
Una skill no sustituye la lectura del proyecto. Toda skill debe adaptarse a las herramientas reales del repositorio.
En proyectos existentes, `ponytail` nunca debe sobrescribir reglas previas sin diagnostico, propuesta y confirmacion cuando exista riesgo.
