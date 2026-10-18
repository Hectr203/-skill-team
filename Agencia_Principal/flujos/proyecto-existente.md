# Proyecto existente

El [asistente principal](../asistente-principal.md) coordina este flujo. Aplicar [precedencia](../reglas/precedencia.md), [contrato de roles](../agentes/contrato-agente.md) y [selección de skills](../reglas/seleccion-skills.md). Tecnología y arquitectura se resuelven en el perfil del manifiesto.

## Activación
Inspección, ampliación o corrección de código existente.

## Entradas
Objetivo autorizado, contexto, repositorio, cambios del usuario y controles existentes.

## Procedimiento
Registrar baseline y leer convenciones reales. Consultar grafo disponible antes de explorar estructura, con fallback localizado explicado si falla. Identificar impacto y contratos; no imponer el perfil estándar ni migrar carpetas fuera del alcance. Implementar el cambio mínimo suficiente, ejecutar regresiones pertinentes y actualizar decisiones afectadas. No actualizar índices por rutina ni instalar herramientas por documentación.

## Entrega
Cambios compatibles, baseline, regresiones y limitaciones.

## Criterios de aceptación
El objetivo se cumple preservando contratos y trabajo previo; las comprobaciones faltantes son explícitas.
