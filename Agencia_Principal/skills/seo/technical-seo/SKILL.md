---
name: technical-seo
description: Auditoría y optimización técnica de SEO web. Rastreo, indexabilidad, robots.txt, sitemaps XML, canonización, redirecciones 301/302, encabezados HTTP y Core Web Vitals.
---

# SEO Técnico y Rastreo Web

Basado en las directivas de **Claude SEO** ([github.com/AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo)). Esta skill audita la infraestructura técnica del sitio web para asegurar indexabilidad impecable y tiempos de carga óptimos.

## Áreas de Auditoría Técnica

1. **Rastreo e Indexabilidad**:
   - Validación sintáctica y reglas de bloqueo en `robots.txt`.
   - Generación de `sitemap.xml` dinámico y libre de URLs con código 4xx o 5xx.
   - Verificación de directivas `noindex`, `nofollow` y etiquetas `<meta name="robots">`.
2. **Canonización y Enlaces**:
   - Asignación estricta de `<link rel="canonical" href="...">` para evitar contenido duplicado.
   - Detección y corrección de cadenas de redirecciones o bucles 301/302.
   - Enlazado interno con textos ancla semánticos y distribución de PageRank.
3. **Rendimiento y Core Web Vitals**:
   - **LCP (Largest Contentful Paint)**: Optimización de imágenes en formatos modernos (WebP/AVIF), preloading de fuentes críticas y CSS inline esencial.
   - **INP (Interaction to Next Paint)**: Minimización de bloqueo del hilo principal en JavaScript y debouncing de eventos pesados.
   - **CLS (Cumulative Layout Shift)**: Dimensiones explícitas (`width` y `height`) en imágenes, videos y banners.

## Criterios de Aceptación Falsables
Toda recomendación técnica debe incluir:
- Evidencia observable (URL, línea de código o encabezado HTTP analizado).
- Indicador cuantificable (ej. "reducir LCP de 3.2s a <2.5s").
- Criterio de falsabilidad: cómo demostraríamos que la solución no tuvo efecto.
