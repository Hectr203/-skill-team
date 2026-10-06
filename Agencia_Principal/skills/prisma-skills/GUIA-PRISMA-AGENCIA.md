# Guía de Uso de Prisma Skills en Agencia Principal

Esta suite curada reúne las habilidades y referencias técnicas oficiales de **Prisma ORM** ([prisma/skills](https://github.com/prisma/skills.git)), adaptadas para trabajar en sinergia con nuestro stack obligatorio: **Node.js 22 LTS, Express.js, TypeScript, PostgreSQL y Prisma**, bajo la arquitectura modular por dominio de la Agencia.

---

## 1. Sinergia con las Convenciones de la Agencia

| Nuestra Convención ([prisma-base-de-datos](../prisma-base-de-datos/SKILL.md)) | Qué aporta Prisma Skills ([prisma-skills](README.md)) |
| :--- | :--- |
| **Modelado en Español:** `Usuario`, `Ruta`, `cuid()`, `creadoEn`. | **API exacta del Cliente:** Tipos de queries, filtros, operadores y `select`/`include`. |
| **Aislamiento:** Prisma vive **únicamente** en `*.repository.ts`. | **Seguridad en Transacciones:** Fórmulas correctas para `$transaction` interactivo sin fugas de conexiones. |
| **PostgreSQL mandatorio:** Prohibidos SQL Server, Knex y MongoDB. | **Driver Adapters modernos:** Implementación de `@prisma/adapter-pg` para Node.js 22 LTS. |
| **Human-in-the-Loop:** Aprobación antes de comandos destructivos. | **Agent Safety:** Bloqueo automatizado de `migrate reset` o `db push --force-reset`. |

---

## 2. Catálogo de Habilidades Instaladas (7 Skills)

| Habilidad | Carpeta | Propósito Principal |
| :--- | :--- | :--- |
| **Prisma Client API** | [prisma-client-api](skills/prisma-client-api/SKILL.md) | Referencia exhaustiva de queries, CRUD, filtros escalares/lógicos, relaciones anidadas y `createManyAndReturn()`. |
| **Prisma CLI** | [prisma-cli](skills/prisma-cli/SKILL.md) | Comandos del CLI: `prisma migrate dev`, `prisma migrate deploy`, `prisma db seed`, `prisma studio`, `prisma validate`. |
| **Prisma ORM Setup** | [prisma-orm-setup](skills/prisma-orm-setup/SKILL.md) | Inicialización estructurada del ORM y diagnóstico de conexión con PostgreSQL. |
| **Driver Adapter** | [prisma-driver-adapter-implementation](skills/prisma-driver-adapter-implementation/SKILL.md) | Configuración del adaptador SQL `@prisma/adapter-pg` con pool de conexiones en Node 22. |
| **Database Setup** | [prisma-database-setup](skills/prisma-database-setup/SKILL.md) | Configuración de cadenas de conexión y variables de entorno para PostgreSQL. |
| **Prisma Postgres** | [prisma-postgres](skills/prisma-postgres/SKILL.md) | Conectividad y optimizaciones específicas para motores PostgreSQL. |
| **Upgrade v7** | [prisma-upgrade-v7](skills/prisma-upgrade-v7/SKILL.md) | Guía técnica para migraciones entre versiones mayores sin regresiones. |

---

## 3. Patrón de Repositorio Limpio con Prisma Client API

Dentro de `backend/src/modules/<modulo>/<modulo>.repository.ts`, aplicamos las reglas de [prisma-client-api](skills/prisma-client-api/SKILL.md):

```typescript
// backend/src/modules/almacen/almacen.repository.ts
import { prisma } from '../../config/prisma';
import { CrearItemAlmacenDTO, FiltrosAlmacenDTO } from './almacen.dto';
import { ItemAlmacen } from './almacen.types';

export class AlmacenRepository {
  // 1. Búsqueda con filtros tipados y paginación
  async buscarConFiltros(filtros: FiltrosAlmacenDTO): Promise<ItemAlmacen[]> {
    return prisma.itemAlmacen.findMany({
      where: {
        eliminadoEn: null, // Borrado lógico
        ...(filtros.terminoBusqueda && {
          nombre: {
            contains: filtros.terminoBusqueda,
            mode: 'insensitive', // Búsqueda insensible a mayúsculas/minúsculas
          },
        }),
      },
      select: {
        id: true,
        codigoSku: true,
        nombre: true,
        stockActual: true,
        creadoEn: true,
      },
      orderBy: { creadoEn: 'desc' },
      skip: filtros.desplazamiento ?? 0,
      take: filtros.limite ?? 20,
    });
  }

  // 2. Operación transaccional compuesta segura
  async registrarEntradaStock(itemId: string, cantidad: number, motivo: string) {
    return prisma.$transaction(async (tx) => {
      // Registrar movimiento
      const movimiento = await tx.movimientoAlmacen.create({
        data: {
          itemId,
          cantidad,
          motivo,
          tipo: 'ENTRADA',
        },
      });

      // Actualizar stock atómicamente
      const itemActualizado = await tx.itemAlmacen.update({
        where: { id: itemId },
        data: {
          stockActual: { increment: cantidad },
        },
      });

      return { movimiento, itemActualizado };
    });
  }
}
```

---

## 4. Protocolo de Seguridad para Comandos del CLI (*Agent Safety*)

Como establece [agent-safety.md](skills/prisma-cli/references/agent-safety.md), los siguientes comandos son **destructivos** y requieren consentimiento explícito del humano antes de ejecutarse:

- `prisma migrate reset` (borra la base de datos por completo y reaplica migraciones).
- `prisma db push --force-reset` (destruye esquemas de tablas).
- `prisma db push --accept-data-loss` (borra columnas con datos).

### Flujo Autorizado en la Agencia:
1. **Desarrollo local:** Usar siempre `npx prisma migrate dev --name <nombre_migracion_en_espanol>`.
2. **Entornos de producción / staging:** Usar `npx prisma migrate deploy`.
3. **Poblado inicial:** Usar `npx prisma db seed`.
4. **Verificación visual:** Usar `npx prisma studio`.

---

## 5. Integración con los Agentes

- **[agente-backend.md](../../agentes/agente-backend.md):** 
  Utiliza [prisma-client-api](skills/prisma-client-api/SKILL.md) para construir queries en repositorios y [prisma-cli](skills/prisma-cli/SKILL.md) para ejecutar migraciones y validaciones.
- **[prisma-base-de-datos](../prisma-base-de-datos/SKILL.md):** 
  Establece los modelos `Usuario`, `cuid()` y la arquitectura por capas, delegando la sintaxis del cliente a esta suite.
