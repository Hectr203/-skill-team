# Metodología Superpowers y Principio de Artefactos de IDE

Esta norma define cómo la **Agencia Principal** aplica la metodología de desarrollo de [Superpowers](https://github.com/obra/superpowers.git) (activa de forma nativa a nivel global en el IDE) garantizando la máxima higiene y limpieza del repositorio de código fuente.

---

## 1. Principio Fundamental: Cero Basura en el Workspace

> [!IMPORTANT]
> **REGLA MANDATORIA DE HIGIENE:**
> Queda terminantemente prohibido crear carpetas acumulativas de especificaciones o planes intermedios como `docs/specs/`, `docs/plans/`, `specs/`, `.plans/` o similares dentro del árbol de archivos del proyecto.
> 
> Toda especificación técnica, plan de implementación paso a paso, análisis de arquitectura o borrador de requerimientos **DEBE CREARSE Y MANTENERSE EXCLUSIVAMENTE COMO UN ARTEFACTO DEL IDE** (en el directorio de cerebro del agente: `<appDataDir>/brain/<conversation-id>/`), a menos que el humano solicite explícitamente persistirlo dentro del repositorio del proyecto.

### ¿Por qué Artefactos del IDE?
1. **Repositorio Limpio:** El repositorio de código solo contiene código fuente productivo, pruebas, configuración y la memoria consolidada del proyecto (en `contexts/projects/<id>/`), sin acumular decenas de archivos `.md` de especificaciones obsoletas tras cada tarea.
2. **Experiencia de Usuario Superior:** Los artefactos del IDE se renderizan de forma interactiva en la interfaz de Antigravity con formateo enriquecido, alertas, diagramas Mermaid y botones de acción.
3. **Persistencia Trazable:** El IDE conserva el historial de artefactos por conversación sin contaminar los commits de Git del cliente ni generar deuda técnica documental.
4. **Excepción Explícita:** Solo si el usuario indica textualmente: *"Guarda este spec en el proyecto como docs/specs/modulo.md"*, se creará el archivo en el workspace.

---

## 2. Los 5 Pilares de Superpowers Integrados en la Agencia

La Agencia aprovecha las habilidades de Superpowers que operan globalmente en el entorno del IDE:

### A. Brainstorming Estructurado (`brainstorming`)
- Antes de saltar a programar cualquier funcionalidad o componente, el agente profundiza en la intención real del usuario.
- Explora alternativas de diseño y aclara requerimientos en bloques pequeños y digeribles.
- Todo entregable de diseño o borrador de especificación se emite como un **Artefacto del IDE**.

### B. Planes de Implementación Bite-Sized (`writing-plans` y `executing-plans`)
- Descompone la tarea en pasos pequeños y verificables que cualquier ingeniero pueda seguir sin desviarse.
- Cada paso incluye el archivo exacto a modificar, la prueba a ejecutar y el resultado esperado.
- El plan se guarda como un artefacto (ej. `plan_implementacion_<tarea>.md`) para que el humano pueda revisarlo y aprobarlo antes de iniciar la ejecución.

### C. La Ley de Hierro de TDD (`test-driven-development`)
- **"The Iron Law":** *Ningún código de producción sin una prueba que falle primero (Rojo → Verde → Refactor).*
- Si se escribe código antes de la prueba, debe descartarse e implementarse de nuevo partiendo de la prueba que falla.
- Para corregir errores (Prove-It Pattern), se escribe primero una prueba que reproduzca el fallo exactamente; una vez confirmada la falla, se implementa la corrección hasta ver la prueba en verde.

### D. Desarrollo Basado en Subagentes (`subagent-driven-development`)
- Tareas independientes se delegan a subagentes especializados (`agente-backend`, `agente-frontend`, `ingeniero-de-pruebas`).
- Cada subagente implementa, auto-revisa contra las directrices de la agencia y reporta con evidencia.

### E. Verificación Basada en Evidencia (`verification-before-completion`)
- **Prohibido afirmar éxito sin pruebas:** Nunca declarar que una tarea está terminada o que los tests pasan sin haber ejecutado los comandos en la terminal y verificado su código de salida (`exit code 0`).
- La evidencia manda sobre las aserciones.

---

## 3. Matriz de Flujo Operativo en la Agencia

```
1. RECEPCIÓN DE TAREA
   │
   ▼
2. BRAINSTORMING & ESPECIFICACIÓN
   │  └─ Emite: Artefacto IDE (brainstorming.md / spec.md)
   ▼
3. PLAN DE IMPLEMENTACIÓN DETALLADO
   │  └─ Emite: Artefacto IDE (plan_implementacion.md)
   │  └─ Compuerta: Aprobación humana vía solicitar_validacion.py
   ▼
4. EJECUCIÓN CON TDD ESTRICTO
   │  ├─ Rojo: Prueba unitaria/integración que falla
   │  ├─ Verde: Código mínimo que hace pasar la prueba
   │  └─ Refactor: Limpieza respetando Clean Architecture
   ▼
5. VERIFICACIÓN Y EVIDENCIA
   │  └─ Ejecución real de linters, compilación y test suites
   ▼
6. CIERRE DE TAREA
   │  ├─ Actualización de memoria: scripts/agencia.py cierre
   │  └─ Notificación sonora: scripts/notificar_tarea.py
```

---

## 4. Enlaces y Referencias
- [Lineamientos de Desarrollo](lineamientos-desarrollo.md)
- [Reglas Generales](reglas-generales.md)
- [Human-in-the-Loop](human-in-the-loop.md)
- [Asistente Principal](../asistente-principal.md)
