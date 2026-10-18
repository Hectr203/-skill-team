# Auditoría técnica y seguridad

El [asistente principal](../asistente-principal.md) coordina este flujo. Aplicar [precedencia](../reglas/precedencia.md), [contrato de roles](../agentes/contrato-agente.md) y [selección de skills](../reglas/seleccion-skills.md). Tecnología y arquitectura se resuelven en el perfil del manifiesto.

## Activación
Auditoría solicitada o revisión de un cambio de riesgo.

## Entradas
Alcance, exclusiones, código/configuración reales y fronteras de confianza.

## Procedimiento
Inventariar archivo por archivo y marcar exclusiones. Revisar corrección, permisos, datos, dependencias y documentación con evidencia. Separar sospechas de riesgos confirmados; buscar evidencia que refute cada hallazgo. Las pruebas activas o acceso externo requieren autorización aplicable. Corregir si el encargo lo autoriza; de otro modo entregar remediaciones revisables. No presumir subagentes, frameworks de cacería ni certificaciones.

## Entrega
Cobertura, hallazgos por archivo, correcciones autorizadas y controles pendientes.

## Criterios de aceptación
Cada hallazgo tiene contexto e impacto, la cobertura es explícita y no se divulgan secretos.
