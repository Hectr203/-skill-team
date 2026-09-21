---
name: refactorizacion-controlada
description: Guía de refactorización incremental y segura para código existente, aplicando la filosofía Ponytail, pruebas de regresión y commits atómicos.
---

# Refactorización Controlada en Proyectos Existentes

## Propósito
Modificar o modernizar componentes existentes sin alterar el comportamiento esperado por los usuarios ni introducir regresiones en módulos interdependientes.

## Principios Fundamentales
1. **Regla de Oro**: No mezclar refactorizaciones cosméticas con correcciones de errores o nuevas funcionalidades en el mismo commit o tarea.
2. **Pruebas de Caracterización**: Antes de modificar código legacy sin cobertura, escribir una prueba mínima que capture el comportamiento actual (incluyendo casos límite).
3. **Cambios en Rebanadas Verticales**: Aplicar la filosofía Ponytail y la técnica de "Mikado" o rebanadas pequeñas: un cambio atómico a la vez.
4. **Verificación Continua**: Ejecutar los tests de regresión tras cada pequeña mutación.
5. **Reversibilidad Garantizada**: Cada paso debe ser revertible de forma aislada sin dejar el repositorio en estado roto.

## Procedimiento
1. Delimitar el alcance exacto del componente a refactorizar.
2. Comprobar en el grafo de Graphify qué módulos dependen de él.
3. Crear o confirmar la prueba de regresión base.
4. Aplicar el cambio mínimo que cumple el objetivo técnico.
5. Ejecutar la suite de pruebas y linters.
6. Notificar la finalización mediante `scripts/notificar_tarea.py` si es una tarea extensa.
