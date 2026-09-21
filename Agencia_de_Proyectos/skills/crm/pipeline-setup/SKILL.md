---
name: pipeline-setup
description: Configuración del pipeline comercial y etapas de ventas para gestión de leads local y soberana con Auto-CRM.
---

# Configuración del Pipeline Comercial

Basado en la arquitectura comercial de **Auto-CRM** ([github.com/hainrixz/auto-crm](https://github.com/hainrixz/auto-crm)). Define las fases de venta para el seguimiento ordenado de oportunidades sin depender de plataformas SaaS externas.

## Etapas del Pipeline Comercial

1. **Lead Entrante (Nuevo)**: Prospecto recién capturado pendiente de primer contacto o verificación.
2. **Calificado (Contacto Inicial)**: Se determinó que el prospecto tiene necesidad real, presupuesto aproximado y capacidad de decisión.
3. **Propuesta / Demostración**: Se ha entregado una cotización formal, prototipo o demostración de software.
4. **Negociación / Revisión**: Ajuste de términos, alcance o contrato.
5. **Cierre Ganado (Won)**: Acuerdo firmado e inicio de onboarding.
6. **Cierre Perdido (Lost)**: Oportunidad descartada, con registro obligatorio del motivo de pérdida para retroalimentación.

## Reglas de Operación
- Toda oportunidad registra: nombre del lead, empresa, valor estimado, fecha de última interacción y próxima acción programada.
- Detección automática de **deals estancados**: alertas para cualquier oportunidad sin actividad en más de 7 días.
- Soberanía total: la base de datos reside en SQLite local, preservando la confidencialidad de clientes y montos.
