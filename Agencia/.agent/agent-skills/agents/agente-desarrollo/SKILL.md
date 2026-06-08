---
name: agente-desarrollo
description: Asistente experto en el stack y arquitectura del proyecto (Backend Node/Prisma, Frontend React/Vite/Tailwind). Garantiza la correcta separación de capas y estructura modular.
---
# Skill: Agente de Desarrollo (Arquitectura del Proyecto)

## Objetivo
Actuar como un desarrollador experto que conoce perfectamente el stack, la arquitectura y las reglas de negocio de este repositorio. El agente debe adherirse estrictamente a las convenciones de carpetas, tecnologías y patrones definidos para el backend y el frontend.

## Stack Tecnológico
- **Backend:** Node.js, Express, TypeScript, Prisma ORM (PostgreSQL), JWT, bcryptjs.
- **Frontend:** React (Vite), TypeScript, Tailwind CSS, React Router DOM, Zustand, Axios, Lucide React, Sonner (notificaciones).

## Arquitectura Backend (Clean Architecture & Modular)
Todo desarrollo backend se agrupa por sub-dominios en `backend/src/modules/`.

### Estructura de un módulo Backend:
```text
/backend/src/modules/administracion/almacenes/
├── almacenes.routes.ts       # Definición de rutas Express y asignación de middlewares
├── almacenes.controller.ts   # Manejo de Req/Res HTTP y captura de errores
└── almacenes.service.ts      # Lógica de negocio e interacción con Prisma
```

### Reglas Backend:
1. **Separación de Capas:** El controlador (`.controller.ts`) NUNCA debe invocar a Prisma de forma directa. Todo controlador debe delegar al servicio (`.service.ts`), el cual concentra la lógica de negocio y realiza las consultas a la base de datos usando Prisma.
2. **Nomenclatura:** Los archivos se nombran usando la convención `.controller.ts`, `.service.ts`, `.routes.ts`. Los métodos usan `camelCase` (ej. `crearAlmacen()`).
3. **Manejo de Errores:** Se deben capturar las excepciones en el controlador y responder con el formato JSON estandarizado del proyecto.
4. **Dependencias:** Emplea las librerías existentes en `backend/package.json` (Express, Prisma, bcrypt, jsonwebtoken). No instales nuevas tecnologías sin validación.

## Arquitectura Frontend (Atomic Design & Modular)
El frontend organiza su lógica de negocio en módulos (`frontend/src/modules/`), pero sus componentes UI genéricos se construyen siguiendo el modelo **Atomic Design** (`frontend/src/components/`).

### Estructura Atomic Design (`frontend/src/components/`):
- **atoms/**: Elementos básicos e indivisibles de UI (ej. botones, inputs, iconos, etiquetas).
- **molecules/**: Combinación simple de átomos (ej. campos de formulario con labels, barras de búsqueda).
- **organisms/**: Secciones complejas y funcionales que agrupan moléculas y átomos (ej. headers, sidebars, tablas de datos).
- **templates/**: Layouts base sin datos que definen la estructura de la página (ej. AppShellTemplate).

### Estructura de un módulo Frontend (`frontend/src/modules/`):
```text
/frontend/src/modules/administracion/almacenes/
├── components/               # Componentes locales específicos del módulo
├── services/                 # Llamadas HTTP a la API (ej. almacenesService.ts)
├── types/                    # Interfaces TS del módulo (ej. almacenTypes.ts)
└── index.tsx                 # Vista principal que orquesta la UI usando templates y organisms
```

### Reglas Frontend:
1. **Componentes y Estilos (Atomic Design):** Cuando crees un elemento UI reutilizable, ubícalo en la capa atómica correspondiente (`atoms`, `molecules`, `organisms`). Si es específico de una vista, ponlo en `modules/<dominio>/components/`. Usa EXCLUSIVAMENTE Tailwind CSS.
2. **Servicios API:** Toda interacción con el backend debe realizarse mediante funciones exportadas desde `services/` utilizando `Axios`. Ningún componente de UI debe hacer llamadas directas.
3. **Tipado Fuerte:** Toda entidad consumida o enviada debe estar tipada mediante interfaces definidas en `types/`.
4. **Gestión de Estado:** Emplea estado local (`useState`/`useReducer`) cuando sea posible. Para estado global, usa `Zustand`.
5. **UI y UX:** Mantén consistencia visual. Usa `lucide-react` para iconos y `sonner` para notificaciones.

## Flujo de Trabajo Obligatorio del Agente
1. **Análisis Arquitectónico:** Antes de escribir una sola línea de código, analiza en qué módulos impacta el cambio (Backend y Frontend) y diseña la estructura de archivos respetando el patrón modular descrito.
2. **Generación de Código Estricta:** Implementa los archivos delegando la responsabilidad de forma correcta (Controlador -> Servicio -> Prisma) y (Vista -> Componente -> Servicio Axios). 
3. **Validación de Integridad:** Comprueba que los imports sean precisos y que el contrato de datos (Interfaces del Frontend) coincida con la respuesta de la API (Backend).
4. **Documentación de Cambios:** Al finalizar la implementación, DEBES documentar qué hiciste y cómo lo hiciste.
   - **Ubicación exacta:** Guarda la documentación en el directorio `Agencia/INFORACION DE AGNETES/documentacion de agnetes/informe de desarollo/`.
   - **Carpetas Individuales:** Por CADA nuevo informe o requerimiento completado, crea una nueva subcarpeta con un nombre claro y descriptivo (formato kebab-case o snake_case).
   - **Archivo Principal:** Dentro de la nueva carpeta, crea un archivo `.md` (ej. `informe.md`) detallando las modificaciones realizadas, archivos afectados, decisiones técnicas y cómo se resolvió la tarea.
