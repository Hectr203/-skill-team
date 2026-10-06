# Guía de Clean Architecture por Dominio en Backend

Esta guía establece cómo aplicar los principios de **Clean Architecture** (Robert C. Martin) y **Diseño Simple** (Kent Beck) integrados a la perfección con la arquitectura **Modular por Dominio** de la Agencia Principal.

---

## 1. El Principio de Armonía: Clean Architecture por Dominio

Muchos tutoriales de Clean Architecture organizan carpetas de forma puramente técnica global (`src/entities/`, `src/usecases/`, `src/controllers/`), lo cual dispersa la lógica de un mismo negocio en múltiples carpetas lejanas.

En la Agencia Principal combinamos lo mejor de ambos mundos: **Empaquetado por Componente/Dominio (*Packaging by Feature/Domain*)** manteniendo la **separación estricta de capas hacia adentro**.

### Estructura de un Módulo de Dominio (`backend/src/modules/<modulo>/`)

```txt
backend/src/modules/almacen/
├── almacen.routes.ts       # Capa 4: Frameworks & Drivers (Express Router)
├── almacen.controller.ts   # Capa 3: Interface Adapters (Controlador HTTP)
├── almacen.service.ts      # Capa 2: Use Cases / Casos de Uso (Lógica de Aplicación)
├── almacen.repository.ts   # Capa 3/4: Acceso a Datos y Persistencia (Prisma ORM)
├── almacen.dto.ts          # Cruce de Fronteras: DTOs de Entrada y Salida
├── almacen.schema.ts       # Validación en Frontera: Esquemas Zod / Joi
└── almacen.types.ts        # Capa 1: Entidades de Dominio e Interfaces
```

---

## 2. Correspondencia con las Capas de Clean Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ Frameworks & Drivers: almacen.routes.ts, prisma.ts              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Interface Adapters: almacen.controller.ts, repository.ts │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │ Use Cases: almacen.service.ts                   │    │    │
│  │  │  ┌─────────────────────────────────────────┐    │    │    │
│  │  │  │ Entities / Dominio: almacen.types.ts     │    │    │    │
│  │  │  └─────────────────────────────────────────┘    │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                    ← Las dependencias siempre apuntan hacia adentro
```

1. **Entidades / Dominio (`almacen.types.ts`):**
   - Tipos de datos puros de TypeScript que representan los conceptos de negocio.
   - **Regla sagrada:** Prohibido importar Express, Prisma, Axios o dependencias externas en este archivo.

2. **Casos de Uso / Servicio (`almacen.service.ts`):**
   - Orquesta la lógica del negocio (ej. `crearEntradaAlmacen`, `ajustarStock`).
   - No sabe qué es HTTP, no recibe `req` ni `res`, no envía códigos de estado (200, 404).
   - Recibe DTOs tipados y devuelve DTOs tipados o tipos de dominio.
   - Depende de la interfaz abstracta del repositorio (`IAlmacenRepository`), permitiendo pruebas unitarias instantáneas con mocks en memoria.

3. **Adaptadores de Interfaz (`almacen.controller.ts`, `almacen.repository.ts`):**
   - **Controlador:** Extrae parámetros de la petición HTTP (`req.body`, `req.params`), los valida contra `almacen.schema.ts`, llama al servicio y formatea la respuesta HTTP (`res.status(201).json(...)`).
   - **Repositorio:** Implementa `IAlmacenRepository`. Es el **único lugar** donde se escribe `prisma.almacen.findMany(...)` o `$transaction`.

4. **Frameworks y Drivers (`almacen.routes.ts`):**
   - Define los endpoints de Express (`router.post('/', controller.crear)`), aplica middlewares de autenticación/autorización y vincula la ruta con el método del controlador.

---

## 3. Flujo Obligatorio de una Petición

Toda petición HTTP en el backend de la agencia debe seguir esta secuencia sin saltarse capas:

```txt
HTTP Request
     ↓
Ruta (almacen.routes.ts)
     ↓ [aplica middlewares de auth y validación]
Controlador (almacen.controller.ts)
     ↓ [pasa DTO validado]
Servicio (almacen.service.ts)
     ↓ [ejecuta reglas de negocio y llama interfaz de repositorio]
Repositorio (almacen.repository.ts)
     ↓ [ejecuta queries tipadas]
Prisma ORM
     ↓
PostgreSQL
```

---

## 4. Cruce de Fronteras con DTOs (*Data Transfer Objects*)

**Principio:** Los modelos crudos de base de datos nunca deben salir directamente al frontend sin transformación.

```typescript
// almacen.dto.ts
export interface CrearItemAlmacenDTO {
  codigoSku: string;
  nombre: string;
  cantidadInicial: number;
  ubicacionId: string;
}

export interface ItemAlmacenRespuestaDTO {
  id: string;
  codigoSku: string;
  nombre: string;
  stockActual: number;
  creadoEn: string;
}
```

---

## 5. Principios de Kent Beck (Diseño Simple y Detección de Code Smells)

El skill [kent-beck-style](skills/kent-beck-style/SKILL.md) aporta las cuatro reglas de diseño simple para evitar sobre-ingeniería:

1. **Pasa las pruebas (*Passes the Tests*):** Cada caso de uso debe tener pruebas unitarias que validen sus reglas de negocio.
2. **Revela la intención (*Reveals Intent*):** Los nombres de métodos y variables deben describir claramente qué hacen en el contexto de negocio (ej. `verificarStockDisponible()` en lugar de `check()`).
3. **Cero duplicación (*No Duplication / DRY*):** Validaciones repetidas o cálculos de impuestos compartidos deben vivir en funciones puras reutilizables en `shared/`.
4. **Mínimo número de elementos (*Fewest Elements / YAGNI / KISS*):**
   - No crear interfaces o fábricas si solo existe una implementación real y no aporta valor inmediato.
   - No crear abstracciones especulativas para requisitos que aún no existen.

### Code Smells Comunes a Eliminar en el Backend:
- **Controlador Gordo (*Fat Controller*):** Si el controlador tiene más de 15 líneas por método o realiza cálculos, esa lógica pertenece al Servicio.
- **Fuga de Prisma en el Controlador:** Si `prisma` se importa en un archivo `.controller.ts` o `.service.ts`, es una violación de Clean Architecture; debe moverse a `.repository.ts`.
- **Acoplamiento a HTTP en el Servicio:** Si un servicio recibe `req` o `res`, el servicio no es testeable de forma aislada.
