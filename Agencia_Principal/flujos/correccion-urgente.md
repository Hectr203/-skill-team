# Corrección urgente

El [asistente principal](../asistente-principal.md) coordina este flujo. Aplicar [precedencia](../reglas/precedencia.md), [contrato de roles](../agentes/contrato-agente.md) y [selección de skills](../reglas/seleccion-skills.md). Tecnología y arquitectura se resuelven en el perfil del manifiesto.

## Activación
Incidente o defecto que requiere parche acotado.

## Entradas
Síntoma, entorno, impacto, alcance autorizado y evidencia sin secretos.

## Procedimiento
Localizar y reproducir el defecto con prueba o pasos deterministas. Aplicar parche mínimo sin refactors incidentales; en backend y frontend, conforme a la [política de simplicidad](../reglas/simplicidad-ponytail.md), dejando la prueba de reproducción como comprobación mínima. Verificar reproducción y regresiones relevantes. Preparar recuperación y distinguir prueba local de intervención productiva. Desplegar únicamente si está autorizado; registrar causa y mitigación sin transferir logs a terceros automáticamente.

## Entrega
Parche, causa observada, pruebas, riesgo residual y estado de despliegue.

## Criterios de aceptación
El defecto tiene evidencia de resolución dentro del alcance; no se declara producción corregida por una prueba local.
