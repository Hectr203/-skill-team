# Guía de Selección de Stacks Tecnológicos y Estándares Transversales

Esta sección establece el catálogo de tecnologías, criterios de selección y estándares transversales para los proyectos desarrollados o mantenidos por la Agencia de Proyectos.

---

## 1. Stack Tecnológico Predeterminado (Greenfield)

Para proyectos creados desde cero, la agencia adopta por defecto un stack moderno, fuertemente tipado y de alto rendimiento organizado bajo un **Monorepo dividido**:

* **Backend**: Node.js (v20+ LTS) con Express.js y TypeScript estricto.
* **Frontend**: React (v18+) con TypeScript y Vite (o Next.js para SSR/SEO intensivo).
* **Base de Datos**: PostgreSQL (v15+).
* **ORM y Migraciones**: Prisma ORM con migraciones atómicas versionadas.
* **Gestión de Monorepo**: Workspaces (`npm` o `pnpm`) con scripts concurrentes en la raíz.

---

## 2. Guía de Selección de Estilos y Diseño Visual

> [!IMPORTANT]
> **Regla de oro visual**: Queda terminantemente prohibido instalar Bootstrap y Tailwind CSS simultáneamente por defecto.

La selección de la capa visual debe basarse en la siguiente matriz de decisión:

| Opción Visual | Cuándo Elegirla | Ventajas Clave | Compromisos / Cuidados |
|---|---|---|---|
| **Tailwind CSS** | Aplicaciones con diseño a medida, microinteracciones ricas y componentes de **React Bits** o **Google Stitch**. | Máxima flexibilidad, cero CSS no utilizado, control fino de tokens. | Requiere disciplina para no saturar el JSX de clases utilitarias extensas. |
| **Bootstrap** | Paneles administrativos rápidos, herramientas internas donde la velocidad de entrega prima sobre la personalización visual extrema. | Componentes listos y probados, cuadrícula robusta, familiaridad. | Más difícil de personalizar profundamente con acabados estilo Apple/Linear. |
| **Biblioteca de Componentes (Radix / Shadcn / Chakra)** | Proyectos que exigen accesibilidad nativa rigurosa (WAI-ARIA) y componentes de formulario complejos. | Accesibilidad garantizada, foco en comportamiento, fácil estilizado con Tailwind. | Requiere entender la composición headless. |
| **Sistema de Diseño Propio (Tokens Puros)** | Proyectos con identidad de marca cerrada o requerimientos estrictos de rendimiento extremo. | Cero dependencia de terceros, control total de bytes. | Mayor tiempo inicial de desarrollo de bloques atómicos. |

---

## 3. Estándares Transversales Obligatorios

1. **Autenticación y Sesiones**:
   - Autenticación stateless mediante tokens JWT de vida corta (15 min) + Refresh Tokens rotativos seguros almacenados en cookies `HttpOnly`, `Secure` y `SameSite=Strict`.
2. **Autorización y Control de Acceso (RBAC)**:
   - Verificación de permisos a nivel de ruta contra el catálogo centralizado (`shared/auth/permissions.catalog.ts`).
3. **Validación de Entradas (Zod)**:
   - Esquemas DTO estrictos en todos los endpoints HTTP y validación de variables de entorno (`.env`) al iniciar la aplicación.
4. **Manejo de Errores Uniforme**:
   - Clase base `ApiError` para errores HTTP controlados (400, 401, 403, 404, 409).
   - Middleware centralizado que captura excepciones no controladas (500) sin exponer stack traces al cliente en producción.
5. **Seguridad y Cabeceras**:
   - Configuración de cabeceras seguras con Helmet (CSP, HSTS, X-Frame-Options).
   - CORS con lista blanca explícita de orígenes autorizados.
6. **Migraciones y Semillas (Prisma)**:
   - Separación estricta entre generación de cliente (`prisma generate`) y aplicación de migraciones (`prisma migrate deploy`).
   - Seeds idempotentes (`prisma/seed.ts`) para datos iniciales de catálogo y usuarios de prueba.
7. **Procesos en Segundo Plano y Trabajos Asíncronos**:
   - Tareas pesadas (envío de correos, generación de PDFs, sincronizaciones externas) delegadas a colas de trabajo (BullMQ / Redis o jobs programados).
8. **Observabilidad y Monitoreo**:
   - Logs estructurados en formato JSON (Winston o Pino) con identificador único de petición (`x-request-id`).
   - Métricas de salud del sistema mediante endpoint `/health` y `/ready`.
