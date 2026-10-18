# Pruebas de navegador

El [asistente principal](../asistente-principal.md) coordina este flujo. Aplicar [precedencia](../reglas/precedencia.md), [contrato de roles](../agentes/contrato-agente.md) y [selección de skills](../reglas/seleccion-skills.md). Tecnología y arquitectura se resuelven en el perfil del manifiesto.

## Activación
Un recorrido web necesita comprobación visual o funcional.

## Entradas
Flujos, aplicación y datos de prueba aislados, capacidades disponibles.

## Procedimiento
Usar el navegador o runner disponible y autorizado, sin prioridad por marca de IDE ni activar servidores automáticamente. Confirmar URL real y readiness; no asumir TLS o puerto. Comprobar recorridos afectados, errores, teclado, foco y movimiento reducido. Usar tamaños pertinentes al público, no una lista universal. Registrar capturas/logs mínimos sin datos personales.

## Entrega
Casos, resultados, entorno y evidencia; restricciones si no hay navegador.

## Criterios de aceptación
Recorridos pertinentes verificados; revisión manual y automatización se distinguen.
