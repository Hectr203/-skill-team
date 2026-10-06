---
name: lead-capture
description: Ingestión, mapeo y calificación automática de prospectos a través de webhooks locales, endpoints HTTP y formularios de contacto en SQLite.
---

# Captura y Calificación de Leads

Basado en el subsistema de ingestión de **Auto-CRM** ([github.com/hainrixz/auto-crm](https://github.com/hainrixz/auto-crm)). Automatiza la recepción y almacenamiento estructurado de prospectos comerciales.

## Mecanismos de Captura

1. **Webhooks Locales**:
   - Endpoint HTTP seguro (`POST /api/leads/webhook`) que recibe payloads JSON desde landing pages, formularios web o proveedores de formularios (Tally, Typeform).
2. **Importación CSV**:
   - Parseo determinista de listas de contactos con normalización de emails, teléfonos y nombres de empresa.
3. **Mapeo Automático de Campos**:
   - Extracción de campos estándar: `nombre`, `email`, `telefono`, `empresa`, `origen`, `mensaje_inicial`.

## Calificación Automática de Prospectos
- Asignación de puntaje (*lead scoring*) basado en:
  - Completitud de datos proporcionados.
  - Ajuste al perfil de cliente ideal (ICP).
  - Urgencia declarada en el mensaje.
- Etiquetado de alta prioridad para prospectos con intención de compra inmediata.
- Notificación al equipo mediante los scripts locales de notificación (`scripts/notificar_tarea.py`).
