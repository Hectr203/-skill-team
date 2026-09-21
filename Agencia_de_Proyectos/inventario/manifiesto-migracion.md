# Manifiesto de migracion

| Origen | Destino | Accion | Justificacion | Estado |
|---|---|---|---|---|
| `Agencia_para_proyectos_desde_0/asistente-principal.md` | `asistente-principal.md` | adaptar | Base greenfield, loops y compuertas | validado por lectura |
| `Agencia_Proyectos_Existentes/asistente-principal.md` | `asistente-principal.md` | adaptar | Clasificacion brownfield y preservacion | validado por lectura |
| `*/flujos/*` | `flujos/` | unificar | Conserva fases y bifurcaciones | validado por inspeccion |
| `*/reglas/*` | `reglas/` | unificar | Evita contradiccion entre imposicion y conservacion | validado |
| `*/skills/ponytail/*` | `skills/engineering/ponytail/` | adaptar | Regla transversal portable | validado |
| `*/skills/improve/*` + `.agents/skills/improve` | `skills/audit-and-security/improve/` | adaptar | Fuente read-only senior advisor | validado |
| `*/skills/mejora-asesor/*` | `skills/audit-and-security/mejora-asesor/` | integrar | Flujo bi-modelo (inteligente / económico) | validado |
| `*/skills/playwright-mcp-testing/*` | `skills/web-automation/playwright-mcp-testing/` | integrar | Testing E2E con snapshots y suite completa | validado |
| `*/skills/ahorro-contexto/*` | `skills/context-optimization/ahorro-contexto/` | integrar | Ahorro de tokens con scripts locales | validado |
| `*/skills/agent-skills/*` | `skills/agent-skills/` | integrar | Suite completa de 23 skills de Addy Osmani (Google) | validado |
| `*/skills/ui-ux-pro-max/*` | `skills/design-and-motion/ui-ux-pro-max/` | integrar | Catálogo masivo de diseño con CSVs y scripts | validado |
| `*/skills/notificacion-finalizacion/*` | `skills/notifications/notificacion-finalizacion/` | adaptar | Notificación audible/visual sin dependencias | validado |
| `*/skills/despliegue-azure-*/*` | `skills/deployment/despliegue-azure-*/` | integrar | Despliegue en Azure con Azure CLI | validado |
| `*/skills/commits-espanol/*` | `skills/commits-espanol/` | integrar | Validación y mensajes en español | validado |
| `*/skills/creador-de-habilidades/*` | `skills/creador-de-habilidades/` | integrar | Creación de nuevas skills estandarizadas | validado |
| `*/scripts/*` (notificaciones y memoria) | `scripts/` | integrar | `notificar_tarea.py`, `solicitar_autorizacion.py`, etc. | validado |
| `*/agentes/*` | `agentes/` | reemplazar | 15 roles formales con contrato unificado | validado |

No se mutaron, renombraron, movieron ni eliminaron archivos en las agencias de origen. Todas permanecen 100% de solo lectura.
