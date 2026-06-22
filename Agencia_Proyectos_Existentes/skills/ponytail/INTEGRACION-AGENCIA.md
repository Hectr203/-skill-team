# Integracion de Ponytail en la agencia de proyectos existentes

## Resumen
Ponytail se integra como skill de diagnostico e incorporacion progresiva para repositorios ya iniciados. Su punto de entrada local es `SKILL.md`; las reglas originales se conservan en `skills/`, `AGENTS.md`, adaptadores de IDE y archivos de plugin.

## Funcionamiento confirmado
- El repo original define la regla principal en `skills/ponytail/SKILL.md`.
- Las skills auxiliares son `ponytail-review`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain` y `ponytail-help`.
- `AGENTS.md` contiene una version compacta para agentes que leen instrucciones de proyecto.
- Los manifiestos de Codex y Claude Code apuntan a `hooks/claude-codex-hooks.json`.
- OpenCode usa `.opencode/plugins/ponytail.mjs`, que requiere `hooks/ponytail-instructions.js` y `hooks/ponytail-config.js`.
- Gemini usa `gemini-extension.json` con `AGENTS.md` como contexto.

## Inferencia tecnica
En proyectos existentes, Ponytail no debe instalarse como configuracion global sin revisar primero el repo. Las reglas actuales del equipo pueden tener prioridad y la integracion debe evitar sobrescrituras.

## Recomendacion propuesta
Usar Ponytail como auditor de complejidad y como capa adicional de instrucciones. Preferir archivos nuevos junto a reglas existentes antes que modificar archivos compartidos. Si se requiere fusionar, crear respaldo o documentar una estrategia de reversion.

## Flujo operativo
1. Identificar ruta del proyecto existente.
2. Leer documentacion, reglas de agentes e instrucciones de IDE ya presentes.
3. Detectar adaptadores existentes: `.cursor`, `.windsurf`, `.clinerules`, `.github`, `AGENTS.md`, `.opencode`, `.codex-plugin`, `.claude-plugin`, `gemini-extension.json`.
4. Presentar propuesta de archivos a crear, fusionar u omitir.
5. Esperar confirmacion antes de sobrescribir o modificar archivos existentes.
6. Copiar reglas originales sin traducir ni modificar cuando se creen archivos nuevos.
7. Registrar conflictos, decisiones, respaldos y validaciones en la memoria independiente del proyecto.

## Matriz de adaptadores
| Entorno | Recurso local | Criterio en proyecto existente |
| --- | --- | --- |
| Codex | `.codex-plugin/`, `skills/`, `hooks/`, `assets/` | Validar rutas y hooks antes de instalar. |
| Claude Code | `.claude-plugin/`, `skills/`, `hooks/` | No activar hooks sin revision. |
| OpenCode | `.opencode/`, `opencode.json`, `skills/`, `hooks/` | Fusionar `opencode.json` solo con confirmacion. |
| Gemini / Antigravity | `gemini-extension.json`, `AGENTS.md`, `commands/`, `skills/` | Si existe `AGENTS.md`, proponer bloque o archivo alterno. |
| Cursor | `.cursor/rules/ponytail.mdc` | Agregar archivo nuevo junto a reglas existentes. |
| Windsurf | `.windsurf/rules/ponytail.md` | Agregar archivo nuevo junto a reglas existentes. |
| Cline | `.clinerules/ponytail.md` | No reemplazar si `.clinerules` ya existe como archivo unico. |
| GitHub Copilot | `.github/copilot-instructions.md` | No modificar sin respaldo si ya existe. |
| Kiro | `.kiro/steering/ponytail.md` | Agregar steering separado. |
| Generico | `AGENTS.md` o `skills/ponytail/SKILL.md` | Respetar instrucciones del repo. |

## Prevencion de conflictos
Prioridad: instrucciones del humano, reglas globales de la agencia, reglas y arquitectura preexistentes del proyecto, configuracion del IDE, Ponytail, valores predeterminados.

Ponytail no autoriza reestructuraciones masivas. Sus hallazgos de `ponytail-review` y `ponytail-audit` son propuestas de simplificacion, no cambios automaticos.

## Actualizacion
Para actualizar esta copia, comparar contra el repositorio de referencia `../../ponytail` desde la raiz del workspace, revisar cambios en `skills/`, `AGENTS.md`, `hooks/`, `commands/`, `docs/` y adaptadores, y copiar solo lo necesario. No reemplazar `SKILL.md` ni este documento sin conservar las adaptaciones de agencia.
