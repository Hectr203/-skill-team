---
name: schema-markup
description: Generación y validación de datos estructurados JSON-LD Schema.org para enriquecer fragmentos de búsqueda (rich snippets) y clarificar entidades ante motores de búsqueda.
---

# Datos Estructurados y Marcado Schema.org

Basado en el módulo de microdatos de **Claude SEO** ([github.com/AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo)). Define la semántica formal del sitio web mediante bloques `<script type="application/ld+json">`.

## Esquemas Principales Soportados

1. **Organización y Marca (`Organization`)**:
   - Nombre legal, URL canónica, logotipo corporativo, perfiles sociales verificados (`sameAs`) y datos de contacto.
2. **Sitio Web y Búsqueda (`WebSite`)**:
   - Nombre de marca, URL base y habilitación de `SearchAction` (caja de búsqueda integrada en Google).
3. **Comercio Electrónico (`Product` & `Offer`)**:
   - Nombre, descripción, SKU, precio, moneda (`ISO 4217`), disponibilidad (`InStock` / `OutOfStock`), valoraciones de clientes (`AggregateRating`).
4. **Artículos y Blogs (`Article` / `BlogPosting`)**:
   - Titular, fecha de publicación, fecha de modificación (`dateModified`), autor verificado y editor (`Publisher`).
5. **Negocio Local (`LocalBusiness`)**:
   - Dirección física (`PostalAddress`), coordenadas geográficas, horario de atención y teléfono.
6. **Preguntas Frecuentes (`FAQPage`)**:
   - Pares estructurados de preguntas (`Question`) y respuestas aceptadas (`Answer`).

## Reglas de Implementación
- Inyección limpia en el `<head>` de la página sin duplicaciones.
- Validación de sintaxis estricta contra la especificación oficial de Schema.org.
- Verificación contra Google Rich Results Validator antes de confirmar la entrega.
