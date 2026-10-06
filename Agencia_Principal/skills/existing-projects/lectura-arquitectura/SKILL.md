---
name: lectura-arquitectura
description: Metodología de diagnóstico y lectura de arquitectura en repositorios existentes mediante memoria persistente, inspección estática y grafos de conocimiento.
---

# Lectura y Diagnóstico de Arquitectura Existente

## Propósito
Comprender a fondo la arquitectura, el flujo de llamadas, el modelo de datos y las fronteras de un repositorio existente sin realizar lecturas masivas a ciegas ni quemar tokens innecesarios.

## Procedimiento de Diagnóstico
1. **Recuperación de Memoria Persistente**:
   - Consultar `claude-mem` o el archivo de memoria local del proyecto para conocer acuerdos previos y estado de tareas.
2. **Inspección del Grafo de Conocimiento (Graphify)**:
   - Verificar si existe `graphify-out/graph.json`.
   - Si existe, ejecutar `graphify query` para identificar dependencias, nodos centrales y puntos de entrada.
   - Si no existe y el proyecto cuenta con código, ejecutar la indexación inicial de Graphify.
3. **Mapeo de Tecnologías y Versiones**:
   - Inspeccionar manifests (`package.json`, `go.mod`, `Cargo.toml`, `requirements.txt`).
   - Identificar versiones exactas de runtime y dependencias críticas.
4. **Reproducción del Comportamiento Actual**:
   - Verificar si los tests existentes pasan antes de tocar código.
   - Si no hay tests, registrar el baseline observado.
5. **Evaluación de Deuda Técnica**:
   - Detectar puntos frágiles, acoplamientos excesivos o APIs obsoletas.

## Entregables
- Diagnóstico conciso de arquitectura existente.
- Matriz de tecnologías detectadas.
- Puntos de entrada identificados y mapa de riesgos de modificación.
