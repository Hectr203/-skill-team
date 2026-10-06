---
name: geo-ai-optimization
description: Optimización para motores de búsqueda generativos basados en inteligencia artificial (GEO / AEO). Estructuración de llms.txt, citabilidad algorítmica y formatos para ChatGPT, Claude, Perplexity y Gemini.
---

# Optimización para Motores de IA (GEO / AEO)

Basado en las directivas de Generative Engine Optimization (GEO) y Answer Engine Optimization (AEO) de **Claude SEO** ([github.com/AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo)). Prepara el contenido y la arquitectura del sitio para maximizar su probabilidad de citación en respuestas generadas por modelos de IA.

## Pilares de GEO / AEO

1. **Citabilidad Algorítmica**:
   - Redacción de afirmaciones directas, factuales y respaldadas con fuentes verificables.
   - Definiciones concisas al inicio de secciones para facilitar su extracción por agentes de IA.
   - Tablas comparativas y listas estructuradas que los LLMs pueden sintetizar limpiamente.
2. **Estructuración de `llms.txt`**:
   - Creación del archivo de texto plano `/llms.txt` en la raíz del dominio para orientar a los crawlers de IA sobre la documentación y páginas más relevantes del sitio.
   - Inclusión de descripciones breves por sección con enlaces directos en Markdown.
3. **E-E-A-T (Experiencia, Pericia, Autoridad y Confiabilidad)**:
   - Declaración explícita de autores expertos con perfiles verificables.
   - Notas metodológicas en estudios y artículos técnicos.
   - Cero afirmaciones ambiguas que puedan generar alucinaciones en modelos de lenguaje.
4. **Metadatos e Imágenes**:
   - Textos alternativos (`alt`) explicativos y contextuales en todas las imágenes.
   - Metadatos descriptivos en assets visuales.
