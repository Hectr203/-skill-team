# Reglas Generales

1. El proyecto existente es la fuente principal de verdad.
2. La documentacion existente prevalece sobre suposiciones del agente.
3. Las convenciones locales prevalecen sobre estilos genericos.
4. Todo cambio debe tener una razon vinculada al requerimiento, bug o mejora solicitada.
5. Las modificaciones deben ser lo mas pequenas posible dentro de una solucion correcta.
6. No se deben introducir dependencias sin verificar alternativas existentes.
7. No se debe cambiar arquitectura para resolver un problema local si una extension puntual es suficiente.
8. Los cambios de base de datos requieren analisis de impacto, migracion y plan de validacion.
9. Los cambios de seguridad requieren revision explicita de autenticacion, autorizacion, datos sensibles y exposicion.
10. Todo cierre debe declarar pruebas ejecutadas, pruebas no ejecutadas y riesgo residual.
11. Ninguna tarea se considera completada sin evidencias de que todos los criterios de aceptacion obligatorios estan cumplidos.
12. Cada tarea debe pasar por el ciclo completo: Analisis, Especificacion, Implementacion, Validacion, Evaluacion, Correccion y Cierre. No se permite saltar fases.
13. Cada iteracion debe registrarse con numero correlativo, agentes participantes, pruebas ejecutadas, errores detectados, correcciones aplicadas y estado de los criterios de aceptacion.
14. No repetir una correccion identica que ya haya fallado anteriormente sin modificar el enfoque.
15. Si un error persiste tras 3 intentos de correccion, documentar el bloqueo y escalar al humano. Maximo 5 iteraciones por defecto.
16. No confundir actividad con progreso. No confundir generacion de codigo con cumplimiento de requerimientos.
17. No ocultar errores ni pruebas fallidas. No declarar exito cuando las pruebas no puedan ejecutarse.
