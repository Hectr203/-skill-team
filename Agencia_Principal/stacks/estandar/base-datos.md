# Stack Estándar: Base de Datos (PostgreSQL + Prisma ORM)

Este documento define las especificaciones técnicas obligatorias para el diseño, persistencia y migración de datos bajo el stack oficial predeterminado.

---

## 1. Motor y Herramientas

- **Motor Principal:** PostgreSQL 16+
- **ORM Oficial:** Prisma ORM
- **Herramientas de Migración:** Prisma Migrate (`npx prisma migrate dev`, `npx prisma migrate deploy`)
- **Prohibiciones:** Quedan estrictamente prohibidos SQL Server, Knex o inyecciones de SQL crudo sin justificación técnica aprobada en un ADR.

---

## 2. Convenciones de Modelado (`schema.prisma`)

1. **Modelos y Campos en Español**:
   - Nombres de modelos en singular y PascalCase (`Usuario`, `Cliente`, `Proyecto`, `Factura`).
   - Nombres de campos en camelCase (`nombreCompleto`, `correoElectronico`, `fechaCreacion`).
   - Mapeo a base de datos con `@@map("usuarios")` y `@map("correo_electronico")` si se requiere snake_case a nivel físico.

2. **Ejemplo de Esquema Estándar**:
```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

enum RolUsuario {
  ADMINISTRADOR
  OPERADOR
  CLIENTE
}

model Usuario {
  id               String       @id @default(uuid())
  nombreCompleto   String       @map("nombre_completo")
  correo           String       @unique
  contrasenaHash   String       @map("contrasena_hash")
  rol              RolUsuario   @default(OPERADOR)
  activo           Boolean      @default(true)
  creadoEn         DateTime     @default(now()) @map("creado_en")
  actualizadoEn    DateTime     @updatedAt @map("actualizado_en")

  proyectos        Proyecto[]

  @@map("usuarios")
}

model Proyecto {
  id               String       @id @default(uuid())
  nombre           String
  descripcion      String?
  estado           String       @default("ACTIVO")
  creadoEn         DateTime     @default(now()) @map("creado_en")
  actualizadoEn    DateTime     @updatedAt @map("actualizado_en")

  usuarioId        String       @map("usuario_id")
  usuario          Usuario      @relation(fields: [usuarioId], references: [id])

  @@map("proyectos")
}
```

---

## 3. Reglas de Migración y Semillas (Seeds)
1. **Migraciones Aditivas**: Nunca ejecutar `DROP TABLE` ni `DROP COLUMN` directamente en producción. Las migraciones deben ser retrocompatibles en dos fases.
2. **Semillas Reutilizables (`seed.ts`)**: Todo proyecto debe incluir datos iniciales controlados para arranque de desarrollo y pruebas locales.
