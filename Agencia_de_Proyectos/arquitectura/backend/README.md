# Arquitectura del Backend: Clean Architecture Modular por Dominio

Esta guía establece el estándar arquitectónico para el desarrollo de servicios y APIs backend dentro de la Agencia de Proyectos. Implementa una **Clean Architecture modular por dominio** adaptada a **Node.js**, **TypeScript**, **Express**, **Prisma ORM** y **PostgreSQL**, garantizando alta cohesión, desacoplamiento, mantenibilidad y testabilidad sin sobreingeniería (criterio Ponytail).

---

## 1. Carácter de Arquetipo Ilustrativo y Adaptabilidad Universal

> [!IMPORTANT]
> **Arquetipo de referencia, no un dominio impuesto**:
> Las carpetas y nombres de dominios mostrados como ejemplo (tales como `almacenes`, `auditoria`, `inventario`, etc.) constituyen **únicamente un caso de estudio ilustrativo y pedagógico**. **NO representan un proyecto final real ni limitan a la agencia a crear sistemas administrativos o ERPs.**
>
> Ante cada nuevo proyecto, la agencia analizará los requerimientos específicos del usuario (fintech, e-commerce, telemedicina, streaming, SaaS, educación, etc.), deduciendo y modelando sus **propios dominios de negocio en español** (ej. en salud: `pacientes`, `citas`, `historiales`; en e-commerce: `catalogo`, `carrito`, `pagos`, `envios`).

---

## 2. Convención de Idioma y Nomenclatura

* **Carpetas Estructurales y Técnicas en INGLÉS**:
  `src`, `config`, `modules`, `controllers`, `services`, `repositories`, `routes`, `dto`, `middlewares`, `utils`, `shared`, `auth`, `errors`.
* **Dominios de Negocio y Submódulos SIEMPRE en ESPAÑOL**:
  Toda carpeta funcional que represente un módulo de negocio o entidad se nombra en español adaptado al giro del software:
  - En Logística / ERP (ejemplo): `administracion`, `almacen`, `auth`, `compras`, `pedido`.
  - En E-Commerce: `catalogo`, `carrito`, `pagos`, `envios`, `clientes`.
  - En Educación: `cursos`, `estudiantes`, `evaluaciones`, `certificados`.
* **Frontera Limpia**: Las convenciones técnicas siguen el estándar global (`service`, `controller`, `dto`, `repository`), mientras que el dominio refleja con precisión el lenguaje del negocio en español.

---

## 3. Arquetipo Canónico Universal

```text
backend/src/
├── config/                                  # Configuración global y validación estricta de entorno (.env con Zod)
│   └── env.ts                               # Esquema Zod de variables requeridas para arrancar el servidor
├── modules/                                 # MÓDULOS DE DOMINIO DE NEGOCIO (Descubiertos por proyecto)
│   └── <modulo-del-negocio>/                # Carpeta en español del dominio (ej. ventas, pacientes, inventario)
│       ├── <submodulo>/                     # Subdominio específico o entidad
│       │   ├── <submodulo>.controller.ts    # Capa de entrada HTTP (recibe req, valida, llama servicio, responde res)
│       │   ├── <submodulo>.dto.ts           # Esquemas de validación de entrada (Zod) y tipos inferidos
│       │   ├── <submodulo>.routes.ts        # Enrutador Express con middlewares de autenticación y validación
│       │   ├── <submodulo>.service.ts       # Casos de uso y reglas de negocio del dominio (independiente de HTTP)
│       │   └── <submodulo>.repository.ts    # Persistencia / consultas Prisma (cuando la lógica de datos lo amerita)
│       ├── <modulo>.middleware.ts           # Middlewares específicos de este módulo
│       └── <modulo>.routes.ts               # Enrutador agrupador del módulo
├── shared/                                  # CAPACIDADES Y SERVICIOS TRANSVERSALES
│   ├── auth/                                # Control de acceso, guardias RBAC y catálogo de permisos
│   │   ├── permission.service.ts            # Verificación de permisos de usuario
│   │   └── permissions.catalog.ts           # Catálogo centralizado de permisos del sistema
│   ├── errors/                              # Jerarquía de excepciones y manejador global de errores
│   │   ├── ApiError.ts                      # Clase base para errores HTTP controlados (400, 401, 403, 404, 500)
│   │   └── errorHandler.middleware.ts       # Middleware centralizado de captura de errores Express
│   ├── middlewares/                         # Middlewares globales
│   │   ├── auth.middleware.ts               # Validación de JWT y extracción del payload de usuario
│   │   ├── validate.middleware.ts           # Middleware genérico de validación Zod (body, query, params)
│   │   └── cors.middleware.ts               # Configuración estricta de orígenes permitidos
│   └── utils/                               # Utilidades transversales
│       ├── crypto.ts                        # Hashing (bcrypt/argon2) y firma de tokens JWT
│       ├── prisma.ts                        # Conexión e instancia compartida del cliente Prisma ORM
│       ├── response.helper.ts               # Formato de respuesta JSON estandarizado
│       └── time.ts                          # Manejador de fechas y zonas horarias
├── app.ts                                   # Creación de Express, middlewares globales y montaje de rutas modulares
└── server.ts                                # Arranque del servidor HTTP y listeners de procesos
```

