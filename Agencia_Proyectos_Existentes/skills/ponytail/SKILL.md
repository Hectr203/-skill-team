---
name: ponytail
description: "Integra Ponytail en proyectos existentes mediante inspección previa, propuesta de cambios, fusión segura de reglas y prevención de sobrescrituras."
---

# Ponytail - Proyectos Existentes

## Propósito
Ponytail es una skill portable para agentes de IA que fuerza la solución más simple que funciona: cuestionar trabajo innecesario, preferir la biblioteca estándar, preferir capacidades nativas de la plataforma, evitar dependencias nuevas y escribir el mínimo código correcto.

En esta agencia de proyectos existentes, Ponytail se integra de forma conservadora: primero analiza el repositorio real, detecta reglas, IDEs y convenciones ya presentes, y solo después propone cómo incorporar reglas de minimalismo sin sobrescribir configuraciones del equipo.

## Cuándo invocar esta skill
Invócala cuando ocurra cualquiera de estos casos:

- El humano pide "ponytail", "modo lazy", "YAGNI", "mínimo código", "sin sobreingeniería" o "solución simple".
- Se incorpora la agencia a un repositorio por primera vez.
- Antes de una refactorización, simplificación, revisión de sobreingeniería o reducción de deuda técnica.
- Antes de añadir una dependencia, abstracción, capa, wrapper, factory o configuración nueva a un proyecto ya iniciado.
- Cuando existan dudas sobre si el proyecto ya tiene reglas de Cursor, Windsurf, Cline, Codex, Claude Code, OpenCode, Gemini, Copilot, Kiro, Antigravity, CodeWhale o agentes genéricos.

No la invoques para imponer una arquitectura nueva ni para reescribir configuraciones existentes sin diagnóstico.

## Entradas necesarias
- La ruta del proyecto existente.
- Alcance del cambio o revisión.
- IDE, agente o asistente objetivo, si el humano lo conoce.
- Nivel de intensidad deseado: `lite`, `full`, `ultra` u `off`. Si no se especifica, usa `full` solo como propuesta.
- Confirmación explícita antes de sobrescribir, fusionar o mover archivos existentes.

## Flujo de ejecución
1. Ejecuta la lectura inicial del proyecto según `asistente-principal.md` y las skills `adaptacion-proyectos-existentes`, `lectura-arquitectura-existente` y `conservacion-estructura-actual` cuando apliquen.
2. Detecta configuraciones existentes: `.cursor/rules/`, `.windsurf/rules/`, `.clinerules/`, `.github/copilot-instructions.md`, `AGENTS.md`, `.kiro/steering/`, `.opencode/`, `.codex-plugin/`, `.claude-plugin/`, `gemini-extension.json`, `opencode.json`.
3. Clasifica el estado:
   - Sin reglas: propone copiar solo el adaptador necesario.
   - Con reglas compatibles: propone añadir Ponytail como archivo nuevo junto a las reglas existentes.
   - Con reglas que podrían entrar en conflicto: redacta una propuesta de fusión y espera confirmación.
   - Con plugin ya instalado: valida rutas y versión, no reinstales.
4. Antes de editar, muestra la lista de archivos que se crearán o modificarán.
5. Si se requiere modificar un archivo existente, crea respaldo o deja una estrategia de reversión documentada.
6. Copia reglas originales sin traducir ni alterar cuando se instalen como adaptador.
7. Documenta conflictos, decisiones, archivos tocados y validaciones en la memoria independiente del proyecto.
8. Ejecuta validación estructural y, si el proyecto tiene pruebas rápidas seguras, ejecútalas después de integrar.

## Selección de configuración por herramienta

