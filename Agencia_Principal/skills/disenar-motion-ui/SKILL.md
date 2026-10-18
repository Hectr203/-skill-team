---
name: disenar-motion-ui
description: Diseñar, evaluar, especificar o implementar movimiento en interfaces web con crossfade, shared element, magnification y blur selectivo, comparando también alternativas estáticas. Usar para transiciones de UI, continuidad tarjeta-detalle, docks con efecto lupa, foco visual, revisión de animaciones o aplicación de las técnicas del reel de Santa IA. No activar para edición de video, motion graphics audiovisuales ni diseño visual general sin un encargo de movimiento o interacción.
---

## Integración en Agencia Principal
Aplicar el [contrato de selección y coordinación](../../agentes/contrato-agente.md). Activar esta habilidad solo si su resultado corresponde al alcance autorizado; los ejemplos de stack y herramientas no sustituyen el manifiesto. Recursos relativos se resuelven desde esta fuente. No ampliar permisos, invocar procesos recursivos ni declarar controles no ejecutados.


# Diseñar movimiento de interfaz con criterio

Resolver el encargo mediante movimiento intencional, identidad visual coherente y comportamiento verificable. Tratar las cuatro técnicas como opciones, no como un catálogo obligatorio ni como prueba de calidad.

## Referencias de consulta

- Leer [patrones.md](references/patrones.md) al elegir o implementar una técnica; incluye condiciones, fallos y prompts.
- Leer [evaluacion.md](references/evaluacion.md) al revisar una propuesta o verificar una implementación.
- Consultar [fundamentos.md](references/fundamentos.md) para semántica, preferencias de movimiento y selección tecnológica.
- Consultar [fuente.md](references/fuente.md) cuando se requiera fidelidad al reel o atribución.

## 1. Delimitar el trabajo

Identificar objetivo, público/tarea, contexto, contenido, dispositivos, capacidades de entrada, restricciones y entregable: análisis, especificación, prototipo o código.

Revisar componentes, tokens, documentación y dependencias reales. Usar `DESIGN.md` cuando exista, resolviendo sus conflictos con instrucciones actuales del usuario. No suponer que la herramienta, el framework ni la marca del reel corresponden al proyecto.

Preguntar solo por información cuya ausencia cambie una decisión sustancial. Declarar supuestos reversibles y avanzar con lo disponible. Conservar el alcance: una especificación no autoriza modificar una aplicación.

## 2. Separar evidencia, intención y preferencia

- Distinguir observaciones de la referencia, requisitos explícitos, hipótesis de diseño y restricciones verificadas.
- Formular una intención concreta: orientar durante navegación, reconocer un cambio, localizar una acción, enfocar contenido o expresar personalidad.
- Reconocer la expresividad y el disfrute como objetivos legítimos si forman parte del encargo; no imponer sobriedad a todos los productos.
- No equiparar más movimiento, minimalismo, rapidez, un proveedor o una estética con mejor diseño.
- No prometer mayor conversión, usabilidad o apariencia «premium» sin evidencia relevante. Proponer cómo comprobar una hipótesis.
- No asignar habilidades, preferencias o necesidades a personas por edad, región u otras categorías generales. Diseñar a partir de requisitos y condiciones conocidas.
- Mantener abierta la elección de técnica, combinación o alternativa estática. No forzar ausencia de movimiento ni las cuatro animaciones.
- Diferenciar fidelidad solicitada de adaptación: reproducir un efecto nombrado cuando sea viable; explicar una limitación concreta si requiere una alternativa.

## 3. Elegir por contexto

| Intención | Candidato | Condición decisiva | Alternativa a comparar |
| --- | --- | --- | --- |
| Sustituir contenido en un mismo contexto | Crossfade | Existe un cambio de estado claro y el solapamiento conserva comprensión | Cambio directo con selección visible |
| Mostrar continuidad entre dos representaciones | Shared element | Existe un elemento reconocible y una correspondencia espacial útil | Navegación normal o fundido localizado |
| Explorar un menú con respuesta al puntero | Magnification | Las capacidades de entrada, el espacio y las zonas de interacción permiten escala progresiva | Menú estable con foco/selección |
| Dirigir atención a un objetivo temporal | Blur selectivo | La nitidez de los pares no es necesaria en ese momento | Borde, superficie, contraste o separación |

Comparar solo opciones relevantes. Explicar la elección mediante el objetivo y los costes concretos de lectura, interacción, implementación y mantenimiento. No inventar puntuaciones ni umbrales universales. Si el usuario solicita una técnica, priorizar su evaluación y adaptación.

Tratar la tabla como un conjunto acotado, no exhaustivo. Si la necesidad requiere carga, arrastre, confirmación u otro patrón, identificarlo sin forzarlo dentro de estas cuatro técnicas; ampliar el diseño al patrón pertinente cuando el alcance lo permita.

## 4. Especificar el comportamiento antes del código

Definir, en formato proporcional al alcance:

