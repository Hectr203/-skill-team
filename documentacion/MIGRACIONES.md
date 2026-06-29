# Guía de Migraciones y Seeders — VTP Transporte Backend

Este documento explica cómo funciona el sistema de migraciones de la base de datos y qué comando debes usar según tu situación. Léelo completo antes de tocar la base de datos en cualquier ambiente.

---

## ¿Qué es una migración y para qué sirve?

Una **migración** es un archivo `.sql` que define la estructura de una tabla (columnas, índices, claves foráneas). Los **seeders** son archivos `.sql` que insertan datos iniciales necesarios para que la app funcione (catálogos, roles, etc.).

En lugar de correr SQL a mano cada vez que hay un cambio, estos scripts se encargan de aplicar solo lo que falta, de forma ordenada y sin romper lo que ya existe.

---

## Archivos y carpetas relevantes

```
vtp-transporte-backend-main/
├── scripts/
│   ├── migrate-safe.js             ← Script principal (uso diario)
│   ├── migrate-register-existing.js ← Script de arranque único
│   └── migrate-local.js            ← Solo para desarrollo local (BORRA TODO)
├── src/
│   └── infra/
│       └── db/
│           ├── migrations/         ← Archivos .sql de estructura de tablas
│           └── seeders/            ← Archivos .sql con datos iniciales
└── package.json                    ← Comandos npm disponibles
```

La tabla `_migrations_log` en la base de datos es la que lleva el registro de qué archivos ya se ejecutaron. **Nunca la borres manualmente.**

---

## Variables de entorno requeridas

Antes de correr cualquier comando, asegúrate de tener el archivo `.env` en la raíz del backend con estas variables:

```env
DB_HOST=<host del servidor MySQL>
DB_PORT=3306
DB_USER=<usuario>
DB_PASSWORD=<contraseña>
DB_NAME=vtptransporte
DB_SSL=true   # "true" si es Azure, "false" si es local
```

---

## Comandos disponibles (`npm run ...`)

### `db:migrate-safe` — ✅ El que usarás el 99% del tiempo

```bash
npm run db:migrate-safe
```

**¿Qué hace?**
- Conecta a MySQL usando el `.env`
- Crea la base de datos si no existe (sin borrar nada)
- Crea la tabla `_migrations_log` si no existe
- Detecta qué migraciones y seeders aún no se han aplicado
- Aplica **solo los pendientes**, en el orden correcto
- Registra cada archivo ejecutado para no volver a correrlo

**¿Cuándo usarlo?**
- Después de hacer `git pull` y hay migraciones nuevas
- Al desplegar a staging o producción
- Cada vez que un compañero agregó una migración nueva

---

### `db:migrate-safe:only-migrate` — Solo estructura de tablas

```bash
npm run db:migrate-safe:only-migrate
```

**¿Qué hace?**
Igual que `db:migrate-safe` pero **omite los seeders**. Solo aplica cambios de estructura (CREATE TABLE, ALTER TABLE, etc.).

**¿Cuándo usarlo?**
- Cuando solo hay migraciones nuevas y los seeders ya están correctos
- En ambientes donde los datos ya existen y no quieres correr inserts innecesarios

---

### `db:migrate-safe:only-seed` — Solo datos iniciales

```bash
npm run db:migrate-safe:only-seed
```

**¿Qué hace?**
Igual que `db:migrate-safe` pero **omite las migraciones** de estructura. Solo corre los seeders pendientes.

**¿Cuándo usarlo?**
- Cuando se agregó un nuevo catálogo o dato inicial sin cambiar ninguna tabla

---

### `db:migrate-safe:dry-run` — Vista previa sin ejecutar nada

```bash
npm run db:migrate-safe:dry-run
```

**¿Qué hace?**
Lee la base de datos y muestra en consola **qué archivos correría**, pero **no ejecuta ningún SQL**. La base de datos queda intacta.

**¿Cuándo usarlo?**
- Antes de aplicar migraciones en producción para verificar qué va a cambiar
- Para revisar el estado actual sin riesgo

---

### `db:register-existing` — ⚠️ Solo para primera configuración

```bash
npm run db:register-existing
```

