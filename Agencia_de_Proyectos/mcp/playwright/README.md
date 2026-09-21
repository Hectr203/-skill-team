# Servidor MCP: Playwright (Automatización Web y Pruebas E2E)

- **Repositorio oficial**: [github.com/microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)
- **Mantenedor**: Microsoft (Licencia MIT)
- **Propósito**: Navegación, interacción y verificación determinista en navegadores web mediante snapshots del árbol de accesibilidad (rápido y sinVision dependiente).

## Regla de Precedencia Estricta
1. **Prioridad 1 (Google Antigravity IDE)**: Usar directamente el control del navegador integrado de Antigravity (navegador Chrome real con captura visual automática en webp).
2. **Prioridad 2 (Fallback Universal)**: En otros entornos (Cursor, Windsurf, Claude Code, VS Code o terminales CLI), activar automáticamente `@playwright/mcp@latest`.

## Herramientas Expuestas
- `navigate`: Carga de URL web.
- `click`: Clic sobre elementos mediante selectores de accesibilidad.
- `fill`: Llenado de campos de formulario.
- `screenshot`: Captura de imagen de la pantalla o elemento.
- `evaluate`: Ejecución segura de JavaScript en el contexto de la página.

## Configuración (`mcp_config.json`)
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```
