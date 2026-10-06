---
name: graphify
description: Navegación de código basada en grafos de conocimiento para ahorro masivo de tokens. Indexa relaciones, flujo de llamadas, dependencias y nodos centrales antes de cualquier exploración profunda.
---

# Graphify: Navegación por Grafo de Código y Ahorro de Tokens

Esta skill establece el protocolo obligatorio para mapear, consultar y navegar el código fuente mediante grafos de conocimiento persistentes con **Graphify**, evitando que los agentes exploren a ciegas o quemen tokens en lecturas completas de archivos o comandos `grep` masivos.

---

## 1. Dinámica según el Ciclo de Vida del Proyecto

1. **Al Inicio de un Proyecto Nuevo (Greenfield)**:
   - Durante la fase inicial de descubrimiento, requisitos y diseño conceptual, **no se genera el grafo** (no existen archivos de código que indexar).
   - **Punto de activación**: Tan pronto como la estructura base de carpetas y archivos esté creada en `frontend/` y `backend/`, es **obligatorio ejecutar la indexación inicial** para habilitar la navegación por grafo en los pasos de desarrollo subsiguientes.
2. **En Proyectos Existentes (Brownfield)**:
   - **Comprobación inmediata**: Verificar si existe `graphify-out/graph.json`.
   - Si existe: usar inmediatamente `graphify query` para resolver dependencias y arquitectura.
   - Si no existe: indexar el repositorio con Graphify **antes de cualquier exploración masiva** para proteger la ventana de contexto.
3. **Mantenimiento Incremental**:
   - Tras completar una tarea o modificar módulos clave, actualizar el grafo utilizando el modo incremental (`graphify --update`) para registrar las nuevas conexiones sin reindexar todo desde cero.

---

## 2. Regla de Consulta Previa Obligatoria

> [!IMPORTANT]
> **PROHIBICIÓN DE LECTURAS A CIEGAS**:
> Antes de explorar archivos arbitrariamente o responder preguntas estructurales sobre el software (*"¿cómo funciona X?", "¿dónde se maneja Y?", "¿qué llama a Z?", "¿qué impacto tiene modificar este endpoint?"*), los agentes deben consultar primero el grafo mediante `graphify query`.
> Solo después de haber identificado los nodos o archivos exactos a través del grafo se procede a leer los fragmentos indispensables.

---

## 3. Comandos y Herramientas del Grafo

| Comando | Propósito | Salida / Beneficio |
|---|---|---|
| `graphify query "<pregunta>"` | Consulta semántica y topológica en lenguaje natural sobre la arquitectura | Nodos y aristas relevantes con contexto condensado |
| `graphify status` | Verifica el estado del índice del grafo y si existen archivos desactualizados | Resumen de nodos, aristas y frescura |
| `graphify callers <simbolo>` | Identifica todas las funciones o módulos que invocan al símbolo indicado | Detección de impacto (*blast radius*) previo a refactors |
| `graphify callees <simbolo>` | Identifica todas las dependencias y servicios que el símbolo consume | Mapa de dependencias hacia capas inferiores |
| `graphify impact <archivo/nodo>` | Analiza el radio de afectación si se modifica o elimina el nodo | Lista de componentes potencialmente afectados |
| `graphify --update` | Sincronización incremental tras aplicar cambios de código | Actualización rápida sin costo de reindexación total |

---

## 4. Estructura de Salida de Graphify

La indexación genera en la raíz del proyecto el directorio `graphify-out/`:
- `graph.json`: Estructura serializada de nodos (archivos, clases, funciones) y aristas (llamadas, importaciones, herencia).
- `GRAPH_REPORT.md`: Resumen ejecutivo con nodos centrales (*god nodes*), métricas de acoplamiento y detección de comunidades modulares.
- `graph.html`: Visualizador interactivo local para inspección visual del grafo de dependencias.

---

## 5. Protocolo de Ahorro Extremo de Contexto

1. **Localizar el punto de entrada** mediante `graphify query`.
2. **Limitar la lectura** únicamente al rango de líneas indicado por los nodos del grafo (`file://path/to/file#L10-L40`).
3. **Verificar dependientes** con `graphify callers` antes de mutar contratos o tipos TypeScript.
4. **Registrar el hallazgo** en la memoria persistente del proyecto (`claude-mem`) para que la siguiente sesión no tenga que reconsultar el mismo flujo.