**¿Qué hace?**
Este script es para cuando ya tienes una base de datos con tablas y datos **pero sin la tabla `_migrations_log`** (es decir, la primera vez que alguien en el equipo usa este sistema de migraciones sobre una BD ya existente).

Lo que hace por cada archivo `.sql`:
1. Intenta ejecutarlo
2. Si falla porque la tabla/columna ya existe → lo marca como ya ejecutado sin error
3. Si pasa sin error → lo ejecuta y lo registra
4. Si falla por otro motivo → te lo reporta para revisión manual

**¿Cuándo usarlo?**
- **Una sola vez**, cuando un ambiente ya tiene tablas creadas manualmente y quieres empezar a usar `db:migrate-safe`
- Después de correrlo, usa `db:migrate-safe` de ahí en adelante normalmente

> ⚠️ **IMPORTANTE:** No uses este comando si ya tienes `_migrations_log`. Solo sirve para el "arranque inicial" del sistema de migraciones.

---

### `db:migrate:reset` — 🔴 Solo para desarrollo local

```bash
npm run db:migrate:reset
```

**¿Qué hace?**
Borra y recrea la base de datos desde cero. **Elimina todos los datos.**

**¿Cuándo usarlo?**
- **Solo en tu máquina local** cuando quieres un ambiente limpio
- **NUNCA en staging ni producción**

---

## Tabla de decisión rápida

| Situación | Comando a usar |
|---|---|
| Hay migraciones nuevas después de un pull | `db:migrate-safe` |
| Quiero ver qué va a cambiar sin aplicar nada | `db:migrate-safe:dry-run` |
| Solo hay cambios de estructura (no seeders) | `db:migrate-safe:only-migrate` |
| Solo hay seeders nuevos (no estructura) | `db:migrate-safe:only-seed` |
| Primera vez que uso este sistema en una BD existente | `db:register-existing` (una sola vez) |
| Quiero resetear mi BD local desde cero | `db:migrate:reset` (solo local) |

---

## Flujo típico de un desarrollador

### Caso 1: Llegué por la mañana, hice `git pull` y hay migraciones nuevas

```bash
# 1. Actualiza tu código
git pull

# 2. Aplica lo que falta
npm run db:migrate-safe
```

Listo. La salida en consola te dirá qué archivos se aplicaron.

### Caso 2: Voy a desplegar a producción

```bash
# 1. Primero revisa qué va a cambiar (sin ejecutar nada)
npm run db:migrate-safe:dry-run

# 2. Si todo se ve bien, aplica las migraciones
npm run db:migrate-safe
```

### Caso 3: Soy nuevo en el equipo, tengo la BD vacía

```bash
# Aplica todo desde cero (crea BD, tablas y datos iniciales)
npm run db:migrate-safe
```

### Caso 4: Tengo una BD con datos pero nunca usé este sistema

```bash
# Solo la primera vez, registra lo que ya existe
npm run db:register-existing

# De ahí en adelante, usa el comando normal
npm run db:migrate-safe
```

---

## ¿Cómo agrego una migración nueva?

1. Crea un archivo `.sql` en `src/infra/db/migrations/` con el nombre en formato `NNN_descripcion.sql` (ej. `023_create_payment_records.sql`)
2. Si necesita un orden específico respecto a otras tablas, agrégalo a la lista `PRIORITY_MIGRATIONS` en `scripts/migrate-safe.js`
3. Haz commit del archivo `.sql` junto con tu código
4. Cuando los demás hagan `git pull` y corran `npm run db:migrate-safe`, se aplicará automáticamente

---

## Errores comunes

### `ER_ACCESS_DENIED_ERROR`
Las credenciales del `.env` están mal. Revisa `DB_USER` y `DB_PASSWORD`.

### `ECONNREFUSED`
MySQL no está corriendo o `DB_HOST`/`DB_PORT` son incorrectos.

### `Error en NNN_archivo.sql: ...` (el proceso se detiene)
Hay un error en ese SQL. El script se detiene para que no quede la BD en estado inconsistente. Corrígelo y vuelve a correr `db:migrate-safe`; los archivos que ya pasaron no se vuelven a ejecutar.

### Un seeder falla pero el proceso continúa
Los errores en seeders **no son fatales**. El script te avisa pero sigue con los demás. Revisa el seeder manualmente si necesitas esos datos.
