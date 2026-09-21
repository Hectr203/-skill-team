# Fuentes externas investigadas

Las siguientes fichas se basan en documentación pública consultada sin instalar
ni ejecutar repositorios. Los estados de compatibilidad local son `documental`,
no una certificación de runtime.

| Fuente | Evidencia y licencia | Recomendacion |
|---|---|---|
| `microsoft/playwright-mcp` | README oficial; MCP Playwright, MIT según repo | opt-in; Antigravity browser primero, MCP fallback |
| `thedotmack/claude-mem` | README oficial; Apache-2.0; Node >=20; hooks, SQLite/FTS5, Chroma | opt-in; usar herramientas reales `search`, `timeline`, `get_observations` |
| `headroomlabs-ai/headroom` | README oficial; Apache-2.0; CLI/proxy/MCP y SDK | opt-in; no prometer 80%, medir cada corpus |
| `AgriciDaniel/claude-seo` | README oficial; MIT; 25 subskills/18 agentes declarados | adaptar directivas, no copiar instalador ni credenciales |
| `charlie947/social-media-skills` | README oficial; MIT; 17 skills declaradas | adaptar voz y contenido; publicación siempre HITL |
| `cloudflare/security-audit-skill` | Repo público MIT; `skills/security-audit/SKILL.md` y `report-schema.json`; actualización comprobada 2026-09-14 | adaptar contrato y fases; ejecución solo en sandbox aprobado |
| `PleasePrompto/notebooklm-mcp` | fuente solicitada no se ejecutó | documentar como experimental y contingencia; no llamarlo oficial |
| Google Stitch | MCP solicitado, autenticación y paquete deben validarse con documentación Google vigente | prioridad de diseño solo tras aprobación y prueba |
| Emil Kowalski / Anime.js | MIT; skills de diseño y motor de animación | directivas y recetas propias, sin copias extensas |
| `DavidHDev/react-bits` | MIT + Commons Clause; revisar cada componente antes de redistribuir | referencia de componentes, no biblioteca redistribuible |

Skills de seguridad a investigar continuamente: Semgrep/SAST, Gitleaks o
TruffleHog/secretos, OSV-Scanner/npm audit/SCA, Trivy/IaC y DAST de APIs. Cada
adopción requiere licencia, mantenimiento, permisos, aislamiento y prueba
read-only documentados. `skills/SkillSpector` local es una referencia útil para
revisar skills, no una tercera agencia.
