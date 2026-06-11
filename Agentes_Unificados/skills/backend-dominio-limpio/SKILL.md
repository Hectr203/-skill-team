---
name: backend-dominio-limpio
description: Guia arquitectonica y estandares para desarrollar backend SMT con Node.js, Express, TypeScript, PostgreSQL y Prisma bajo Clean Architecture y arquitectura hexagonal.
---

# Habilidad: Backend con Dominio Limpio

## Objetivo
Garantizar que el backend del proyecto SMT se construya con separacion estricta de responsabilidades, bajo acoplamiento, alta cohesion y trazabilidad tecnica, evitando que la logica de negocio quede mezclada con Express o Prisma.

## Arquitectura obligatoria
Todo desarrollo backend debe organizarse por modulos de negocio dentro de `backend/src/modulos/`:

```text
backend/src/modulos/administracion/almacen/
├── dominio/
│   ├── entidades/
│   └── repositorios/
├── aplicacion/
│   ├── casos-uso/
│   └── dto/
├── infraestructura/
│   └── repositorios/
└── interfaces/
    └── http/
        ├── controladores/
        └── rutas.ts
```

## Reglas de implementacion
1. Los controladores HTTP nunca invocan Prisma directamente.
2. Los casos de uso contienen la logica de negocio y dependen de interfaces de repositorio.
3. Los repositorios de infraestructura son la unica capa autorizada para usar Prisma.
4. Las entidades de dominio no deben importar Express, Prisma ni librerias de infraestructura.
5. Toda entrada debe validarse antes de llegar al caso de uso.
6. Las operaciones compuestas deben usar `$transaction` cuando la integridad de datos lo requiera.
7. Los nombres de variables, funciones, DTOs, errores y logs deben mantenerse en espanol, salvo palabras reservadas o convenciones inevitables.

## Restricciones
- Stack obligatorio: Node.js 22 LTS, Express.js, TypeScript, PostgreSQL y Prisma.
- Quedan prohibidos `SQL Server`, `Knex` y accesos paralelos a la persistencia fuera de Prisma.
- No usar consultas SQL crudas salvo excepcion aprobada y documentada.

## Validacion rapida
Antes de cerrar un cambio backend, confirma:

- Separacion correcta entre interfaces HTTP, aplicacion, dominio e infraestructura.
- Uso exclusivo de Prisma en repositorios.
- DTOs y contratos consistentes con frontend.
- Errores y mensajes en espanol.
