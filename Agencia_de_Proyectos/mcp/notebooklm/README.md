# Servidor MCP: Google NotebookLM (`notebooklm-mcp`)

- **Repositorio de referencia**: [github.com/PleasePrompto/notebooklm-mcp](https://github.com/PleasePrompto/notebooklm-mcp)
- **Propósito**: Conectar agentes con libretas de Google NotebookLM para consultar documentación extensa, especificaciones de arquitectura y PDFs de negocio con citas respaldadas.

## Advertencia de Mantenimiento y Contingencia
- El repositorio upstream fue archivado por su autor original.
- **Modo de Operación**: Operación experimental mediante stdio y Patchright Chromium.
- **Alternativa Directa**: Si el servidor deja de responder, la agencia recurre a extracción estructurada de documentación mediante **Scrapling** o consultas a la API de Google Gemini / Vertex AI.

## Configuración (`mcp_config.json`)
```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "npx",
      "args": ["-y", "notebooklm-mcp@latest"]
    }
  }
}
```