---

## 4. Estándares de Clean Architecture y Responsabilidades por Capa

### A. Controladores (`*.controller.ts`)
- **Responsabilidad**: Capa de entrega HTTP delgada. Reciben la petición (`req`), extraen los datos validados del DTO, delegan la ejecución en el servicio correspondiente y devuelven respuestas uniformes mediante `response.helper.ts`.
- **Prohibición**: Queda terminantemente prohibido ejecutar consultas directas a base de datos (`prisma.findMany`) o albergar lógica de negocio dentro del controlador.

### B. Validación de Entradas (`*.dto.ts` con Zod)
- Cada endpoint valida estrictamente su entrada (body, query, params) antes de ejecutar la lógica:
```typescript
import { z } from 'zod';

export const CrearAlmacenSchema = z.object({
  nombre: z.string().min(3, 'El nombre debe tener al menos 3 caracteres'),
  codigo: z.string().regex(/^[A-Z0-9_-]+$/, 'Código alfanumérico inválido'),
  capacidadM2: z.number().positive('La capacidad debe ser positiva'),
  esPrincipal: z.boolean().default(false),
});

export type CrearAlmacenDto = z.infer<typeof CrearAlmacenSchema>;
```

### C. Servicios de Dominio (`*.service.ts`)
- **Responsabilidad**: Contienen los casos de uso y las reglas de negocio del dominio. Coordinan transacciones, validan estados operacionales y devuelven entidades limpias.
- **Independencia Total**: No dependen de objetos `req` ni `res` de Express. Esto permite probarlos unitariamente sin necesidad de levantar un servidor HTTP ni simular contextos web.

### D. Repositorios (`*.repository.ts`) y Criterio Ponytail
- **Responsabilidad**: Abstracción de persistencia y consultas complejas a base de datos mediante Prisma ORM.
- **Criterio Ponytail**: Para operaciones CRUD simples y directas, el servicio puede interactuar directamente con `prisma` si un repositorio solo actuaría como un pasamanos sin valor añadido. El archivo `*.repository.ts` se introduce cuando la consulta involucra múltiples joins, agregaciones o lógica de datos compleja.

### E. Transacciones Atómicas
- Toda operación de negocio que involucre múltiples mutaciones en base de datos (ej. crear un traspaso y actualizar el stock de dos almacenes) debe ejecutarse obligatoriamente bajo `prisma.$transaction`:
```typescript
await prisma.$transaction(async (tx) => {
  await tx.almacenStock.decrement({ ... });
  await tx.almacenStock.increment({ ... });
  await tx.traspasoRegistro.create({ ... });
});
```

### F. Formato Estandarizado de Respuestas API (`response.helper.ts`)
Toda respuesta de la API seguirá un contrato predecible para el cliente frontend:
```json
{
  "success": true,
  "data": {},
  "message": "Operación completada exitosamente",
  "meta": { "total": 100, "page": 1, "limit": 10 }
}
```
En caso de error controlado (`ApiError`):
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Datos de entrada inválidos",
    "details": []
  }
}
```

### G. Control de Acceso Basado en Roles (RBAC)
- Las rutas del submódulo asocian guardias de autenticación (`auth.middleware.ts`) y validación de permisos específicos (`permission.service.ts`) contra el catálogo centralizado (`permissions.catalog.ts`):
```typescript
router.post(
  '/',
  authMiddleware,
  checkPermission('almacen:crear'),
  validateBody(CrearAlmacenSchema),
  almacenController.crear
);
```

---

## 5. Principio Ponytail en Backend: Cero Sobreingeniería
* No forzar patrones de fábrica, interfaces genéricas vacías o inyección de dependencias compleja en módulos sencillos.
* Cada submódulo comienza con la estructura mínima que funciona: `controller`, `dto`, `service` y `routes`.
* El código debe ser directo, altamente legible y fuertemente tipado con TypeScript estricto.
