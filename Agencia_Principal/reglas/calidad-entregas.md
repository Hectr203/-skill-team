# Calidad de las entregas

Aplica al cierre de tareas de desarrollo y evaluación; usar el registro proporcional al trabajo, sin añadir trámites a consultas o ajustes triviales.

1. El asistente principal acuerda criterios observables antes de implementar y asigna un responsable por resultado. Conserva cambios de alcance explícitos.
2. Cada criterio cumplido cita una comprobación pertinente: resultado esperado, comando ejecutado cuando corresponda, código de salida, fecha y limitaciones. Un log vacío o una declaración de éxito no demuestran comportamiento.
3. Distinguir pruebas de la agencia, pruebas de una aplicación e integración con servicios externos. No inferir que unas certifican las otras.
4. Para entregas sustanciales, utilizar [el registro estructurado](../plantillas/entrega.json). Las evidencias locales llevan ruta relativa y SHA-256. Se pueden generar huellas con `sha256sum archivo`; no almacenar secretos en los informes.
5. Ejecutar `python3 scripts/control_entregas.py evaluar informe.json --raiz-entrega /ruta/del/proyecto`. Código 0: completo con integridad comprobada; 2: parcial o bloqueado; 1: registro inválido o evidencia alterada. No ejecuta comandos ni concede permiso para publicar.
6. Revisar contenido y pertinencia de las evidencias, además del control automático. En cambios sensibles, justificar riesgos, reversión y revisión correspondiente; no crear un segundo orquestador.
7. Medir entregas con `python3 scripts/control_entregas.py metricas informe1.json informe2.json --raiz-entrega /ruta/del/proyecto`. Usar una revisión por tarea. No mezclar monedas ni convertir tiempo transcurrido en horas de trabajo.
8. Registrar causas de retrabajo y una mejora concreta cuando existan. Mantener costos desconocidos como `null`; conservar tamaño de muestra y no presentar escenarios simulados como entregas reales.

El registro es local y editable: verifica integridad, no veracidad, autorización ni calidad semántica. Los criterios los acuerda el responsable con el usuario; no existe una puntuación automática que certifique una agencia de 10.

Para cierres de tareas del plan operativo, incluir `artefactos` con rutas y huellas de los archivos asignados. El control vuelve a comprobar esos archivos y la vigencia de sus dependencias al reanudar; consultar [operación de tareas](operacion-tareas.md).
