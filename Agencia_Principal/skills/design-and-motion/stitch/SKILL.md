---
name: google-stitch
description: Use for approved Google Stitch UI ideation, screen inspection, design tokens and design-to-code mapping.
---

## Integración en Agencia Principal
Aplicar el [contrato de selección y coordinación](../../../agentes/contrato-agente.md). Activar esta habilidad solo si su resultado corresponde al alcance autorizado; los ejemplos de stack y herramientas no sustituyen el manifiesto. Recursos relativos se resuelven desde esta fuente. No ampliar permisos, invocar procesos recursivos ni declarar controles no ejecutados.

# Google Stitch
Adaptador y suite oficial de diseño para Google Stitch en la Agencia.

Para el flujo de trabajo completo, mitigación de límites de tokens con `upload_to_stitch.py`, estructuración de prompts y conversión a React:
- Consulta la [Guía Operativa de Google Stitch Skills](../../stitch-skills/GUIA-STITCH-AGENCIA.md).
- Usa [stitch-generate-design](../../stitch-skills/skills/stitch-generate-design/SKILL.md) para generar pantallas y variantes.
- Usa [stitch-react-components](../../stitch-skills/skills/stitch-react-components/SKILL.md) para desacoplar pantallas en componentes modulares.
- Si Google Stitch MCP no está configurado, recurre al catálogo local `ui-ux-pro-max` y `styles/tokens.css`.

