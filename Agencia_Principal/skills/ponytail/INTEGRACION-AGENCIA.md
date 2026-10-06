# Integracion de Ponytail en la agencia de proyectos desde cero

## Resumen
Ponytail se integra como skill de configuracion inicial para proyectos nuevos. Su punto de entrada local es `SKILL.md`; las reglas originales se conservan en `skills/`, `AGENTS.md`, adaptadores de IDE y archivos de plugin.

## Funcionamiento confirmado
- El repo original define la regla principal en `skills/ponytail/SKILL.md`.
- Las skills auxiliares son `ponytail-review`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain` y `ponytail-help`.
- `AGENTS.md` contiene una version compacta para agentes que leen instrucciones de proyecto.
- Los manifiestos de Codex y Claude Code apuntan a `hooks/claude-codex-hooks.json`.
- OpenCode usa `.opencode/plugins/ponytail.mjs`, que requiere `hooks/ponytail-instructions.js` y `hooks/ponytail-config.js`.
- Gemini usa `gemini-extension.json` con `AGENTS.md` como contexto.

## Inferencia tecnica
En esta agencia, Ponytail debe instalarse antes de iniciar desarrollo para que las reglas de minimalismo guien las primeras decisiones: seleccion de dependencias, estructura inicial, componentes, scripts, reglas de IDE y convenciones de agentes.

## Recomendacion propuesta
Configurar solo los adaptadores del IDE o agente que el proyecto realmente usara. Si el equipo aun no decide herramienta, copiar `AGENTS.md` como fallback portable y registrar la decision pendiente.

## Flujo operativo
1. Identificar el proyecto en `proyectos/<nombre>/`.
2. Preguntar o detectar IDE y asistentes objetivo.
3. Seleccionar adaptadores concretos desde esta carpeta.
4. Copiar reglas sin traducir ni modificar.
5. Registrar en memoria la intensidad elegida: `lite`, `full`, `ultra` u `off`.
6. Validar que las rutas relativas de los archivos copiados sigan funcionando.

## Matriz de adaptadores
| Entorno | Recurso local |
| --- | --- |
| Codex | `.codex-plugin/`, `skills/`, `hooks/`, `assets/` |
| Claude Code | `.claude-plugin/`, `skills/`, `hooks/` |
| OpenCode | `.opencode/`, `opencode.json`, `skills/`, `hooks/` |
| Gemini / Antigravity | `gemini-extension.json`, `AGENTS.md`, `commands/`, `skills/` |
| Cursor | `.cursor/rules/ponytail.mdc` |
| Windsurf | `.windsurf/rules/ponytail.md` |
| Cline | `.clinerules/ponytail.md` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Kiro | `.kiro/steering/ponytail.md` |
| Generico | `AGENTS.md` o `skills/ponytail/SKILL.md` |

## Prevencion de conflictos
Prioridad: instrucciones del humano, reglas globales de la agencia, arquitectura del proyecto, configuracion del IDE, Ponytail, valores predeterminados.

Ponytail no elimina obligaciones de seguridad, validacion, accesibilidad, pruebas minimas, Clean Architecture, Prisma ni Atomic Design. Solo cuestiona complejidad no requerida dentro de esas reglas.

## Actualizacion
Para actualizar esta copia, comparar contra el repositorio de referencia `../../ponytail` desde la raiz del workspace, revisar cambios en `skills/`, `AGENTS.md`, `hooks/`, `commands/`, `docs/` y adaptadores, y copiar solo lo necesario. No reemplazar `SKILL.md` ni este documento sin conservar las adaptaciones de agencia.
