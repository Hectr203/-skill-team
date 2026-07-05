# Skill: Testing

## Proposito
Definir o ejecutar validaciones proporcionales al riesgo.

## Base principal
- `Agencia_Proyectos_Existentes/skills/agent-skills/skills/test-driven-development/SKILL.md`
- `Agencia_Proyectos_Existentes/skills/agent-skills/agents/test-engineer.md`
- `Agencia_Proyectos_Existentes/skills/playwright-mcp-testing/SKILL.md`

## Rol en el sistema
Esta skill local cubre el trabajo de pruebas del proyecto y aterriza el enfoque TDD/prove-it del nucleo sobre el codigo real que se este cambiando. Se apoya en Playwright MCP para validacion en navegador real y pruebas de API.

## Cuando usar
- Bugs.
- Nueva funcionalidad.
- Refactorizaciones.
- Flujos criticos.
- Regresiones.

## Procedimiento
1. Identificar comportamiento esperado.
2. Elegir nivel de prueba: unitario, integracion, E2E o manual.
3. Si hay navegador involucrado, usar Playwright MCP para pruebas E2E.
4. Cubrir camino feliz, errores y bordes.
5. Ejecutar o documentar pruebas pendientes.
6. Si el proyecto ya tiene framework de pruebas, mantenerlo; Playwright se suma solo para E2E.

## Herramientas
- **Playwright Test** para E2E e integracion.
- **Playwright MCP** para interaccion con navegador real desde el agente.
- **Framework existente** (Jest/Vitest/Mocha) para unitarias, sin cambios.

## Salidas
- Casos de prueba.
- Resultado de validacion.
- Playwright report HTML si se ejecutaron E2E.
- Brechas de cobertura.
