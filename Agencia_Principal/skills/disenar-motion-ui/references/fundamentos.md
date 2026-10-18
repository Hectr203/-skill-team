# Fundamentos técnicos y fuentes primarias

Fuentes consultadas el 6 de octubre de 2026. Confirmar nuevamente documentación y compatibilidad al implementar una API, especialmente en navegadores objetivo. Estas fuentes apoyan decisiones técnicas; no prueban impacto comercial de las animaciones.

## Pestañas: semántica y activación

Consultar [W3C APG: Tabs Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/).

Relacionar pestaña y panel mediante semántica apropiada, indicar selección y mantener navegación por teclado. La activación automática al recibir foco es una opción cuando mostrar el panel no tiene latencia perceptible; con carga lenta, considerar activación manual. No confundir estado de selección y posición de foco. APG es guía de patrones, no una certificación del producto.

## Preferencias de movimiento

Consultar [Media Queries Level 5](https://www.w3.org/TR/mediaqueries-5/#prefers-reduced-motion) y [W3C: Understanding SC 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html).

Interpretar `prefers-reduced-motion` como una preferencia de la persona y respetarla también en animaciones controladas desde JavaScript. SC 2.3.3 corresponde a nivel AAA y trata la posibilidad de desactivar movimiento no esencial iniciado por interacción. No atribuir conformidad global de WCAG a implementar esta media query. Evaluar fundidos/desenfoque por su efecto perceptivo y conservar función y contenido.

## Transición visual y cambio funcional

Consultar [CSS View Transitions Module Level 1](https://www.w3.org/TR/css-view-transitions-1/).

Usar la separación entre cambio de DOM y representación visual como orientación arquitectónica: una transición omitida no debe impedir el cambio funcional. La aplicación sigue siendo responsable de su concurrencia y de sus datos. Para la API, comprobar unicidad de nombres por captura y tratar rechazo/omisión visual sin repetir operaciones funcionales.

El documento enlazado es una especificación en evolución, no una tabla de soporte de navegadores. Verificar versiones y capacidades en el entorno real. No asumir que navegación dentro de un documento y entre documentos tienen las mismas APIs o requisitos.

## Seleccionar tecnología

Comparar capacidades existentes: CSS para cambios sencillos, APIs de plataforma para efectos que soporten y herramientas del proyecto cuando integren estado/disposición. Introducir biblioteca adicional solo con una razón concreta. Evitar que la skill dependa de una marca, proveedor o versión no verificada.
