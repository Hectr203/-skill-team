# Registro y Catálogo de Servidores MCP

Este registro formaliza las capacidades, herramientas, permisos y protocolos de respaldo para cada servidor MCP integrado en la Agencia de Proyectos.

---

## Matriz de Servidores MCP

| Servidor | Paquete / Fuente | Propósito y Etapa | Agentes Autorizados | Herramientas Expuestas | Plan de Contingencia / Fallback |
|---|---|---|---|---|---|
| **agencia** | `scripts/agencia_mcp.py` (Nativo) | Motor operativo, Context Engine, memoria, estado y compuertas HITL | Todos los agentes y clientes MCP | `agencia_arranque`, `agencia_cierre`, `agencia_doctor`, `agencia_estado`, `agencia_nuevo`, `agencia_validar` | CLI unificado local `python3 scripts/agencia.py` |
| **claude-mem** | `claude-mem` ([github.com/thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)) | Memoria persistente multicapa universal (inicio y cierre de tareas) | Asistente Principal, todos los agentes | `mem:search`, `mem:recall`, `mem:timeline`, `mem:forget`, `mem:stats` | Volcado sincronizado en Markdown (`contexts/projects/<id>/memoria.md`) y scripts locales (`scripts/arranque.py`, `scripts/cierre.py`) |
| **stitch-mcp** | `@_davideast/stitch-mcp` | Diseño rápido *design-to-code* y extracción de tokens de interfaz | Agente Diseño/Motion, Frontend, Arquitecto | `list_projects`, `list_screens`, `get_screen`, `extract_tokens` | Prototipado manual con Atomic Design, `ui-ux-pro-max` y design tokens locales |
| **headroom** | `headroom-ai` ([github.com/headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom)) | Compresión semántica en tiempo real de logs y diffs masivos | Todos los agentes vía orquestador | `headroom_compress`, `headroom_retrieve`, `headroom_stats` | Truncamiento inteligente local con preservación de stack traces y líneas de error |
| **playwright** | `@playwright/mcp@latest` (Microsoft) | Automatización web, pruebas deterministas E2E y accesibilidad | Agente Web Testing, QA, Frontend | `navigate`, `click`, `fill`, `screenshot`, `evaluate` | **Prioridad 1**: Navegador integrado de Google Antigravity IDE; Playwright MCP como fallback universal |
| **notebooklm** | `notebooklm-mcp@latest` ([github.com/PleasePrompto/notebooklm-mcp](https://github.com/PleasePrompto/notebooklm-mcp)) | Interrogación documental profunda de fuentes extensas con citas | Agente Documentación, Arquitecto | `query_notebook`, `search_sources`, `get_citations` | Extracción estructurada con Scrapling o API de Google Gemini / Vertex AI |
| **auto-crm** | Auto-CRM local ([github.com/hainrixz/auto-crm](https://github.com/hainrixz/auto-crm)) | Consulta conversacional de leads y pipeline comercial en SQLite | Agente CRM, Director de Proyecto | `/pipeline`, `/deals`, `/summary` | Consultas directas a base de datos local SQLite (`data/crm.db`) sin conexión externa |

---

## Reglas de Seguridad y Human-in-the-Loop para MCP
1. **Protección de Credenciales**: Ningún token, API key ni secreto se escribe en configuraciones versionadas; residen exclusivamente en variables de entorno locales (`.env` no versionado).
2. **Acceso de Solo Lectura por Defecto**: Las herramientas de búsqueda, compresión y consulta operan de forma autónoma. Cualquier mutación externa (envío de correos, transacciones, cambios de DNS) requiere aprobación explícita humana.
3. **Persistencia Compartida**: `claude-mem` comparte la misma base de datos local SQLite entre Google Antigravity, Claude Code, Cursor y OpenCode para mantener memoria continua cross-sesión.
