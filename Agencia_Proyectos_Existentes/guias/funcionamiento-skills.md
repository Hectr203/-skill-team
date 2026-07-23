# Funcionamiento y Activacion de Skills

Este documento describe la estructura y el mecanismo de uso de las skills dentro de la **Agencia Universal para Proyectos Existentes**.

## 1. Naturaleza de las Skills
A diferencia de los Agentes (que representan roles o perfiles específicos), las **Skills** son archivos de contexto (`.md`) reutilizables. Su función es "inyectar" reglas y capacidades específicas al Asistente Principal o a los sub-agentes según la naturaleza de la tarea.

- **Ubicación:** `skills/`
- **Plantilla base:** Toda skill nueva debe crearse usando `plantillas/nueva-skill.md`.
- **Regla inquebrantable:** Ninguna skill debe sustituir la lectura previa del proyecto real. Las skills se adaptan a la arquitectura existente.

## 2. Flujo de Activacion

La activación de una skill consiste en seleccionarla basándose en el requerimiento y proveer su documento como contexto para la tarea. El Asistente Principal ejecuta el siguiente flujo:

1. **Clasificación del requerimiento:** Identificar si es backend, frontend, refactorización, documentación, etc.
2. **Selección por criterio:** Consultar `guias/criterios-activacion-skills.md` para identificar qué skills se necesitan.
3. **Inyección de contexto:** Leer el contenido de las skills seleccionadas y aplicarlo como reglas absolutas durante la ejecución.
4. **Validación:** Comprobar que las reglas de la skill se adaptan al código base que ya existe (ej. no instalar librerías nuevas si la skill de frontend lo sugiere, pero el proyecto ya usa otra).

## 3. Ejemplos de Flujos

| Tarea Requerida | Evaluación del Asistente | Skills Activadas | Resultado Esperado |
| --- | --- | --- | --- |
| Iniciar jornada o proyecto | Se debe cargar la memoria local. | `ahorro-contexto` | Uso de `memoria_proyecto.py` para cargar estado en `.memoria/`. |
| Organizar una API antigua | Es backend y refactorización. | `backend-dominio-limpio`, `refactorizacion-controlada` | Código ordenado respetando la estructura actual, sin romper el contrato. |
| Mejorar visualmente un botón | Es un cambio visual. | `ui-ux-pro-max`, `adaptacion-proyectos-existentes` | CSS/Componentes mejorados siguiendo la guía de estilos existente. |
| Requerimiento incompleto | Falta contexto técnico o de negocio. | `interview`, `analisis-requerimientos` | El agente hace preguntas antes de proponer código. |

## 4. Estructura Interna Obligatoria de una Skill
Cuando se consulta o se crea una skill, siempre contendrá:
- **Objetivo:** Qué resuelve.
- **Cuándo usar / Cuándo no usar:** Límites de su aplicabilidad.
- **Entradas necesarias:** Requisitos previos (ej. modelo de datos, diseño de Figma).
- **Procedimiento:** Instrucciones para el agente.
- **Salidas esperadas:** Entregable (ej. código, pruebas, ADR).
- **Riesgos:** Advertencias de qué no modificar.
