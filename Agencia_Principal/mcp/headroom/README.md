# Servidor MCP: Headroom (Compresión Semántica en Tiempo Real)

- **Repositorio oficial**: [github.com/headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom)
- **Licencia**: Apache-2.0
- **Propósito**: Comprimir en tiempo real la salida de comandos largos, volcados de terminal, logs masivos y diffs de git, logrando hasta un 80% de ahorro de tokens sin perder información crítica ni stack traces.

## Herramientas Expuestas
- `headroom_compress`: Comprime bloques de texto extensos reteniendo líneas críticas (FATAL, ERROR, excepciones).
- `headroom_retrieve`: Recupera fragmentos originales específicos no comprimidos cuando sea necesario.
- `headroom_stats`: Reporta la tasa de compresión efectiva y los tokens ahorrados acumulados.

## Configuración (`mcp_config.json`)
```json
{
  "mcpServers": {
    "headroom": {
      "command": "npx",
      "args": ["-y", "headroom-ai", "mcp"]
    }
  }
}
```

## Modo Wrapper Alternativo
Compatible con ejecución transparente por terminal:
```bash
headroom wrap pytest
headroom wrap npm test
```
