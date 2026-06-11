---
name: prisma-base-de-datos
description: Guia y convenciones para el uso obligatorio de Prisma con PostgreSQL en SMT, incluyendo modelos, migraciones, semillas, repositorios y transacciones.
---

# Habilidad: Prisma y Base de Datos

## Objetivo
Definir una capa de persistencia consistente para SMT usando PostgreSQL y Prisma, con modelos claros, migraciones trazables y repositorios alineados a la arquitectura hexagonal.

## Reglas de modelado en `schema.prisma`
1. Los modelos se nombran en espanol, singular y `PascalCase`: `Usuario`, `Ruta`, `Unidad`.
2. Los campos se nombran en espanol y `camelCase`, sin acentos por compatibilidad tecnica: `nombreComercial`, `kilometrosReales`.
3. Todo modelo debe incluir:

```prisma
id            String    @id @default(cuid())
creadoEn      DateTime  @default(now())
actualizadoEn DateTime  @updatedAt
```

4. Cuando aplique borrado logico, agrega `eliminadoEn DateTime?`.
5. Las relaciones deben declararse de forma explicita con sus campos relacionales y referencias.

## Acceso a datos
1. `PrismaClient` debe inicializarse como singleton en `src/config/prisma.ts`.
2. Los controladores HTTP jamas importan Prisma.
3. Solo los repositorios de infraestructura pueden acceder a Prisma.
4. Los casos de uso dependen de interfaces de repositorio, no de implementaciones Prisma.

## Transacciones y consistencia
- Usa `$transaction` cuando una operacion involucre varias escrituras dependientes.
- Evita cambios parciales que rompan integridad referencial o trazabilidad.
- Define indices y restricciones solo cuando respondan a necesidades reales del dominio.

## Migraciones y semillas
1. Toda modificacion de `schema.prisma` debe generar una migracion con nombre claro en espanol.
2. Nunca reescribas una migracion ya aplicada; corrige con una nueva.
3. Las semillas viven en `prisma/seed.ts` y deben poblar catalogos y datos iniciales controlados.

## Restricciones
- PostgreSQL es el motor definitivo.
- Prisma es el ORM obligatorio.
- Quedan prohibidos `SQL Server`, `Knex` y consultas SQL crudas como practica comun.
- Si una consulta cruda es inevitable, debe justificarse, documentarse y aprobarse.
