---
name: prisma-base-de-datos
description: Guía y convenciones para el uso de Prisma ORM con PostgreSQL en el backend, incluyendo diseño de modelos, transacciones, migraciones y seeds.
---

# Skill: Prisma y Base de Datos (PostgreSQL)

## Objetivo
Definir las reglas y convenciones para la gestión de la base de datos usando Prisma ORM, garantizando un esquema limpio, consistente y preparado para escalar.

## Reglas de Modelado en `schema.prisma`

1.  **Nomenclatura Obligatoria:**
    *   **Modelos (Tablas):** `PascalCase` singular en inglés o español, pero Prisma usa convención PascalCase (ej. `model Usuario`, `model Ruta`).
    *   **Campos (Columnas):** `camelCase` en español (ej. `nombreComercial`, `kilómetrosReales`).
    *   **Comentarios:** Usar `///` para comentarios que se reflejen en los tipos generados y `//` para anotaciones internas.

2.  **Identificadores y Timestamps:**
    *   Todo modelo debe tener un ID tipo CUID: `id String @id @default(cuid())`
    *   Todo modelo debe registrar su creación y actualización:
        ```prisma
        creadoEn      DateTime  @default(now())
        actualizadoEn DateTime  @updatedAt
        ```

3.  **Soft Deletion (Borrado Lógico Obligatorio):**
    *   **NUNCA** eliminar registros físicamente. Todo modelo susceptible de borrado debe incluir `eliminadoEn DateTime?`.
    *   Los repositorios deben filtrar siempre `where: { eliminadoEn: null }`.
    *   Para eliminar, usar `update({ where: { id }, data: { eliminadoEn: new Date() } })`.

4.  **Relaciones (1:1, 1:N, N:M):**
    *   Definir claramente los campos relacionales, ej:
        ```prisma
        chofer   Chofer @relation(fields: [choferId], references: [id])
        choferId String
        ```
    *   Usar onDelete y onUpdate de forma explícita si se requiere comportamiento en cascada (aunque preferiblemente controlarlo a nivel de código con soft deletes).

## Acceso a Datos y Repositorios

1.  **Aislamiento de Prisma Client:**
    *   La instancia de `PrismaClient` debe inicializarse como singleton en `src/config/prisma.ts`.
    *   **REGLA DE ORO:** Los Controladores HTTP **JAMÁS** deben importar `PrismaClient`. Solo los Repositorios acceden a Prisma. Los Servicios llaman a los Repositorios.

2.  **Uso de Transacciones (`$transaction`):**
    *   Utilizar `$transaction` cuando una operación involucre múltiples escrituras dependientes.
    *   Ejemplo: Al autorizar un mantenimiento correctivo, se cambia el estado del `Mantenimiento` a ACTIVO y simultáneamente se actualiza el estado de la `Unidad` a EN_TALLER.

## Migraciones y Entornos

1.  **Creación de Migraciones:**
    *   Al modificar `schema.prisma`, generar la migración con un nombre claro y descriptivo en español:
        `npx prisma migrate dev --name agregar-tabla-telemetria`
    *   No modificar migraciones ya aplicadas. Si hay error, crear una nueva que corrija el anterior.

2.  **Seeds (Datos Iniciales):**
    *   El archivo `prisma/seed.ts` debe contener los registros básicos para inicializar el sistema (Roles predefinidos, un Usuario Administrador).
    *   Ejecutar con `npx prisma db seed`.

## Agnosticismo de Motor (Futuras Migraciones)
*   Prisma abstrae la capa relacional. Para preparar el sistema ante un eventual cambio de motor (ej. a MongoDB o MySQL), asegurar que toda consulta de persistencia viva encapsulada dentro de la carpeta `src/modulos/<modulo>/infraestructura/repositorios/`.
*   El resto del código (Casos de Uso) debe depender de Interfaces de Repositorio ubicadas en `src/modulos/<modulo>/dominio/repositorios/`.