| Herramienta | Archivo o directorio a revisar/copiar | Regla para proyecto existente |
| --- | --- | --- |
| Codex plugin | `.codex-plugin/`, `skills/`, `hooks/`, `assets/` | Si ya existe plugin o hooks, no sobrescribas; valida y propone fusión. |
| Claude Code plugin | `.claude-plugin/`, `skills/`, `hooks/` | Requiere `node`; no ejecutes hooks durante la integración. |
| OpenCode | `.opencode/`, `skills/`, `hooks/`, `opencode.json` | Fusiona `plugin` en `opencode.json` solo con confirmación. |
| Gemini CLI / Antigravity | `gemini-extension.json`, `AGENTS.md`, `commands/`, `skills/` | Si existe `AGENTS.md`, añade archivo alterno o propuesta de bloque. |
| Cursor | `.cursor/rules/ponytail.mdc` | Preferir archivo nuevo junto a reglas existentes. |
| Windsurf | `.windsurf/rules/ponytail.md` | Preferir archivo nuevo junto a reglas existentes. |
| Cline | `.clinerules/ponytail.md` | Si `.clinerules` ya es archivo único, no reemplazar; proponer fusión. |
| GitHub Copilot editor | `.github/copilot-instructions.md` | Si existe, no modificar sin respaldo y confirmación. |
| Kiro | `.kiro/steering/ponytail.md` | Añadir como steering separado. |
| CodeWhale, VS Code Codex, agentes genéricos | `AGENTS.md` o `skills/ponytail/SKILL.md` | Respetar instrucciones existentes del repo. |

## Resultados esperados
- Diagnóstico de reglas y asistentes existentes.
- Propuesta de integración antes de cambios destructivos.
- Archivos de Ponytail añadidos de forma incremental.
- Registro de conflictos, respaldos, decisiones y validaciones.
- Confirmación de que la integración no cambió código productivo por sí misma.

## Archivos internos relevantes
- `skills/ponytail/SKILL.md`: regla principal de minimalismo.
- `skills/ponytail-review/SKILL.md`: revisión de sobreingeniería en diffs.
- `skills/ponytail-audit/SKILL.md`: auditoría de repositorio completo.
- `skills/ponytail-debt/SKILL.md`: inventario de comentarios `ponytail:`.
- `skills/ponytail-help/SKILL.md`: ayuda de comandos.
- `AGENTS.md`: regla compacta para agentes sin soporte de skills.
- `hooks/`: activación automática y seguimiento de modo en hosts compatibles.
- `commands/`: comandos TOML usados por hosts compatibles.
- `docs/agent-portability.md`: mapa de adaptadores por agente.
- `docs/platform-native.md`: referencia de soluciones nativas antes de dependencias.

## Jerarquía de resolución de conflictos
Si hay conflictos entre las reglas preexistentes del proyecto y Ponytail:

1. Instrucciones explícitas del humano.
2. Reglas globales de la agencia.
3. Reglas y arquitectura preexistentes del proyecto.
4. Configuración específica del IDE.
5. Instrucciones de Ponytail.
6. Valores predeterminados.

En proyectos existentes, las reglas del repositorio tienen más peso que cualquier preferencia genérica. Ponytail solo reduce complejidad dentro de los límites reales del sistema.

## Cómo NO utilizarla
- No borres ni sobrescribas configuraciones del equipo.
- No modifiques `tsconfig.json`, linters, reglas de IDE o instrucciones del repo sin análisis y confirmación.
- No ejecutes hooks o scripts automáticamente durante la integración.
- No uses Ponytail para cambiar arquitectura, patrones o dependencias existentes sin una razón técnica concreta.
- No ejecutes refactorizaciones masivas bajo el pretexto de "aplicar Ponytail".
- No modifiques el repositorio original de referencia.

## Validación mínima
- Verifica que `SKILL.md`, `AGENTS.md`, `skills/`, `hooks/`, `commands/` y los adaptadores elegidos existan.
- Verifica que los manifiestos copiados no apunten a rutas ausentes.
- Comprueba que no se sobrescribieron archivos existentes sin respaldo o confirmación.
- Registra en la memoria independiente del proyecto qué adaptadores se instalaron, omitieron o dejaron pendientes.
