# Skill: Refactorizacion Controlada

## Proposito
Mejorar codigo existente sin cambiar comportamiento observable.

## Base principal
- `Agencia_Proyectos_Existentes/skills/agent-skills/skills/code-simplification/SKILL.md`
- Apoyo de ejecucion gradual: `Agencia_Proyectos_Existentes/skills/agent-skills/skills/incremental-implementation/SKILL.md`

## Rol en el sistema
Esta skill traduce el principio de simplificacion del nucleo a cambios pequenos y verificables dentro del proyecto.

## Cuando usar
- Deuda tecnica concreta.
- Duplicacion.
- Codigo dificil de probar.
- Simplificacion necesaria para implementar un cambio.

## Procedimiento
1. Definir comportamiento a preservar.
2. Identificar pruebas o validacion manual.
3. Separar refactorizacion de funcionalidad nueva.
4. Cambiar en pasos pequenos.
5. Verificar no regresion.

## Salidas
- Codigo simplificado.
- Evidencia de no regresion.
- Riesgos residuales.
