# Servidor MCP: claude-mem (Memoria Persistente Universal)

- **Repositorio oficial**: [github.com/thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)
- **Licencia**: Apache-2.0
- **Propósito**: Proveer memoria persistente a largo plazo multicapa y compartida para cualquier modelo o plataforma de IA (Google Antigravity, Claude Code, OpenCode, Cursor, Cline).

## Herramientas Expuestas
- `mem:search`: Búsqueda híbrida (FTS5 en SQLite + vectores de Chroma) en el historial de tareas del proyecto.
- `mem:recall` / `get_observations`: Recuperación detallada de observaciones específicas sin reinyectar logs completos.
- `mem:timeline`: Consulta de la secuencia cronológica de decisiones y cambios.
- `mem:forget`: Purga de memorias obsoletas o descartadas a solicitud del usuario.
- `mem:stats`: Métricas de almacenamiento y tamaño de memoria.

## Configuración Universal (`mcp_config.json`)
```json
{
  "mcpServers": {
    "claude-mem": {
      "command": "npx",
      "args": ["-y", "claude-mem", "mcp"]
    }
  }
}
```

## Fallback en Markdown
Si el servidor MCP no está activo, los agentes consultan y actualizan automáticamente el volcado de memoria en:
`contexts/projects/<project-id>/memoria.md` o los scripts en `scripts/arranque.py` y `scripts/cierre.py`.
