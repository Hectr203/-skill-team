# Skill: Conservacion de Estructura Actual

## Proposito
Evitar cambios innecesarios de carpetas, capas, tecnologia o estilo.

## Correspondencia en `agent-skills`
No existe una skill exacta para conservar estructura actual.

## Referencia mas cercana
- `Agencia_Proyectos_Existentes/skills/agent-skills/skills/incremental-implementation/SKILL.md`
- `Agencia_Proyectos_Existentes/skills/agent-skills/skills/code-simplification/SKILL.md`

## Rol en el sistema
Esta skill es una regla de prudencia del proyecto. La referencia del nucleo mas cercana es la de cambios pequenos y verificables, pero el objetivo local aqui es preservar la forma existente del repo.

## Cuando usar
- Cuando el proyecto ya tiene una estructura funcional.
- Cuando el cambio solicitado es localizado.
- Cuando hay riesgo de alterar contratos existentes.

## Procedimiento
1. Buscar el lugar natural del cambio.
2. Reutilizar patrones cercanos.
3. Evitar renombres o movimientos globales.
4. Documentar excepciones.

## Salidas
- Cambio compatible con la estructura actual.
- Justificacion si se altera algo estructural.
