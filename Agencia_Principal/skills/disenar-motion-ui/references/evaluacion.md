# Evaluar diseño y comportamiento

## Revisar decisiones antes de implementar

Responder con evidencia disponible, no con una nota global inventada:

| Pregunta | Evidencia útil | Qué revisar si falta |
| --- | --- | --- |
| ¿Cumple la intención del encargo? | Relación explícita entre interacción y efecto | Replantear objetivo o comparar otra alternativa |
| ¿Preserva identidad y contenido? | Tokens, referencia, estados y textos reales | Revisar diseño; declarar supuestos |
| ¿Se comprende el estado sin movimiento? | Selección, título, etiqueta o indicador persistente | Añadir señal estable |
| ¿La entrada alternativa permite la misma tarea? | Recorrido con teclado/toque y estado de foco | Definir comportamiento equivalente |
| ¿Resuelve repetición e interrupciones? | Estado final tras secuencias concretas | Especificar política y separación de datos |
| ¿Su coste es aceptable en el entorno? | Observación o medición con contenido representativo | Medir; no afirmar fluidez por intuición |

No puntuar belleza, conversión ni satisfacción sin un método relevante. Diferenciar inspección experta, prueba técnica y prueba con personas.

## Casos de aceptación de una implementación

Seleccionar los que correspondan; registrar entrada, resultado esperado, resultado observado y limitación.

| Caso | Resultado esperado |
| --- | --- |
| Activación normal y salida | Estado correcto, sin capas residuales ni pérdida de contenido |
| A → B → C antes de terminar | Navegación acaba en C; ninguna respuesta antigua sustituye C |
| Deshacer o volver durante transición | Resultado conforme a política; datos y foco coherentes |
| Datos vacíos, lentos, error o fuera de orden | Estado explícito del contexto correcto; sin datos heredados |
| Formulario con datos introducidos | Preservación según contrato; animación no provoca pérdida ni doble envío |
| Alto/ancho variable, texto ampliado, carga tardía | Contenido accesible y objetivos pulsables sin recortes |
| Teclado y foco durante transición | Orden lógico, señal visible y ausencia de foco oculto |
| Toque y cambio a teclado/ratón | Tarea disponible sin depender de hover |
| Preferencia de movimiento reducido y cambio en sesión | Presentación adaptada; función conservada |
| API de animación ausente, transición omitida o desmontaje | Función correcta; limpieza sin excepciones residuales |
| Recurso de origen eliminado al volver | Destino de retorno lógico; sin transición a elemento inexistente |
| Lista extensa o varios efectos simultáneos | Sin degradación relevante para la tarea en el entorno probado |

El caso A → B → C se refiere a navegación, no a cancelar operaciones transaccionales.

## Comprobar por patrón

- **Crossfade:** selección y panel correcto; representación saliente no interactiva; sin sobreposición confusa; alturas variables; pestañas operables.
- **Exposición semántica:** revisar árbol de accesibilidad o comprobación equivalente durante el solapamiento; cuando cambie exposición/foco, comprobar lectura y recorrido con tecnología asistiva representativa si está disponible, documentando si no se probó.
- **Shared element:** correspondencia de entidad; continuidad perceptible; imagen proporcionada y texto legible; cierre/retorno lógico.
- **Magnification:** escala continua; vecinos coherentes; geometría estable; etiquetas visibles; selección precisa sin objetivos obstruidos.
- **Blur:** objetivo nítido; datos necesarios legibles; control enfocado nítido; recuperación del conjunto sin ambigüedad.

## Rendimiento y alcance de las afirmaciones

Usar contenido y entorno representativos cuando haya posibilidad de medición. Observar retraso de interacción, saltos, trabajo de layout/pintura y memoria persistente cuando sean relevantes. Comparar con la versión sin el efecto.

No imponer 60 fps, tiempos absolutos o un dispositivo concreto como prueba universal. Si hay presupuestos del proyecto, verificarlos; si no, documentar condiciones y síntomas. Un prototipo aislado no valida un producto completo.

No convertir «se ve bien» en «mejora la conversión». Proponer prueba con personas o experimento de producto únicamente cuando ayude a responder una incertidumbre real.

## Informe breve

Indicar decisión, razón contextual, prueba realizada, condiciones del entorno y asuntos pendientes. Una especificación sin implementación debe distinguir criterios de aceptación de pruebas ejecutadas.
