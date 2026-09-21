# Flujo de Proyecto Nuevo (Greenfield)

Este flujo dirige la creación de nuevos proyectos de software desde cero, asegurando que ninguna estructura técnica se construya antes de comprender a fondo el problema de negocio y garantizando una arquitectura de **Monorepo dividido** limpia y modular.

---

## Fases del Proceso Greenfield

```text
1. Descubrimiento ──> 2. Requisitos y Alcance ──> 3. Arquitectura y Monorepo ──> 4. Prototipado Stitch ──> 5. Estructura Base e Indexación Graphify ──> 6. Loops SDD (Ponytail) ──> 7. Pruebas y Auditoría ──> 8. Despliegue y Memoria
```

---

### Fase 1: Descubrimiento del Problema y Producto
- **Entrevistar al usuario**: Comprender qué problema resuelve el software, quiénes son los usuarios finales y cuál es la métrica de éxito.
- **Regla inalterable**: Queda estrictamente prohibido generar carpetas, archivos de código o configuraciones técnicas durante esta fase.
- **Entregable**: Resumen de descubrimiento en `contexts/projects/<project-id>/manifiesto.md`.

### Fase 2: Requisitos y Alcance (Spec-Driven Development)
- Formalizar Requisitos Funcionales (RF) y Requisitos No Funcionales (RNF: rendimiento, seguridad, concurrencia, a11y).
- Delimitar claramente qué queda dentro del alcance del MVP y qué queda explícitamente fuera de alcance.
- Definir criterios de aceptación verificables para cada funcionalidad.

### Fase 3: Arquitectura y Monorepo Dividido
- **Adopción obligatoria de Monorepo Dividido**:
  - `frontend/`: Aplicación de interfaz (React / TypeScript / Vite).
  - `backend/`: Servicio de APIs y lógica de negocio (Node.js / Express / Prisma / PostgreSQL).
  - Prohibición estricta de arquitecturas monolíticas acopladas.
- Registro de Decisiones de Arquitectura iniciales (ADRs) en `decisiones/`.
- Configuración de variables de entorno con esquemas de validación estricta Zod en boot time (`src/config/env.ts`).
- Path aliases estandarizados (`@modules/*`, `@shared/*`).

### Fase 4: Diseño UX/UI (Google Stitch MCP & Atomic Design)
- Consulta al servidor Google Stitch MCP para explorar pantallas prototipadas y extraer tokens visuales.
- Mapeo de design tokens (paletas, tipografía, espaciado) en `src/shared/theme/`.
- Composición atómica: definir átomos y moléculas neutras en `src/shared/components/`.

### Fase 5: Estructura Base e Indexación con Graphify
- Creación de la estructura base de carpetas y dependencias aisladas (`package.json` en raíz, `frontend/` y `backend/`).
- **Indexación obligatoria de Graphify**: Tan pronto como la estructura base esté creada, se ejecuta la indexación para habilitar la navegación semántica y topológica en los pasos de implementación subsiguientes.

### Fase 6: Implementación Incremental Guiada por Ponytail
- Implementación en rebanadas verticales pequeñas (base de datos $\rightarrow$ servicio $\rightarrow$ controlador $\rightarrow$ UI).
- Aplicar la escalera de Ponytail: usar capacidades nativas de la plataforma antes de agregar dependencias superfluas.
- Transacciones atómicas con `prisma.$transaction` para toda mutación interdependiente.
- Servicios desacoplados de Express y controladores delgados con DTOs Zod.

### Fase 7: Pruebas, Verificación y Auditoría
- Pruebas unitarias de servicios y validadores.
- Pruebas E2E en navegadores reales mediante la regla de precedencia (Navegador nativo de Antigravity IDE $\rightarrow$ Playwright MCP).
- Auditoría dual antes de producción: Asesor de calidad con `improve` y Threat Hunter con `security-audit` de Cloudflare (modo read-only).

### Fase 8: Despliegue y Memoria Persistente
- Preparación del despliegue (Azure CLI, Vercel o Docker) previa compuerta humana HITL.
- Ejecución de `scripts/notificar_tarea.py` para alertar al usuario de la finalización.
- Registro del hito en `claude-mem` y actualización del manifiesto del proyecto.
