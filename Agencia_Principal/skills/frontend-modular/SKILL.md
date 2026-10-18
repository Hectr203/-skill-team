---
name: frontend-modular
description: Organiza o revisa frontend por módulos de negocio autocontenidos con componentes, hooks, servicios, estado y contratos. Usar al crear o integrar módulos del perfil modular; no impone una migración completa ni un framework en otros perfiles.
---

# Frontend modular

Aplicar el [contrato común](../../agentes/contrato-agente.md), el manifiesto y la [arquitectura del perfil](../../stacks/estandar/arquitectura-frontend.md). Ubicar cada cambio en el módulo del negocio; compartir solo recursos genéricos realmente reutilizados. Revisar entrada pública, separación de presentación/lógica/servicios y dependencias sin ciclos. No acceder a interiores de otros módulos ni mezclar datos de clientes.

Conservar estructura existente fuera del alcance autorizado. Leer recursos relativos desde esta fuente. Una conversión UI externa se adapta al lenguaje, módulos y librerías del perfil antes de integrar. Entregar mapa de módulos afectados y controles realmente ejecutados; esta skill no es un linter ni amplía permisos.
