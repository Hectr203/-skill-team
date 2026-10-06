---
name: conservacion-estructura
description: Regla y procedimiento de prudencia para preservar la arquitectura, estilo, convenciones y organización de carpetas en proyectos brownfield existentes.
---

# Conservación de Estructura Actual

## Propósito
Garantizar que al intervenir un repositorio existente no se apliquen cambios innecesarios de carpetas, capas, tecnología, frameworks o estilo arquitectónico, respetando las decisiones del equipo original y los cambios no confirmados del usuario.

## Cuándo usar
- En todo proyecto brownfield donde el código ya tenga una arquitectura funcional.
- Cuando el cambio solicitado sea localizado o incremental.
- Cuando exista riesgo de romper contratos de datos, dependencias o rutas existentes.

## Procedimiento
1. **Identificar el lugar natural del cambio**: Mapear los módulos o carpetas donde reside la responsabilidad funcional según la estructura del proyecto existente.
2. **Adoptar las convenciones vigentes**: Reutilizar el estilo de tipado, nombrado, manejo de errores y librerías ya instaladas en el repositorio.
3. **Prohibición de sobreescritura de stack**: No forzar Monorepo dividido ni Clean Architecture si el proyecto utiliza otro patrón (ej. monolito modular, arquitectura MVC, etc.).
4. **Mapeo de dependencias**: Consultar el grafo de Graphify antes de mover o renombrar componentes.
5. **Aprobación de cambios estructurales**: Si una refactorización arquitectónica es indispensable para la tarea, proponerla explícitamente y requerir aprobación antes de mover archivos.

## Entregables
- Modificación mínima y quirúrgica compatible con el código existente.
- Pruebas de regresión que confirmen que no se alteraron comportamientos preexistentes.