1. Objetivo y criterio observable de éxito.
2. Disparador, estado de origen/destino y contenido que permanece.
3. Propiedades, geometría, duración, curva y coordinación entre elementos.
4. Estado funcional y estado temporal de animación, como conceptos separados.
5. Política de interrupción: completar, invertir, sustituir o cancelar, según la interacción.
6. Datos pendientes, vacíos, error y respuestas fuera de orden cuando existan.
7. Foco, semántica, selección, scroll y conservación de datos introducidos.
8. Teclado, puntero, toque, dispositivos híbridos y movimiento reducido.
9. Alternativa funcional sin el efecto y condición para usarla.
10. Validación disponible y limitaciones pendientes.

Tomar tiempos y escalas del sistema de diseño o calibrarlos con un prototipo. Si faltan, elegir valores provisionales explícitos; no convertir los ejemplos en valores obligatorios. Comparar con la experiencia sin animación. No retrasar una acción funcional solo para completar su presentación.

## 5. Respetar los invariantes de cada patrón

### Crossfade

Solapar visualmente salida y entrada de forma que el reemplazo sea comprensible; evitar doble contenido legible durante demasiado tiempo. No exigir duplicar el DOM: usar capas o capturas según la implementación.

Mantener una sola representación funcional/semántica activa. No ocultar del árbol accesible un elemento que conserve foco. En pestañas, conservar roles, relaciones, selección y navegación adecuados; distinguir activación manual y automática según la latencia.

Resolver alturas variables, texto ampliado y contenido tardío sin recortes. No imponer animación de altura ni mediciones por fotograma como solución universal.

### Shared element

Elegir un recurso reconocible y relacionar su representación de origen y destino mediante identidad estable. Coordinar posición/tamaño y contenido; evitar duplicación visible, estiramiento de texto y saltos de scroll.

Conservar navegación y gestión del foco según el patrón: cambio de panel, diálogo y cambio de página no tienen la misma política. Prever que el origen no exista al volver.

Usar transición como mejora del cambio de estado. Si la animación no se ejecuta, mantener navegación y datos correctos. Cancelar la transición visual no equivale a cancelar una operación de datos.

### Magnification

Calcular escala continua a partir de proximidad en coordenadas consistentes. Usar referencias geométricas independientes del tamaño animado; invalidarlas ante cambios de disposición.

Elegir una distribución adecuada, sin imponer una fórmula. Limitar escala/alcance y coordinar vecinos, etiquetas y espacio. Mantener zonas pulsables previsibles sin colisiones que impidan seleccionar.

Responder a las capacidades de entrada reales; no deducir hover por ancho de pantalla. El menú debe funcionar al alternar ratón, teclado y toque. No imponer igual movimiento a todas las entradas: preservar acceso y selección equivalentes.

### Blur selectivo

Mantener nítido el objetivo y aplicar desenfoque únicamente a elementos secundarios pertinentes. Evitar desenfocar el objetivo mediante un ancestro.

No reducir la legibilidad de valores necesarios para decidir, comparar o detectar errores. Restaurar nitidez de manera previsible. No esconder controles enfocados ni usar blur como protección de información.

No equiparar selección visual, foco del teclado y selección de datos. Definir explícitamente qué estado dispara el efecto y cómo se abandona, incluyendo toque.

## 6. Implementar según el entorno

Reutilizar el sistema existente cuando sea adecuado. Elegir CSS, API de plataforma o biblioteca por capacidades, compatibilidad real, mantenimiento y coste; ninguna categoría es obligatoria. Justificar una dependencia nueva si mejora el resultado respecto a alternativas disponibles.

Comprobar documentación vigente antes de usar APIs desconocidas o asumir compatibilidad. Implementar mejora progresiva y limpieza de eventos, observadores, capas y animaciones.

Separar presentación de las operaciones de datos. Para cambios de navegación/panel, impedir que una respuesta antigua sustituya la selección actual; para acciones transaccionales, respetar la política funcional del producto. No aplicar «última acción gana» a guardados o pagos por analogía con pestañas.

Evaluar rendimiento en el contexto: no garantizar aceleración de GPU ni fluidez por usar transformaciones. Evitar medir geometría y escribir estilos repetidamente sin necesidad; no imponer un controlador de animación permanente para efectos ocasionales.

## 7. Preservar acceso y control

Mantener contenido, foco visible y operaciones disponibles sin animación. Respetar preferencias de movimiento en CSS y en controladores de JavaScript; responder si cambian durante la sesión.

Sustituir desplazamientos/escalados no esenciales por una alternativa compatible con la preferencia del usuario. Evaluar fundidos y blur por su efecto perceptivo; no exigir desactivar cualquier transición ni afirmar que una media query acredita cumplimiento integral de accesibilidad.

Usar movimiento para comunicar sin convertirlo en el único indicador de selección, error o éxito. Mantener lectura, texto ampliado, etiquetas y comprensión del estado.

## 8. Verificar y entregar

Aplicar [evaluacion.md](references/evaluacion.md) a los casos pertinentes. En una especificación, entregar criterios comprobables; en código, ejecutar comprobaciones relevantes y revisar visualmente si el entorno lo permite. No afirmar pruebas de usuario, rendimiento o accesibilidad que no se hayan realizado.

Entregar el resultado solicitado, la razón de las decisiones importantes, qué se comprobó y qué queda pendiente. Evitar añadir documentación o pruebas que solo repitan la implementación. No afirmar que la solución está libre de sesgos ni que es la mejor posible sin comparación verificable.
