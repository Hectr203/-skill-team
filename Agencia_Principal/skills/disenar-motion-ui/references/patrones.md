# Selección, parámetros y ejemplos

## Calibrar sin fijar una receta

Usar tokens de movimiento existentes cuando sean apropiados. Si no hay sistema, establecer parámetros provisionales y comparar al menos con el cambio directo. Ajustar según distancia, tamaño, lectura, frecuencia de uso e intención expresiva.

Los valores siguientes ilustran un ensayo de prototipo; no provienen del reel ni son umbrales de accesibilidad o calidad.

| Patrón | Parámetros de un ensayo posible | Qué observar antes de conservarlos |
| --- | --- | --- |
| Crossfade | 220 ms y una curva suave | Respuesta perceptible, lectura y cambios rápidos |
| Shared element | 320 ms; curva de llegada sin rebote | Correspondencia espacial, texto y retorno |
| Magnification | Escala máxima 1,35; radio ligado a separación de iconos | Precisión, colisiones, etiquetas y retraso del puntero |
| Blur | 2 px y transición breve, o énfasis estático | Legibilidad, recuperación y datos comparables |

Modificar o descartar cualquier valor que perjudique la tarea. No convertir la duración en latencia de la función ni exigir que el usuario espere.

## Crossfade: reemplazo de contenido

**Elegirlo:** cuando la sustitución gradual refuerce el cambio dentro del mismo contexto.
**Reconsiderarlo:** cuando el solapamiento de texto dificulte lectura, el cambio sea muy frecuente o el contenido actual deba seguir disponible.

- Definir si se animan el panel, su contenido o una captura; conservar controles persistentes.
- Separar el panel semánticamente activo de una representación visual saliente. Opacidad cero y `pointer-events: none` no resuelven por sí solos el acceso por teclado.
- Conservar valores de formularios según el comportamiento autorizado. No desmontar componentes solo para animarlos.
- Permitir recalcular el espacio ante contenido asíncrono; considerar contenedor en flujo, espacio reservado o ajuste controlado según el diseño.
- No transferir el foco al panel por cada cambio de pestaña sin una razón funcional.
- Si la carga tiene latencia, especificar un estado de carga real y controlar resultados fuera de orden; no animar datos de otro contexto como si fueran correctos.

**Prompt:** «Diseña un crossfade para estas pestañas. Conserva navegación, valores de formularios y alturas variables. Define el panel activo, la respuesta a cambios rápidos y datos tardíos. Justifica los parámetros con el contexto y ofrece una alternativa para movimiento reducido. Implementa solo si ese es el alcance solicitado».

## Shared element: continuidad de un recurso

**Elegirlo:** cuando la misma entidad pase de resumen a detalle o cambie de ubicación.
**Reconsiderarlo:** si no hay correspondencia reconocible, si la referencia ya desapareció o si transforma innecesariamente grandes áreas.

- Elegir un ancla por su significado: imagen, título o grupo estable. Un texto idéntico de recursos distintos no establece identidad.
- Preferir un recurso estable de contenido; no confundir índice de lista con identidad cuando pueda reordenarse.
- Prevenir nombres de transición duplicados en la misma captura si la API requiere unicidad.
- Validar geometrías cuando fuentes, imágenes y destino estén disponibles; si faltan o cambian durante el efecto, adaptar la transición o abrir directamente sin bloquear la función.
- Tratar textos e imágenes según su naturaleza: preservar relación de aspecto y lectura; evitar estirar glifos durante cambios de tamaño.
- Alinear con el router y la geometría disponible; no suponer equivalencia entre una SPA y navegación entre documentos.
- En diálogos, implementar cierre y retorno del foco; en páginas, seguir la estrategia de navegación; si el origen desaparece, elegir un destino lógico de retorno.

**Prompt:** «Usa shared element para mantener reconocible este recurso al abrir su detalle. Elige un ancla y define correspondencia espacial, navegación, foco, scroll y alternativa si no hay origen o soporte. Evita duplicaciones y deformaciones. Ajusta tiempos a la intención del proyecto».

## Magnification: respuesta continua a proximidad

