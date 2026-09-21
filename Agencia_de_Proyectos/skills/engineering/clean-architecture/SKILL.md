---
name: clean-architecture
description: Directivas de Clean Architecture modular para servicios Node.js, Express, TypeScript y Prisma. Separa casos de uso de controladores HTTP, aplicando esquemas Zod y filosofía Ponytail.
---

# Clean Architecture Modular en Node.js y Express

Esta skill proporciona las reglas prácticas y operativas para implementar Clean Architecture en los servicios backend de la Agencia de Proyectos.

---

## 1. Regla de Dependencias Inward (Hacia Adentro)

Las capas internas definen las reglas del negocio y nunca dependen de los detalles de infraestructura:

```text
Controlador HTTP (Express) ──> Esquema DTO (Zod) ──> Servicio de Negocio ──> Entidad / Prisma
       ▲                                                     │
       └────────────── Middleware Global (Auth/Error) ───────┘
```

- **El Servicio de Dominio (`*.service.ts`)**:
  - No recibe ni manipula `req`, `res`, ni `next`.
  - Recibe parámetros tipados extraídos del DTO y devuelve promesas con los datos puros.
  - Lanza excepciones de tipo `ApiError` (ej. `ApiError.notFound('Almacén no encontrado')`).
- **El Controlador (`*.controller.ts`)**:
  - Encargado exclusivamente del transporte HTTP: parsea cookies, headers, params y delega al servicio.
  - Responde con `res.status(code).json(responseHelper(...))`.

---

## 2. Validación en Límites de Confianza con Zod

Toda entrada exterior (body, query, headers o params) debe cruzar un validador Zod antes de ingresar a la lógica del servicio:

```typescript
// middlewares/validate.middleware.ts
export const validateBody = (schema: z.ZodSchema) => {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      throw ApiError.badRequest('Error de validación', result.error.errors);
    }
    req.body = result.data;
    next();
  };
};
```

---

## 3. Criterio de Persistencia y Filosofía Ponytail

- **Para CRUDs directos**: El servicio puede interactuar directamente con `prisma.<modelo>` mediante consultas claras y tipadas.
- **Para consultas complejas**: Si una operación involucra agregaciones pesadas, lógica SQL cruda (`$queryRaw`) o transacciones multicapa, encapsularla en un archivo `*.repository.ts`.
- **Transacciones**: Emplear siempre `prisma.$transaction` para garantizar que mutaciones interdependientes sean atómicas.
