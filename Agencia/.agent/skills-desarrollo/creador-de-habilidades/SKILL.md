---
name: creador-de-habilidades
description: Crea nuevas habilidades para el agente Antigravity siguiendo los estándares establecidos. Utiliza esta habilidad cuando el usuario solicite una nueva capacidad estructurada.
---
# Skill: Creador de Habilidades

Esta habilidad permite al agente crear nuevas capacidades reutilizables (habilidades) en el workspace siguiendo los estándares oficiales de Antigravity.

## Cuándo usar esta habilidad
Utiliza esta habilidad cuando un usuario solicite:
- La creación de una nueva "habilidad" o "capacidad".
- La sistematización de un flujo de trabajo recurrente.
- La organización de conocimientos específicos sobre el proyecto en un formato que el agente pueda reutilizar.

## Instrucciones Paso a Paso

1.  **Definición del Nombre**:
    - El nombre de la carpeta debe estar en minúsculas y usar guiones (ej. `analisis-de-rendimiento`).
    - El nombre en los metadatos debe coincidir con el propósito de la habilidad.

2.  **Estructura de Archivos**:
    - Crea la carpeta en `.agents/skills/<nombre-habilidad>/`.
    - Es obligatorio crear el archivo `SKILL.md`.
    - Opcionalmente, crea carpetas `scripts/`, `examples/` o `resources/` si la habilidad requiere lógica o datos adicionales.

3.  **Contenido de SKILL.md**:
    - **Frontmatter YAML**: Debe incluir `name` y `description` (en español).
    - **Instrucciones**: Describe detalladamente el proceso, reglas, checklists y ejemplos. Usa encabezados claros (`#`, `##`, `###`).

4.  **Idioma**:
    - Todas las descripciones e instrucciones deben redactarse exclusivamente en **Español**, a menos que el contexto técnico (código, términos de industria) requiera el inglés.

## Ejemplo de Plantilla (SKILL.md)

```yaml
---
name: nombre-de-la-habilidad
description: Descripción corta y clara de qué hace esta habilidad.
---
# Skill: [Nombre de la Habilidad]

## Objetivo
[Breve explicación del objetivo]

## Flujo de Trabajo
1. Paso 1...
2. Paso 2...

## Reglas y Restricciones
- Regla 1...
- Regla 2...
```

## Validación
Antes de finalizar la creación, el agente debe:
1. Verificar que el `SKILL.md` tenga el frontmatter correcto.
2. Confirmar que la descripción es lo suficientemente clara para que otro agente entienda cuándo activarla.
3. Asegurarse de que la ruta sea correcta según la arquitectura del workspace.
