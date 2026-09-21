---
name: frontend-design
description: Creación de interfaces frontend de clase mundial con diseño distintivo y alta calidad estética. Evita plantillas genéricas o estética de IA genérica. Aplica dirección artística audaz, tipografía cuidada, paletas intencionales y animaciones con propósito.
---

# Diseño de Frontend Distintivo y Producción de Élite

Esta skill guía la concepción y desarrollo de interfaces frontend que destacan por su identidad visual única, evitando completamente el "AI slop" o estética genérica de modelos de IA (como fuentes del sistema comunes, sombras toscas o gradientes morados repetitivos).

---

## 1. Repositorios y Fuentes de Referencia
* **Estándares de Apple**: [developer.apple.com/design](https://developer.apple.com/design/human-interface-guidelines/)
* **Emil Kowalski Design Engineering**: [github.com/emilkowalski/skills](https://github.com/emilkowalski/skills)
* **React Bits**: [reactbits.dev](https://www.reactbits.dev/) / [github.com/DavidHDev/react-bits](https://github.com/DavidHDev/react-bits)
* **Anime.js**: [animejs.com](https://animejs.com/) / [github.com/juliangarnier/anime](https://github.com/juliangarnier/anime)
* **UI/UX Pro Max**: [`../ui-ux-pro-max/SKILL.md`](../ui-ux-pro-max/SKILL.md)

---

## 2. Pensamiento de Diseño Previo al Código

Antes de escribir una sola línea de código frontend, define con claridad:
1. **Propósito**: ¿Qué problema resuelve la vista? ¿Quién la usa?
2. **Tono Visual Específico**: Elige una dirección intencional:
   - *Minimalismo refinado suizo*: Líneas limpias, tipografía protagonista, espacio negativo generoso.
   - *Lujo sobrio / Dark Mode Apple*: Fondos carbón (`#0B0D0E`), vidrio esmerilado, iluminación periférica.
   - *Retro-futurista / Cyberpunk sutil*: Tipografías monoespaciadas técnicas, bordes con acentos de color cian/ámbar.
   - *Editorial contemporáneo*: Títulos display elegantes con serifa acompañados de texto sans-serif limpio.
3. **Elemento Inolvidable**: Define cuál es la interacción o detalle visual que causará admiración al usuario (ej. un hover 3D con TiltCard, una animación SVG fluida de carga o un contador dinámico con Anime.js).

---

## 3. Directrices Estéticas Innegociables

### A. Tipografía
* Evitar fuentes genéricas como Arial, Roboto o Inter estándar sin personalidad.
* Preferir combinaciones con carácter:
  - Display / Títulos: *Geist Sans*, *Outfit*, *Clash Display*, *Plus Jakarta Sans*, *Syne*.
  - Cuerpo / Lectura: *Inter Tight*, *Geist*, *Work Sans*, *DM Sans*.
  - Monospaced / Código / Métricas: *Geist Mono*, *JetBrains Mono*, *Space Mono*.
* Aplicar tracking negativo en títulos grandes (`letter-spacing: -0.02em` a `-0.03em`) para mayor densidad y elegancia.

### B. Color y Tema
* Crear una paleta con jerarquía 60-30-10:
  - 60% color dominante de superficie (luz o carbón profundo).
  - 30% color estructural secundario (bordes sutiles, tarjetas, texto atenuado).
  - 10% acento vibrante (botones de acción principal, indicadores de foco).
* Utilizar variables CSS para consistencia semántica.

### C. Profundidad y Superficies
* Prohibidas las sombras negras pesadas (`0 10px 20px rgba(0,0,0,0.5)`).
* Aplicar la técnica de sombras en capas multicapa descrita en [`../apple-design/SKILL.md`](../apple-design/SKILL.md).
* En modo oscuro, resaltar los límites de los componentes mediante un borde interior sutil (`inset 0 1px 0 rgba(255, 255, 255, 0.08)`).

### D. Composición Espacial
* Ruptura calculada de cuadrículas: superposiciones controladas, tarjetas con asimetría elegante, sangrías generosas.
* Densidad de información calibrada según la naturaleza de la pantalla (alta densidad en dashboards y tablas de datos, baja densidad en landing pages de conversión).

---

## 4. Integración con el Ecosistema de Diseño de la Agencia
* Para la base de datos de estilos, paletas y gráficos: consultar [`../ui-ux-pro-max/SKILL.md`](../ui-ux-pro-max/SKILL.md).
* Para físicas de resorte y tiempos de respuesta: consultar [`../emil-design-eng/SKILL.md`](../emil-design-eng/SKILL.md) y [`../animation-vocabulary/SKILL.md`](../animation-vocabulary/SKILL.md).
* Para componentes de animación interactiva en React: consultar [`../react-bits/SKILL.md`](../react-bits/SKILL.md).
* Para animaciones SVG y timelines fluidos: consultar [`../animejs-motion/SKILL.md`](../animejs-motion/SKILL.md).
