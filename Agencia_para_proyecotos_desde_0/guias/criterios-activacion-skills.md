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

## Regla
Una skill no sustituye la lectura del proyecto. Toda skill debe adaptarse a las herramientas reales del repositorio.
En proyectos nuevos, `ponytail` nunca debe sobrescribir reglas previas sin diagnostico, propuesta y confirmacion cuando exista riesgo.
