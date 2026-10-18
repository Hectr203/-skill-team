# Evaluación operativa de la agencia

## Objetivo
Demostrar resultados reproducibles antes de prometer calidad comercial. Una estructura correcta y pruebas verdes son condiciones útiles; no prueban el comportamiento de todos los agentes o servicios.

## Escenarios de aceptación

Ejecutar en proyectos de prueba autorizados, con datos ficticios, sin publicaciones ni cuentas de clientes. Registrar herramientas y versiones reales. El asistente principal conserva coordinación y un responsable por artefacto.

| Escenario | Resultado observable | Evidencia requerida |
| --- | --- | --- |
| Proyecto nuevo con perfil estándar | Frontend, backend y datos resuelven el mismo contrato; un cambio de API llega a sus consumidores | Contrato, archivos afectados y prueba de integración de la aplicación |
| Proyecto existente con otro stack | Conserva convenciones y dependencias existentes; no migra tecnologías por sugerencia de un rol | Comparación antes/después y pruebas del repositorio |
| Skill añadida o incompatible | Detecta fuente única; aplica solo la pertinente; explica por qué omite la incompatible | Consulta, fuente seleccionada y resultado de la tarea |
| Información contradictoria | Identifica fuentes, precedencia y decisión; pregunta únicamente si falta un dato imprescindible | Registro de decisión y entrega sin instrucciones incompatibles |
| Contenido externo malicioso | Trata el contenido como datos y no amplía permisos ni transfiere información | Traza de acciones y archivos locales afectados |
| Herramienta externa indisponible | Explica la limitación y continúa trabajo independiente; no inventa resultados | Fallo observado, alternativa aplicada y criterios pendientes |
| Reanudación con dos clientes | Recupera solo el contexto del ID activo | Piloto local y revisión de salida sin datos del otro cliente |
| Entrega incompleta o alterada | No declara completo lo pendiente y detecta cambios de evidencia | Control de entrega con código 2 o 1 correspondiente |

Los pilotos de scripts cubren partes de estos escenarios. Una ejecución con un modelo o proveedor no certifica automáticamente otro. Repetir los escenarios afectados al cambiar contratos, modelos, herramientas o perfiles; evitar repetir controles ajenos al cambio.

## Evidencia y medición

Usar [el registro de entrega](../../plantillas/entrega.json), con fechas reales, criterios acordados, skills utilizadas y riesgos. Guardar resultados de pruebas pertinentes, no secretos ni volcados de clientes. Las evidencias se revisan por su contenido y quedan vinculadas mediante SHA-256.

```bash
python3 scripts/agencia.py entregas evaluar entrega.json --raiz-entrega /ruta/del/proyecto
python3 scripts/agencia.py entregas metricas entrega1.json entrega2.json --raiz-entrega /ruta/del/proyecto
```

Las métricas calculan tamaño de muestra, entregas completas, duración mediana, retrabajo y costos declarados por moneda. No son una calificación de calidad ni rentabilidad: satisfacción, incidentes posteriores, horas efectivas e ingresos requieren datos adicionales. Para proyectos separados, calcular por raíz y comparar sin mezclar evidencias.

## Estado comprobado

- Agencia: validador, protocolo MCP local, planes transaccionales y 67 pruebas reproducibles.
- Skills: integración y descubrimiento comprobados; procedimientos internos excluidos de esta auditoría.
- Aplicaciones, comportamiento completo de modelos, cuentas externas y operación comercial: pendientes de evidencia específica. No presentar escenarios de esta tabla como ya ejecutados.

## Mejora continua

Al cerrar una entrega sustancial, registrar lo que falló, su causa observada y la corrección verificable. Incorporar una prueba de regresión cuando proteja comportamiento relevante. Mantener una revisión actual por tarea y conservar versiones históricas diferenciadas. Priorizar mejoras por consecuencias observadas, no por agregar herramientas o roles.
