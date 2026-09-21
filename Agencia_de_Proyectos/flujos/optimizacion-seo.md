# Flujo de Optimización SEO y Posicionamiento en IA (GEO)

Este flujo establece el proceso metódico para auditar, optimizar y monitorear la visibilidad orgánica de una aplicación en motores de búsqueda tradicionales (Google, Bing) y motores generativos de inteligencia artificial (ChatGPT, Claude, Perplexity, Gemini).

---

## Fases del Flujo

```text
1. Reconocimiento Técnico ──> 2. Auditoría Falsable ──> 3. Schema & Semántica ──> 4. Optimización GEO ──> 5. Verificación de Regresiones
```

### Fase 1: Reconocimiento Técnico y Rastreo
1. Inspeccionar `robots.txt` y verificar que las rutas públicas sean accesibles para los User-Agents de búsqueda y LLMs.
2. Generar y validar `sitemap.xml` dinámico.
3. Auditar encabezados HTTP: verificar presencia de directivas de seguridad (`Content-Security-Policy`, `X-Content-Type-Options`) y códigos de estado limpios (cero bucles 301/302 o enlaces rotos 404).

### Fase 2: Auditoría Falsable y Core Web Vitals (Claude SEO)
1. Ejecutar auditoría técnica cuantitativa (escala 0-100) evaluando:
   - **LCP (< 2.5s)**: Optimización de imágenes en formatos modernos (WebP/AVIF), preloading de fuentes críticas.
   - **INP (< 200ms)**: Minimización del bloqueo del hilo principal en scripts de cliente.
   - **CLS (< 0.1)**: Dimensiones fijas en banners y elementos multimedia.
2. Formular recomendaciones bajo el principio de falsabilidad: cada hallazgo debe declarar cómo demostraríamos si la corrección falló.

### Fase 3: Estructuración Semántica y Schema.org JSON-LD
1. Implementar bloques de datos estructurados `<script type="application/ld+json">` según la naturaleza de cada vista:
   - `WebSite` y `Organization` en la página principal.
   - `Product` y `Offer` en e-commerce.
   - `Article` o `BlogPosting` en contenidos informativos.
   - `FAQPage` en secciones de preguntas frecuentes.
2. Validar sintaxis contra el validador oficial de resultados enriquecidos de Google.

### Fase 4: Optimización para Motores de IA (GEO / AEO)
1. Crear y publicar el archivo `/llms.txt` en la raíz del proyecto para facilitar el rastreo algorítmico por modelos de lenguaje.
2. Redactar definiciones claras, directas y factuales al inicio de cada sección temática.
3. Incorporar tablas comparativas y metadatos explícitos que faciliten la citabilidad por LLMs.

### Fase 5: Prevención de Regresiones de Tráfico Orgánico
1. Comparar métricas contra el snapshot anterior antes de autorizar un despliegue crítico a producción.
2. Comprobar que ningún cambio de enrutamiento elimine slugs indexados sin la correspondiente redirección 301.

---

## Compuertas Human-in-the-Loop
- La auditoría técnica y los reportes de diagnóstico son de solo lectura y autónomos.
- Cualquier modificación de archivos de producción (`robots.txt`, redirecciones en servidor o despliegues) requiere aprobación previa.
