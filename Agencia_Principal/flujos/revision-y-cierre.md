# Revisión y cierre

El [asistente principal](../asistente-principal.md) coordina este flujo. Aplicar [precedencia](../reglas/precedencia.md), [contrato de roles](../agentes/contrato-agente.md) y [selección de skills](../reglas/seleccion-skills.md). Tecnología y arquitectura se resuelven en el perfil del manifiesto.

## Activación
Una tarea alcanza su entrega o presenta un bloqueo.

## Entradas
Alcance, criterios, cambios y resultados realmente obtenidos.

## Procedimiento
Comparar cada criterio con evidencia. Revisar contratos, seguridad y documentación según el riesgo. En cambios de backend y frontend, comprobar la evidencia exigida por la [política de simplicidad](../reglas/simplicidad-ponytail.md): nivel aplicado, peldaño de resolución, omisiones y prueba mínima; incluir la pasada de sobreingeniería. Distinguir revisión propia e independiente. Corregir problemas confirmados o documentar lo pendiente. No exigir todas las clases de pruebas, CI o un proveedor cloud para cualquier cambio. Registrar contexto mínimo y entregar sin publicar o desplegar por defecto.

## Entrega
Usar informe de cierre: completado, parcial o bloqueado; cambios, pruebas, riesgos y próximo responsable.

## Criterios de aceptación
Criterios obligatorios con evidencia suficiente; no afirmar controles no ejecutados.

Para trabajo con dependencias o reanudaciones, aplicar [operación de tareas](../reglas/operacion-tareas.md): recuperar revisión, comprobar evidencia vigente y consolidar estados. El registro no inicia agentes ni concede permisos adicionales.
