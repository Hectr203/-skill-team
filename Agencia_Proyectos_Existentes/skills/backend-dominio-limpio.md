# Skill: Backend por Dominio Limpio

## Proposito
Construir o modificar backend separando responsabilidades segun la arquitectura real del proyecto.

## Correspondencia en `agent-skills`
No existe una skill backend dedicada con el mismo alcance.

## Base mas cercana
- `Agencia_Proyectos_Existentes/skills/agent-skills/skills/api-and-interface-design/SKILL.md`
- Apoyo contextual recomendado: `Agencia_Proyectos_Existentes/skills/agent-skills/skills/context-engineering/SKILL.md`

## Rol en el sistema
Esta skill es la capa local para aplicar separacion de responsabilidades sin imponer una arquitectura nueva. La referencia del nucleo mas cercana es la de diseno de interfaces y limites.

## Cuando usar
- APIs.
- Servicios.
- Casos de uso.
- Repositorios.
- Reglas de negocio.

## Procedimiento
1. Identificar patron backend existente.
2. Ubicar frontera HTTP, negocio y persistencia o equivalentes.
3. Mantener logica de negocio fuera de controladores cuando el proyecto tenga esa separacion.
4. Validar entradas y errores.
5. Probar el flujo afectado.

## Limites
No imponer una arquitectura limpia formal si el proyecto usa otra estructura; adaptar el principio a lo existente.
