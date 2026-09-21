# Inventario y matriz de integracion

## Resolucion de la tercera agencia

El directorio comun contiene dos agencias con `asistente-principal.md`, agentes,
skills, flujos y plantillas: `Agencia_para_proyectos_desde_0` y
`Agencia_Proyectos_Existentes`. No existe una tercera carpeta claramente
relacionada. `deploy-azure-cli` es un recurso de despliegue, `ponytail` es una
skill/proyecto de referencia, `skills/SkillSpector` es un analizador de skills y
`skills/` es un catálogo compartido. Seleccionar cualquiera como tercera agencia
por nombre seria incorrecto y no cambia el resultado.

## Resumen comparativo

| Elemento | Desde cero | Existentes | Decision | Motivo |
|---|---|---|---|---|
| Orquestador | Greenfield, SDD, loops y stack fuerte | Brownfield, memoria por proyecto y conservacion | Unificar/adaptar | Clasificador unico con dos ramas en `asistente-principal.md` |
| Arquitectura | React + Node/Express + PostgreSQL/Prisma | Respeta stack hallado | Conservar ambos | Predeterminado solo para nuevo; preservación en brownfield |
| Agentes | requerimientos, DB, diseño, Azure, QA | análisis, integracion, refactor, mantenimiento | Unificar | 15 agentes con contratos formales en `agentes/` |
| Ponytail | completo y portable | reglas de no imposicion | Conservar/adaptar | Skill transversal en `skills/engineering/ponytail/` |
| Memoria y Contexto | CloudMem/Mem Palace local | `.memoria/` por proyecto | Unificar suite | Graphify + claude-mem + Headroom + `ahorro-contexto` y scripts locales |
| Asesoría y Calidad | improve y mejora-asesor bi-modelo | wrapper equivalente | Integrar ambos | `improve` (read-only) + `mejora-asesor` (modelo caro/barato) |
| Testing y Browser | Playwright MCP testing | Adaptador al framework existente | Integrar ambos | Navegador Antigravity nativo + `playwright-testing` + `playwright-mcp-testing` |
| Despliegue Cloud | despliegue-azure-nuevo | despliegue-azure-existente | Integrar ambos | Ambos adaptados en `skills/deployment/` con Azure CLI |
| agent-skills (Google/Addy) | catálogo 23 skills | mismo catálogo | Integrar completo | 23 skills de Addy Osmani en `skills/agent-skills/` |
| UI/UX Pro Max | Motor de diseño con CSVs y scripts | Directivas de diseño | Integrar completo | `skills/design-and-motion/ui-ux-pro-max/` con data y scripts |
| Notificaciones y HITL | scripts y avisos locales | `notificacion-finalizacion` | Integrar completo | `skills/notifications/` y scripts en `scripts/` |
| Redux / Estado Global | React state / Zustand | Reglas de estado mínimo | Crear e integrar | `skills/engineering/redux/` para gestión predecible de estado |
| Commits y Creador | commits-espanol y creador | guías equivalentes | Integrar ambos | `skills/commits-espanol/` y `skills/creador-de-habilidades/` |

## Auditoria por recurso

Los inventarios de ambas agencias fueron auditados exhaustivamente. Se incorporaron todas las herramientas funcionales, scripts operativos y catálogos de habilidades, unificándolos bajo estándares nativos de Google Antigravity (YAML frontmatter) y eliminando dependencias de rutas externas:

| Familia | Elementos Integrados | Calidad | Accion Realizada | Destino en Agencia Unificada |
|---|---|---|---|---|
| Flujos | nuevo, existente, auditoría, urgente, producción | Alta | Unificados y adaptados | `flujos/` |
| Agentes | 15 roles especializados con contrato | Alta | Formalizados con contrato | `agentes/` |
| agent-skills (Addy Osmani) | 23 skills de ingeniería de Google | Alta (Upstream) | Integrados completos | `skills/agent-skills/skills/` |
| UI/UX Pro Max | Data CSVs (12 archivos), scripts (3), SKILL | Alta | Integrado completo | `skills/design-and-motion/ui-ux-pro-max/` |
| Notificaciones | Script ejecutable, HTML y SKILL.md | Alta | Integrado completo | `scripts/` y `skills/notifications/` |
| Asesoría Dual | improve upstream + mejora-asesor | Alta | Integrados ambos | `skills/audit-and-security/` |
| Despliegue Azure | nuevo y existente (Azure CLI) | Alta | Integrados ambos | `skills/deployment/` |
| Ahorro Contexto | scripts de memoria + SKILL.md | Alta | Integrado completo | `skills/context-optimization/ahorro-contexto/` |
| Testing E2E | playwright-testing + playwright-mcp-testing | Alta | Integrados ambos | `skills/web-automation/` |
| Estado Global | Redux Toolkit / Zustand con Ponytail | Alta | Creado e integrado | `skills/engineering/redux/` |
| Preservación Brownfield | conservación, lectura-arq, refactor | Alta | Creados e integrados | `skills/existing-projects/` |
| Commits y Creación | commits-espanol, creador-de-habilidades | Alta | Integrados | `skills/` |
