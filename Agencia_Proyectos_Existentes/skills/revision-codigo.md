# Skill: Revision de Codigo

## Proposito
Evaluar cambios para detectar defectos antes de cierre o merge.

## Base principal
- `Agencia_Proyectos_Existentes/skills/agent-skills/skills/code-review-and-quality/SKILL.md`
- `Agencia_Proyectos_Existentes/skills/agent-skills/agents/code-reviewer.md`

## Rol en el sistema
Esta skill es la capa local de revision del proyecto. Toma la metodologia del nucleo y la aplica sobre el diff o PR concreto sin duplicar criterios de revision.

## Cuando usar
- PRs.
- Cambios criticos.
- Refactorizaciones.
- Correcciones de bugs importantes.

## Procedimiento
1. Leer el requerimiento o spec antes de opinar.
2. Revisar las pruebas primero.
3. Evaluar correctitud, legibilidad, arquitectura, seguridad y rendimiento.
4. Clasificar hallazgos por severidad y proponer el fix minimo.

## Salidas
- Hallazgos accionables.
- Recomendaciones.
- Veredicto o riesgo residual.
