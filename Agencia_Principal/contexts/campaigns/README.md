# Gestión de Campañas y Lanzamientos — Agencia Principal

Este directorio contiene la planificación, seguimiento de métricas y entregables de campañas de marketing, lanzamientos digitales y optimizaciones de crecimiento coordinadas por el agente `growth` y el flujo `flujos/campana-lanzamiento.md`.

---

## 1. Estructura de Campañas

Cada campaña activa se documenta en `contexts/campaigns/<id_campana>/`:

```txt
contexts/campaigns/<id_campana>/
├── brief.md                   # Objetivos, KPIs, presupuesto, fechas y público objetivo
├── activos/                   # Guiones, copys de anuncios, piezas visuales y correos
└── resultados.md              # Métrica de rendimiento, conversiones y retroalimentación
```

---

## 2. Plantilla Base para `brief.md`

```markdown
# Brief de Campaña: [Nombre de la Campaña]

- **ID de Campaña:** [slug-campana]
- **Marca / Cliente:** [Vincular a contexts/brands/ o contexts/clients/]
- **Objetivo Primario:** [Generación de leads / Tráfico web / Branding / Lanzamiento producto]
- **KPIs Medibles:** [Ejemplo: 500 registros calificados con CAC < $15 USD]
- **Canales de Difusión:** [LinkedIn / Meta / Google Ads / Email Marketing]
- **Fecha de Inicio:** [AAAA-MM-DD]
- **Fecha de Cierre:** [AAAA-MM-DD]
```
