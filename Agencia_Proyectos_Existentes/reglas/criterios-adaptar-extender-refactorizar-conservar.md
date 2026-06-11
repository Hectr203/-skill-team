# Criterios para Conservar, Adaptar, Extender o Refactorizar

## Matriz de decision

| Decision | Usar cuando | Evidencia necesaria | Validacion |
| --- | --- | --- | --- |
| Conservar | El patron existente funciona y el cambio cabe dentro de el. | Ejemplos similares en el repo. | Pruebas o revision local. |
| Adaptar | El patron sirve, pero requiere ajuste menor. | Diferencia concreta del caso nuevo. | Verificar compatibilidad. |
| Extender | Falta una capacidad nueva en una estructura existente. | Punto de extension claro. | Pruebas de integracion o flujo. |
| Refactorizar | La estructura actual bloquea una solucion segura o mantenible. | Problema repetible, deuda concreta o bug. | Pruebas antes y despues. |
| Reemplazar | El enfoque actual es inviable o riesgoso. | Analisis comparativo y plan de migracion. | Aprobacion humana. |

## Preguntas obligatorias
- Que comportamiento actual debo preservar.
- Que codigo depende de esta zona.
- Hay pruebas que cubran el comportamiento.
- El cambio rompe APIs, base de datos, permisos o flujos existentes.
- Puedo resolverlo con menor alcance.
- Como revertir el cambio si falla.
