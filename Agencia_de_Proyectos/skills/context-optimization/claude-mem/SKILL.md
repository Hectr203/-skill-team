---
name: claude-mem
description: Sistema universal de memoria persistente multicapa para cualquier IA. Consultar obligatoriamente antes de cualquier acción exploratoria para recuperar contexto, decisiones y aprendizajes previos sin desperdiciar tokens.
---

# Memoria Persistente Universal: claude-mem

Basado en la arquitectura y estándares de **claude-mem** ([github.com/thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)). Esta skill actúa como el estándar central de memoria persistente compartida para **cualquier modelo o plataforma de IA** (Google Antigravity, Claude Code, OpenCode, Cursor, VS Code / Cline, Windsurf).

---

## 1. Principio de Consulta Previa Obligatoria

> [!IMPORTANT]
> **REGLA DE ACCESO PREVIO INNEGOCIABLE**:
> Cada vez que el usuario asigne una nueva tarea o realice una consulta sobre el estado del software, el Asistente Principal y cualquier agente ejecutor **deben consultar obligatoriamente la memoria persistente antes de cualquier acción exploratoria**.
> Está terminantemente prohibido releer repositorios completos o ejecutar comandos masivos de búsqueda a ciegas si la información ya está registrada en la memoria histórica o en el contexto del proyecto.

---

## 2. Arquitectura de Almacenamiento y Recuperación

1. **Almacenamiento Híbrido Local**:
   - Base de datos local en **SQLite con FTS5** (búsqueda full-text por palabras clave).
   - Almacén vectorial con embeddings para **búsqueda semántica híbrida**.
   - Captura continua y comprimida de: actividades recientes, decisiones técnicas (ADRs), resoluciones de bugs y estado de tareas.

2. **Flujo de Recuperación en 3 Capas (Ahorro Extremo de Tokens)**:
   - **Capa 1: Índice de búsqueda (`search`)**: Encuentra resúmenes compactos y coincidencias clave consumiendo apenas unas decenas de tokens.
   - **Capa 2: Línea de tiempo (`timeline`)**: Recupera el orden cronológico de eventos y decisiones tomadas en el proyecto.
   - **Capa 3: Observaciones detalladas (`recall` / `get_observations`)**: Carga el detalle byte a byte únicamente de los fragmentos específicos necesarios para la tarea inmediata.

---

## 3. Herramientas MCP Expuestas para Cualquier IA

El servidor MCP de claude-mem expone las siguientes herramientas estandarizadas para el uso de cualquier agente:

* `mem:search` (o `search`): Búsqueda híbrida (semántica + léxica) en el histórico del proyecto.
* `mem:recall` (o `get_observations`): Recuperación selectiva de detalles y observaciones específicas de tareas previas.
* `mem:timeline` (o `timeline`): Inspección cronológica de los cambios, hitos y acuerdos del repositorio.
* `mem:forget`: Purga o eliminación granular de recuerdos obsoletos, decisiones descartadas o desalineadas a solicitud del usuario.
* `mem:stats`: Diagnóstico del volumen de memoria, cantidad de observaciones y métricas de almacenamiento.

---

## 4. Compatibilidad Universal Multi-IA

1. **Servidor MCP Compartido**:
   - Configurado en `mcp_config.json` para Google Antigravity y OpenCode, y en sus equivalentes para Claude Desktop (`claude_desktop_config.json`) y Cursor (`.cursor/mcp.json`).
   - Todos los agentes consumen el mismo archivo SQLite local (`.memoria/` o base de datos de claude-mem), garantizando continuidad entre diferentes modelos.

2. **Sincronización y Fallback en Markdown**:
   - Para entornos sin soporte MCP activo o sesiones aisladas, se mantiene un volcado seguro y legible en Markdown:
     - `contexts/projects/<project-id>/memoria.md`
     - O el directorio local `.memoria/` gestionado por los scripts `scripts/arranque.py` y `scripts/cierre.py`.
   - Cualquier IA puede leer y escribir en este archivo sin fricción ni dependencias de runtime.

---

## 5. Procedimiento Operativo por Tarea

1. **Arranque de Sesión / Tarea**:
   - Ejecutar consulta a la memoria persistente (`mem:search` o lectura de `contexts/projects/<id>/memoria.md`).
   - Extraer contexto de decisiones previas, convenciones adoptadas y tareas pendientes.
2. **Durante la Ejecución**:
   - No cargar archivos redundantes si su propósito ya está documentado en la memoria.
   - Aplicar el principio Ponytail: cambios mínimos y verificables.
3. **Cierre de Tarea**:
   - Registrar un resumen comprimido del hito alcanzado (archivos modificados, decisión tomada, comandos ejecutados).
   - Actualizar la memoria con `scripts/cierre.py` o mediante la llamada MCP correspondiente para que la próxima sesión/agente disponga del contexto inmediato.
