# Desarrollo incremental

El [asistente principal](../asistente-principal.md) coordina este flujo. Aplicar [precedencia](../reglas/precedencia.md), [contrato de roles](../agentes/contrato-agente.md) y [selección de skills](../reglas/seleccion-skills.md). Tecnología y arquitectura se resuelven en el perfil del manifiesto.

## Activación
Una funcionalidad delimitada añade comportamiento al proyecto.

## Entradas
Criterios, contratos, perfil, estado real y dependencias.

## Procedimiento
Ubicar responsabilidades y asignar un dueño por artefacto. Seleccionar skills pertinentes y acordar contratos entre capas. En backend y frontend, seguir el flujo por funcionalidad de la [política de simplicidad](../reglas/simplicidad-ponytail.md): buscar reutilización, aplicar la escalera de decisión y proponer la solución mínima correcta antes de codificar. Implementar de forma incremental; usar reproducción o TDD cuando aporte evidencia. Ejecutar pruebas según riesgo con el runner real. CI, PR, merge o despliegue solo si forman parte del alcance y existen permisos; no hacer push por completar una iteración local.

## Entrega
Resultado, archivos, pruebas, criterios y traspasos pendientes.

## Criterios de aceptación
La funcionalidad satisface sus criterios y no oculta regresiones o controles pendientes.
