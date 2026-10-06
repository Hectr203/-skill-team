# Servidor MCP: Auto-CRM (Consultas Comerciales Privadas)

- **Repositorio oficial**: [github.com/hainrixz/auto-crm](https://github.com/hainrixz/auto-crm)
- **Licencia**: MIT
- **Propósito**: Interfaz conversacional privada para consultar y actualizar el pipeline comercial local en SQLite sin enviar datos a plataformas SaaS externas.

## Comandos y Herramientas Expuestas
- `/pipeline`: Visualización del embudo de ventas actual y distribución de prospectos por etapa.
- `/deals`: Lista de oportunidades activas, montos y días de estancamiento.
- `/summary`: Resumen ejecutivo de conversión, valor total del pipeline y próximos pasos comerciales.

## Configuración (`mcp_config.json`)
```json
{
  "mcpServers": {
    "auto-crm": {
      "command": "node",
      "args": ["services/crm/mcp-server.js"],
      "env": {
        "CRM_DATABASE_URL": "file:./data/crm.db"
      }
    }
  }
}
```

## Tratamiento Desacoplado
Auto-CRM opera como módulo complementario; no se impone su stack en proyectos que no requieran gestión comercial.
