# Limitaciones y decisiones pendientes

- No se instalaron ni conectaron MCP, Playwright, dependencias ni repositorios
  externos por la instrucción del usuario.
- Google Stitch, Antigravity `agy` y rutas de configuración se documentan como
  adaptadores; la instalación local concreta requiere prueba aprobada.
- `cloudflare/security-audit-skill` sí está publicado bajo MIT. La agencia
  adapta su contrato y fases, pero no copia ni ejecuta el repositorio; la
  operación completa exige el sandbox descrito por upstream.
- Los servidores MCP (Stitch, claude-mem, Headroom, Playwright, NotebookLM, Auto-CRM) están plenamente catalogados y configurados en `mcp/` y `mcp_config.example.json`; su activación en tiempo de ejecución depende de la aprobación y credenciales del usuario.
- `claude-mem` queda integrado como estándar de memoria universal multicapa con soporte para `mem:search`, `mem:recall`, `mem:timeline`, `mem:forget` y `mem:stats`, interoperable con Google Antigravity, Claude Code, Cursor y OpenCode, con respaldo sincronizado en Markdown.
- NotebookLM se mantiene con nota de contingencia documental por estado archivado en upstream, respaldado por extracción estructurada con Scrapling o API de Google Gemini.
- Las suites de Google Stitch, Emil Kowalski, Anime.js, React Bits, Claude SEO, Auto-CRM y Social Media Skills están integradas modularmente como skills de primer nivel sin acoplamiento forzado de stacks.
- Toda acción externa o irreversible se mantiene bajo el control estricto de las compuertas Human-in-the-Loop.
