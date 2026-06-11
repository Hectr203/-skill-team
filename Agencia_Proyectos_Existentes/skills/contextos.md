# Skill: Contextos

## Proposito
Gestionar informacion estable del proyecto para futuras tareas.

## Base principal
- `Agencia_Proyectos_Existentes/skills/agent-skills/skills/context-engineering/SKILL.md`

## Implementacion local relacionada
- `Agencia_Proyectos_Existentes/skills/ahorro-contexto/SKILL.md`

## Rol en el sistema
Esta skill es la capa de memoria y contexto del proyecto. Usa el enfoque del nucleo para decidir que informacion guardar, como resumirla y como reusarla en sesiones posteriores.

## Cuando usar
- Inicio o cierre de sesiones largas.
- Descubrimiento de reglas importantes.
- Cambios en arquitectura o integraciones.

## Procedimiento
1. Capturar hechos verificados.
2. Registrar fuente.
3. Excluir secretos.
4. Resumir implicaciones.
5. Guardar el cierre en la memoria independiente del proyecto con `scripts/memoria_proyecto.py --proyecto <ruta> close`.

## Salidas
- Inventario de contexto actualizado.
- Resumen ejecutivo reutilizable.
- Entrada en `.memoria/` del proyecto activo.
