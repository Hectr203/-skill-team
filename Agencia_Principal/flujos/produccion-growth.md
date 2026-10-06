# Flujo de Proyecto en Producción: Operación, Crecimiento y Mantenimiento

Este flujo se activa cuando la aplicación ya está desplegada y accesible para usuarios reales, conectando la observabilidad operativa con el crecimiento comercial y el posicionamiento orgánico.

---

## Pilares del Ciclo de Producción

```text
1. Monitoreo & Logs ──> 2. Auditoría Continua SEO ──> 3. Pipeline de Conversión (CRM) ──> 4. Estrategia de Contenidos ──> 5. Growth Loops
```

---

### Pilar 1: Monitoreo y Salud Operativa
- Detección proactiva de errores en runtime (HTTP 5xx, excepciones no capturadas).
- Compresión semántica de salidas de depuración y logs masivos mediante **Headroom** para no saturar la ventana de tokens al inspeccionar incidentes.
- Verificación de métricas de infraestructura (CPU, memoria, latencia de base de datos).

### Pilar 2: Auditoría Continua de Posicionamiento (Claude SEO)
- Monitoreo periódico de indexabilidad y prevención de regresiones de rastreo.
- Seguimiento de Core Web Vitals reales en producción.
- Verificación de citabilidad algorítmica en motores de IA (GEO / AEO) y actualización de `/llms.txt`.

### Pilar 3: Optimización del Embudo Comercial (Auto-CRM)
- Recepción de prospectos capturados a través de formularios web y webhooks locales en SQLite.
- Calificación automática de leads y emisión de alertas de deals estancados para el equipo comercial mediante `scripts/notificar_tarea.py`.
- Consultas conversacionales privadas vía comandos MCP (`/pipeline`, `/deals`, `/summary`).

### Pilar 4: Distribución en Redes Sociales (Social Media Skills)
- Estrategia de contenidos bajo el perfil aislado de voz de marca (`contexts/brands/<brand-id>/voice.md`).
- Redacción técnica para LinkedIn y guiones audiovisuales para video corto (Reels / Shorts).
- Evaluación previa de publicaciones con `post-scorer` (umbral > 75/100).
- **Compuerta HITL estricta**: Toda publicación externa requiere confirmación explícita del usuario.

### Pilar 5: Experimentos de Crecimiento (Growth Loop)
- Pruebas A/B de copys, páginas de aterrizaje y llamados a la acción (CTAs).
- Detección de cuellos de botella en la activación y retención de usuarios.
