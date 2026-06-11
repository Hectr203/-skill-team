---
name: backend-dominio-limpio
description: Guía arquitectónica y estándares de código para el desarrollo del backend (Node.js/Prisma) basado en Clean Architecture y Domain-Driven Design para el sistema Tutti Bocado.
---
# Skill: Backend con Dominio Limpio

## Objetivo
Garantizar la sostenibilidad, escalabilidad y legibilidad del código backend del CEDIS Tutti Bocado mediante la separación estricta de responsabilidades y la organización por dominios de negocio.

## Arquitectura de Sistema (Clean Architecture)
El diseño garantiza que la lógica de negocio central (reglas de almacén, FIFO, validación de permisos operativos) no esté acoplada al framework HTTP ni a la base de datos.
- **Capa de Aplicación (Rutas/Controladores):** Maneja solicitudes HTTP, middlewares de autenticación (JWT/Geolocalización) y transformaciones de DTOs.
- **Capa de Dominio (Servicios):** Orquesta los flujos de negocio como la validación de órdenes de compra, control de horarios para pedidos de sucursal y lógica FIFO.
- **Capa de Infraestructura (Repositorios/Prisma):** Exclusiva para la persistencia y lectura en PostgreSQL (con mapeos para evitar filtrar hashes o data sensible).

## Estructura de Directorios
Todo nuevo desarrollo backend debe ser alojado como un dominio modular en `src/modules/<nombre-dominio>/`:

```text
/modules/pedidos/
├── pedidos.routes.ts       # Endpoints REST y asignación de middlewares/guards
├── pedidos.controller.ts   # Manejo de Req/Res, captura de errores HTTP
├── pedidos.service.ts      # Lógica pura de negocio (ej. validación de horario, stock)
└── pedidos.repository.ts   # Consultas específicas con Prisma
```

## Reglas y Restricciones de Implementación
1. **Separación Estricta:** Un controlador NUNCA debe invocar a Prisma directamente. El controlador delega al servicio, y el servicio delega al repositorio.
2. **Trazabilidad Inmutable:** Toda acción de escritura/actualización (ej. autorizar un retorno) debe generar un log de auditoría (Soft-delete obligatorio).
3. **Transacciones:** Operaciones compuestas (ej. descontar stock y generar ticket de salida) deben usar `$transaction` de Prisma para mantener integridad relacional.
4. **Nomenclatura Híbrida:** Archivos en `kebab-case`. Métodos de dominio en `camelCase` español (ej. `validarHorarioPedido()`, `calcularMermaDiaria()`). Términos técnicos estructurales (middlewares, interfaces) en inglés.