**Elegirlo:** para exploración de un conjunto de acciones con espacio y capacidades de entrada apropiados.
**Reconsiderarlo:** si la densidad, el objetivo de precisión o la frecuencia de uso hacen menos previsible la selección.

Una distribución gaussiana es una opción, no una obligación:

```text
d = distancia desde el puntero al centro estable del icono
scale = 1 + A * exp(-(d*d)/(2*sigma*sigma))
A >= 0; sigma > 0; valores finitos
```

- Elegir distancia por geometría: un eje en un dock lineal o distancia espacial en otra composición.
- Usar posiciones en CSS px con scroll/transformaciones coherentes. Recalcular al cambiar orientación, ancho, contenido o disposición.
- Acotar la zona de influencia, restablecer escala al salir y evitar controladores activos sin interacción.
- Definir región de activación que considere también la distancia al dock en el eje perpendicular; no magnificar por proximidad horizontal si el puntero está fuera de esa región.
- Separar área de selección estable y presentación cuando convenga; asegurar que ninguna superposición capture clics de otro objetivo.
- Elegir interpolación y suavizado sin superponer controladores que compitan por la misma propiedad.
- Mostrar etiquetas mediante acceso por puntero y teclado; para toque, hacer comprensible cada acción sin hover.
- En dispositivos híbridos, volver a estado coherente al alternar métodos de entrada.

**Prompt:** «Diseña magnification para este dock si el espacio y la tarea lo permiten. Haz que la escala varíe continuamente con la proximidad y define el comportamiento de los vecinos. Mantén selección previsible, etiquetas y alternativas de teclado/toque. Justifica distribución, amplitud y radio; comprueba colisiones».

## Blur selectivo: enfoque temporal

**Elegirlo:** cuando dirigir atención temporalmente permita entender mejor un objetivo y los pares puedan perder nitidez sin perjudicar la tarea.
**Reconsiderarlo:** en comparaciones, alertas, datos esenciales o interfaces donde leer todos los valores sea la tarea.

- Identificar exactamente qué contenido puede desenfocarse y durante qué estado.
- Diferenciar `filter: blur(...)`, que afecta al elemento, de `backdrop-filter`, que afecta al fondo detrás; elegir según el objetivo.
- No ligar hover, foco y selección sin una política definida; no borrar una selección persistente solo porque el puntero salió.
- Mantener un modo nítido; retirar el efecto ante fin de inspección, foco en contenido secundario o cambio de contexto según el contrato.
- Especificar cómo recuperar todas las filas nítidas con cualquier entrada admitida. Si el foco permanente impide comparar el conjunto, sustituir el blur por énfasis sin pérdida de lectura.
- Si hay costo elevado de renderizado o pérdida de lectura, ajustar área/intensidad o usar borde, superficie o contraste.
- No presentar el blur como ocultación de información: los datos continúan presentes y requieren control de acceso real si son restringidos.

**Prompt:** «Evalúa blur selectivo para esta sección comparándolo con énfasis estático. Mantén nítido el objetivo y preserva toda información necesaria para decidir. Define entrada, salida y selección; comprueba teclado, toque y recuperación de nitidez. Usa blur solo si aporta al objetivo».

## Combinaciones justificadas

- Permitir shared element en una imagen y crossfade en contenido secundario si cada transición comunica una relación distinta.
- Permitir magnification y etiqueta estática si mejoran exploración y reconocimiento.
- Evitar sumar blur, rebote, escala y fundido al mismo objetivo sin explicar la coordinación.
- En un encargo expresivo, diseñar intensidad y ritmo acordes a la marca; preservar lectura y control.

## Plantilla proporcional al encargo

```text
Objetivo y requisito explícito:
Observaciones / supuestos pendientes:
Técnica o alternativa seleccionada:
Razón y coste frente a alternativa relevante:
Disparador / origen / destino / elemento persistente:
Propiedades / parámetros provisionales / coordinación:
Interrupción y datos pendientes (si aplican):
Foco / semántica / scroll / conservación de datos:
Teclado / puntero / toque / híbridos:
Movimiento reducido / alternativa sin efecto:
Criterios de aceptación:
Comprobado / no comprobado:
```
