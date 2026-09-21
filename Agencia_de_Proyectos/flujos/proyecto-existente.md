# Flujo de Proyecto Existente (Brownfield)

Este flujo establece la metodología rigurosa para intervenir, diagnosticar, refactorizar o ampliar repositorios de software existentes, asegurando la preservación de su arquitectura y evitando la imposición arbitraria de patrones ajenos.

---

## Fases del Proceso Brownfield

```text
1. Consulta a Memoria ──> 2. Navegación Graphify ──> 3. Diagnóstico y Baseline ──> 4. Análisis de Impacto ──> 5. Parche Mínimo Ponytail ──> 6. Regresión y Cierre
```

---

### Fase 1: Consulta Obligatoria a la Memoria Persistente
- Consultar `claude-mem` o `contexts/projects/<id>/memoria.md` antes de cualquier acción.
- Recuperar decisiones previas, acuerdos de arquitectura, restricciones y convenciones del equipo.

### Fase 2: Navegación Mediante Grafo de Código (Graphify)
- Comprobar si existe `graphify-out/graph.json`.
  - Si existe: ejecutar `graphify query` para ubicar módulos y puntos de entrada sin quemar tokens en lecturas masivas.
  - Si no existe: indexar el repositorio con Graphify antes de hacer exploraciones amplias.
- Localizar símbolos con `graphify callers` y `graphify callees` para comprender el flujo de llamadas.

### Fase 3: Diagnóstico y Baseline
- Mapear tecnologías, dependencias y versiones en manifests (`package.json`, `go.mod`, etc.).
- Comprobar el estado del repositorio (`git status`): identificar cambios del usuario sin confirmar para preservarlos obligatoriamente.
- Ejecutar la suite de pruebas existente para establecer la línea base (*baseline*) previa a la modificación.

### Fase 4: Análisis de Impacto y Planificación
- Medir el radio de afectación con `graphify impact`.
- Prohibición estricta de sustituir la arquitectura existente por la arquitectura predeterminada de la agencia.
- Redactar un plan de modificación incremental respetando las convenciones del repositorio.

### Fase 5: Implementación Mínima y Compatible (Ponytail)
- Aplicar la modificación quirúrgica más pequeña que resuelva el requerimiento.
- Reutilizar librerías y patrones ya instalados en el proyecto.
- No realizar refactors cosméticos ni mover carpetas fuera del alcance de la tarea.

### Fase 6: Pruebas de Regresión y Cierre
- Ejecutar pruebas de regresión para confirmar que no se rompieron contratos existentes.
- Actualizar el grafo de Graphify de forma incremental (`graphify --update`).
- Notificar la culminación con `scripts/notificar_tarea.py` y actualizar la memoria persistente del proyecto con `scripts/cierre.py`.
