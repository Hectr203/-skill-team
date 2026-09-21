# Arquitectura General: Monorepo Dividido

Todos los proyectos de software construidos por la Agencia de Proyectos se estructuran obligatoriamente bajo un esquema de **Monorepo dividido**, asegurando aislamiento total entre las capas de frontend y backend, independencia de dependencias y una experiencia de desarrollo (DX) de primer nivel.

---

## 1. Estructura General del Monorepo Dividido

```text
mi-proyecto/
├── frontend/                                # Aplicación de interfaz de usuario (React / TypeScript / Vite)
│   ├── src/
│   │   ├── modules/                         # Módulos de dominio de negocio en español
│   │   ├── shared/                          # Atomic Design System global, hooks, utilidades
│   │   ├── config/                          # Variables de entorno validadas con Zod
│   │   └── ...
│   ├── package.json                         # Dependencias exclusivas del frontend
│   └── tsconfig.json                        # Path aliases (@modules/*, @shared/*)
├── backend/                                 # Servicio de lógica de negocio y APIs (Node.js / Express / TypeScript)
│   ├── src/
│   │   ├── modules/                         # Clean Architecture modular por dominio en español
│   │   ├── shared/                          # Middlewares, auth RBAC, errores, helpers
│   │   ├── config/                          # Validación de variables (.env) en boot time con Zod
│   │   └── app.ts                           # Montaje de rutas y middlewares
│   ├── prisma/                              # Esquema y migraciones de base de datos PostgreSQL
│   ├── package.json                         # Dependencias exclusivas del backend
│   └── tsconfig.json                        # Path aliases (@modules/*, @shared/*)
├── .agents/                                 # Configuración y skills locales para agentes de IA
├── docs/                                    # Documentación técnica, memoria y registros ADR
├── package.json                             # Configuración raíz del monorepo (workspaces) y scripts globales
└── README.md
```

---

## 2. Prohibición de Arquitecturas Monolíticas Acopladas

* **Cero Monolitos Mezclados**: Queda estrictamente prohibido utilizar arquitecturas tradicionales acopladas (como Laravel clásico, Django tradicional o Ruby on Rails donde plantillas de vista, controladores y base de datos conviven en la misma jerarquía).
* **Independencia de Dependencias**: `frontend/` y `backend/` mantienen sus propios archivos `package.json` aislados. Una actualización de paquetes en el frontend jamás debe afectar al backend.
* **Separación Física de Responsabilidades**: Ningún archivo de interfaz gráfica (JSX/TSX, CSS) debe residir dentro de `backend/`, ni modelos de Prisma, consultas SQL o controladores de servidor deben ubicarse dentro de `frontend/`.
* **Comunicación Desacoplada**: El frontend interactúa con el backend exclusivamente mediante APIs REST o GraphQL fuertemente tipadas.

---

## 3. Estándares de Ingeniería del Monorepo

1. **Path Aliases Estandarizados**:
   Tanto en `frontend/tsconfig.json` como en `backend/tsconfig.json` se configuran alias absolutos para evitar rutas relativas frágiles (`../../../../`):
   - `@modules/*` -> `src/modules/*`
   - `@shared/*` -> `src/shared/*`
2. **Validación de Entorno (`.env`) en Boot Time**:
   Tanto el frontend como el backend validan sus variables de entorno al iniciar mediante esquemas estrictos de Zod (`src/config/env.ts`), impidiendo que la aplicación arranque en un estado inconsistente o mal configurado.
3. **Orquestación de Scripts en la Raíz**:
   El `package.json` raíz gestiona los workspaces (`pnpm` o `npm`) y expone comandos concurrentes unificados:
   - `npm run dev`: Inicia frontend y backend simultáneamente en terminales concurrentes.
   - `npm run build`: Compila ambos proyectos validando tipos en paralelo.
   - `npm run lint`: Ejecuta el análisis estático en todo el monorepo.
