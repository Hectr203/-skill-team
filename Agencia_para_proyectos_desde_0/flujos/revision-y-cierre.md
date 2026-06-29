# Flujo de Revisión y Cierre

## Objetivo
Asegurar que cada funcionalidad o fase de implementación cumpla con los estándares de calidad y requerimientos funcionales antes de considerarse "completa".

## Checklist
- Requerimiento entendido y cubierto en su totalidad.
- Arquitectura e infraestructura respetadas.
- Código limpio, comentado y formateado.
- Dependencias nuevas documentadas e instaladas correctamente.
- Consideraciones de seguridad aplicadas (ej. validación de inputs, manejo de variables de entorno).
- Pruebas (unitarias o manuales) ejecutadas y exitosas.
- Riesgos residuales o deuda técnica declarados.
- Tareas pendientes separadas del trabajo actual.
- Si hubo Azure: recursos y configuración verificados, comandos `az` registrados, secretos redactados, pruebas integradas ejecutadas y rollback documentado.
- La documentación operativa coincide con lo realmente desplegado y distingue pruebas externas pendientes.

## Informe de Cierre
Al finalizar una tarea significativa, se debe generar un breve resumen que incluya:
- Resumen del desarrollo completado.
- Archivos creados o modificados de forma importante.
- Decisiones técnicas tomadas y su justificación.
- Validaciones realizadas (cómo se probó).
- Siguientes pasos recomendados para la siguiente fase.
