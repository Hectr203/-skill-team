# Servidor MCP: Google Stitch (`stitch-mcp`)

- **Paquete / Integración**: `@_davideast/stitch-mcp` o servidor oficial de Google Stitch
- **Propósito**: Conectar agentes de IA con proyectos de Google Stitch para generar vistas UI/UX a partir de prompts o imágenes, inspeccionar variantes de pantallas y extraer tokens de diseño visual (*design-to-code*).

## Herramientas Expuestas
- `list_projects`: Lista de proyectos activos de Stitch.
- `list_screens`: Lista de pantallas y wireframes dentro de un proyecto.
- `get_screen`: Recuperación del código HTML/React, estilos y estructura de una pantalla específica.
- `extract_tokens`: Extracción estructurada de la paleta de colores, tipografía y espaciado en JSON para sincronizar con Tailwind/CSS/Bootstrap.

## Requisitos y Credenciales
- Acceso habilitado a Stitch API en Google Cloud.
- Autenticación mediante Application Default Credentials (ADC) o API Key en variable de entorno.

## Configuración (`mcp_config.json`)
```json
{
  "mcpServers": {
    "google-stitch": {
      "command": "npx",
      "args": ["-y", "@_davideast/stitch-mcp"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "${GOOGLE_APPLICATION_CREDENTIALS}"
      }
    }
  }
}
```

## Plan de Contingencia
Si las credenciales no están presentes o el servidor no responde, los agentes UI/UX recurren a especificaciones locales y diseño modular mediante la skill `skills/design-and-motion/stitch/SKILL.md` y `ui-ux-pro-max` sin detener el desarrollo.
