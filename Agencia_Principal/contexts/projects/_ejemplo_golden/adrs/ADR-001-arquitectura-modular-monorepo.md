# ADR-001: Conservación de Arquitectura Modular y Separación por Casos de Uso

- **Estado:** Aceptado
- **Fecha:** 2026-09-20
- **Decisores:** Arquitecto de Software, Director de Proyecto

## Contexto
El sistema `vtptransportes` es una base de código en producción que maneja liquidaciones operativas críticas. Se evaluó reescribir el backend a microservicios independientes, pero esto implicaría riesgo de regresión en las transacciones contables y mayor complejidad de despliegue.

## Decisión
Se conserva el monolito modular existente estructurado por dominios (`modules/fletes`, `modules/rutas`, `modules/conductores`). Se adopta la regla de Clean Architecture: los controladores HTTP sólo desempaquetan peticiones y delegan a Casos de Uso puros desacoplados del framework web, validados mediante esquemas Zod estrictos.

## Consecuencias
- **Positivas:** Cero riesgo de fragmentación de datos, despliegues atómicos simples, testing directo de lógica de negocio sin levantar servidores HTTP.
- **Negativas:** La base de código reside en un solo repositorio; requiere disciplina en la frontera de módulos para evitar acoplamientos circulares.
