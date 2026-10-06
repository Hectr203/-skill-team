# Flujo de Gestión Comercial y Pipeline de Ventas (Auto-CRM)

Este flujo establece la captura, calificación y seguimiento soberano de prospectos comerciales mediante una base de datos local SQLite, garantizando total privacidad sin enviar datos sensibles a plataformas externas.

---

## Fases del Flujo

```text
1. Captura de Leads ──> 2. Calificación Automática ──> 3. Pipeline Visual ──> 4. Alertas de Estancamiento ──> 5. Cierre y Métricas
```

### Fase 1: Captura de Prospectos
1. Recepción de payloads JSON desde landing pages o formularios web en el webhook local (`POST /api/leads/webhook`).
2. Sanitización y normalización de datos en SQLite local (`nombre`, `email`, `telefono`, `empresa`, `origen`, `mensaje`).

### Fase 2: Calificación Automática (Lead Scoring)
1. Evaluación de completitud de datos y perfil del cliente ideal (ICP).
2. Asignación de prioridad (Baja, Media, Alta) y etiquetado automático del requerimiento técnico o comercial.

### Fase 3: Pipeline Comercial y Seguimiento
1. Avance visual a través de las etapas del embudo:
   - `Lead Nuevo` -> `Calificado` -> `Propuesta / Demo` -> `Negociación` -> `Ganado / Perdido`.
2. Registro cronológico de notas técnicas, llamadas y acuerdos en la base de datos local.

### Fase 4: Monitoreo de Deals Estancados
1. Detección automática de oportunidades sin interacción en más de 7 días.
2. Generación de avisos locales mediante `scripts/notificar_tarea.py` para sugerir acciones de reactivación.

### Fase 5: Consultas Conversacionales Vía MCP
- Consulta del estado comercial en lenguaje natural mediante el servidor MCP de Auto-CRM:
  - `/pipeline`: Visión general del embudo de ventas.
  - `/deals`: Lista de oportunidades abiertas y valores estimados.
  - `/summary`: Tasa de conversión y valor total en pipeline.

---

## Compuertas Human-in-the-Loop
- El análisis y seguimiento en base de datos local es autónomo.
- **Toda interacción externa** (enviar correos comerciales, mensajes de WhatsApp o proponer contratos formales) requiere aprobación explícita del usuario.
