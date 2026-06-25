---
name: ponytail
description: "Configura Ponytail en proyectos nuevos para establecer reglas de minimalismo, YAGNI, stdlib primero y uso de funciones nativas antes de iniciar el desarrollo."
---

# Ponytail - Proyectos desde cero

## Propósito
Ponytail es una skill portable para agentes de IA que fuerza la solución más simple que funciona: cuestionar trabajo innecesario, preferir la biblioteca estándar, preferir capacidades nativas de la plataforma, evitar dependencias nuevas y escribir el mínimo código correcto.

En esta agencia de proyectos desde cero, Ponytail se usa durante la planificación inicial para definir reglas de IDE y asistentes antes de escribir lógica de negocio, componentes o infraestructura propia. Su objetivo no es reemplazar Clean Architecture, Prisma, UI/UX Pro Max ni las reglas técnicas de la agencia; su función es evitar que esas decisiones se implementen con abstracciones, dependencias o archivos innecesarios.

## Cuándo invocar esta skill
Invócala cuando ocurra cualquiera de estos casos:

- Se inicia un proyecto nuevo o se copia `proyectos/_plantilla_proyecto`.
- Se define el IDE, asistente de IA o entorno de desarrollo del proyecto.
- El humano pide "ponytail", "modo lazy", "YAGNI", "mínimo código", "sin sobreingeniería" o "solución simple".
- Se van a crear reglas de Cursor, Windsurf, Cline, Codex, Claude Code, OpenCode, Gemini, Copilot, Kiro, Antigravity, CodeWhale o agentes genéricos.
- Antes de añadir dependencias, capas, factories, wrappers, scaffolding o configuraciones "por si acaso".

No la invoques para justificar recortes en seguridad, validación en límites de confianza, accesibilidad, manejo de errores que evita pérdida de datos o requisitos explícitos del humano.

## Entradas necesarias
- Ruta del proyecto nuevo, normalmente `proyectos/<nombre>/`.
- IDE, agente o asistente objetivo. Si no está definido, pregúntalo o registra `AGENTS.md` como fallback genérico.
- Nivel de intensidad: `lite`, `full`, `ultra` u `off`. Si no se especifica, usa `full`.
- Restricciones de la agencia: React, TypeScript, Tailwind CSS, Express.js, PostgreSQL, Prisma, Atomic Design y Clean Architecture cuando apliquen.
- Decisiones previas de arquitectura o metodología que deban respetarse.

## Flujo de ejecución
1. Identifica el proyecto y confirma que se trata de un inicio desde cero.
2. Determina los IDE o agentes que se usarán. Si hay duda, configura primero `AGENTS.md` como instrucción portable.
3. Selecciona solo los adaptadores necesarios. Evita copiar configuraciones de herramientas que el proyecto no usará.
4. Copia las reglas desde esta carpeta `skills/ponytail/` sin traducir ni alterar el texto original de Ponytail.
5. Si el proyecto ya contiene alguna regla por haber sido iniciado antes, no la sobrescribas: fusiona mediante archivo adicional o pide confirmación.
6. Registra la decisión en la memoria del proyecto y en la documentación inicial del proyecto.
7. Valida que los archivos seleccionados existan y que no dependan de recursos ausentes.

## Selección de configuración por herramienta

| Herramienta | Archivo o directorio a copiar al proyecto | Nota |
| --- | --- | --- |
| Codex plugin | `.codex-plugin/`, `skills/`, `hooks/`, `assets/` | Requiere autorización de hooks en el host. No ejecutes hooks durante la copia. |
| Claude Code plugin | `.claude-plugin/`, `skills/`, `hooks/` | Requiere `node` para activación automática. |
| OpenCode | `.opencode/`, `skills/`, `hooks/`, `opencode.json` como referencia | Revisa el `opencode.json` del proyecto antes de fusionar. |
| Gemini CLI / Antigravity | `gemini-extension.json`, `AGENTS.md`, `commands/`, `skills/` | `AGENTS.md` es el contexto persistente. |
| Cursor | `.cursor/rules/ponytail.mdc` | Regla de proyecto. |
| Windsurf | `.windsurf/rules/ponytail.md` | Regla de proyecto. |
| Cline | `.clinerules/ponytail.md` | Regla de proyecto. |
| GitHub Copilot editor | `.github/copilot-instructions.md` | No sustituye políticas de repo existentes sin revisar. |
| Kiro | `.kiro/steering/ponytail.md` | Puede copiarse global o por proyecto. |
| CodeWhale, VS Code Codex, agentes genéricos | `AGENTS.md` o `skills/ponytail/SKILL.md` | Fallback portable. |

## Resultados esperados
- Reglas de Ponytail instaladas solo para las herramientas elegidas.
- Decisión de intensidad documentada.
- Lista de archivos copiados o fusionados.
- Confirmación de que no se añadieron dependencias ni scaffolding innecesario.
- Registro de cualquier excepción técnica aprobada por el humano.

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
Si otras skills tienen reglas de código, aplica este orden:

1. Instrucciones explícitas del humano.
2. Reglas globales de la agencia (Clean Architecture).
3. Reglas y arquitectura del proyecto.
4. Configuración específica del IDE.
5. Instrucciones de Ponytail.
6. Valores predeterminados.

Ponytail no impide cumplir Clean Architecture, Atomic Design o reglas de base de datos. Exige que cada capa, componente o configuración exista por una necesidad real y se implemente de la forma más pequeña y mantenible.

## Cómo NO utilizarla
- No traduzcas ni edites las reglas originales al copiarlas a un proyecto.
- No ejecutes scripts de `hooks/` automáticamente durante la integración.
- No añadas todas las configuraciones por defecto; instala solo las que correspondan al IDE o agente elegido.
- No uses Ponytail para eliminar validaciones, accesibilidad, seguridad o pruebas mínimas.
- No modifiques el repositorio original de referencia.

## Validación mínima
- Verifica que `SKILL.md`, `AGENTS.md`, `skills/`, `hooks/`, `commands/` y los adaptadores elegidos existan.
- Si se copian manifiestos de plugin, comprueba que sus rutas relativas sigan resolviendo dentro del proyecto.
- Registra en la memoria del proyecto qué adaptadores se instalaron y cuáles se omitieron.
