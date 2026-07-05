# Flujo Completo de Desarrollo y CI/CD

## Objetivo
Unificar el ciclo completo de desarrollo: desde la especificacion hasta el despliegue en produccion, integrando calidad continua, pruebas automatizadas y despliegue seguro.

## Ciclo de Vida

```
ESPECIFICACION -> PLANIFICACION -> DESARROLLO -> VERIFICACION -> REVISION -> DESPLIEGUE
                                                                              |
                                                                       MONITOREO
                                                                              |
                                                                       RETROALIMENTACION
```

---

## Fase 0: Inicializar Proyecto

Aplica solo para proyectos nuevos. Seguir `flujos/crear-y-configurar-proyecto.md`.

**Entregables:**
- Repositorio git inicializado.
- Stack definido (Node 22, Express, TypeScript, Prisma, React, Tailwind).
- Perfil de despliegue Azure definido (sin crear recursos).
- `.github/workflows/ci.yml` y `.github/workflows/deploy.yml` configurados.
- `playwright.config.ts` con configuracion basica.
- Linter y formateador configurados (ESLint + Prettier).

---

## Fase 1: Especificacion (DEFINE)

**Skills:** `spec-driven-development`, `idea-refine`, `analista-requerimientos`
**Agentes:** `analista-requerimientos`, `asistente-principal`

1. Entender requerimiento del humano.
2. Redactar especificacion clara con criterios de aceptacion.
3. Identificar modulos afectados (backend, frontend, BD, despliegue).
4. Si es critico o ambiguo, aplicar `/improve quick` con `mejora-asesor`.

**Compuerta:** Humano aprueba especificacion.

---

## Fase 2: Planificacion (PLAN)

**Skills:** `planning-and-task-breakdown`, `incremental-implementation`
**Agentes:** `agente-arquitectura`, `asistente-principal`

1. Descomponer especificacion en tareas atomicas (< 1 dia).
2. Identificar dependencias entre tareas.
3. Asignar nivel de prueba para cada tarea: unitario, integracion o E2E.
4. Estimar riesgo: bajo, medio, alto (requiere validacion extra).

**Compuerta:** Plan de tareas documentado y aprobado.

---

## Fase 3: Desarrollo (BUILD)

**Skills:** `backend-dominio-limpio`, `prisma-base-de-datos`, `frontend-design`, `ui-ux-pro-max`, `api-and-interface-design`, `frontend-ui-engineering`, `context-engineering`
**Agentes:** `agente-desarrollo`, `agente-backend`, `agente-frontend`, `agente-base-de-datos`

### Subfase 3.1: Preparacion
1. Leer arquitectura existente y patrones del proyecto.
2. Aplicar `ponytail` antes de crear archivos: evaluar si realmente se necesita.
3. Validar que la solucion no introduzca dependencias innecesarias.

### Subfase 3.2: Implementacion (TDD)
1. Escribir prueba unitaria (Red).
2. Implementar logica minima (Green).
3. Refactorizar sin cambiar comportamiento (Refactor).
4. Escribir prueba de integracion si el modulo cruza fronteras (API, DB).
5. Verificar que todas las pruebas pasan localmente con `npx playwright test`.

### Subfase 3.3: Anti-sobreingenieria
Antes de dar por terminada una tarea, responder:
- ?Realmente necesito esta abstraccion o puedo resolverlo mas simple?
- ?La stdlib o una dependencia ya existente lo cubre?
- ?Estoy creando codigo que solo se usara en este unico lugar?
- ?Puedo resolverlo en menos archivos?
- Marcar simplificaciones intencionales con `ponytail:`.

**Compuerta:** Pruebas unitarias + integracion pasan localmente, `npm run lint` OK.

---

## Fase 4: Verificacion (VERIFY)

**Skills:** `playwright-mcp-testing`, `test-driven-development`, `browser-testing-with-devtools`, `debugging-and-error-recovery`
**Agentes:** `ingeniero-de-pruebas`, `tester`

### CI Pipeline (automatico en cada push/PR)

El archivo `.github/workflows/ci.yml` ejecuta:

```
Push/PR
  |
  v
Compuerta de Calidad (paralelo):
  - Linter (npm run lint)
  - TypeScript (npm run typecheck)
  - Prisma validate (npx prisma validate)
  |
  v
Pruebas (paralelo):
  - Unitarias + Integracion (npm test)
  - E2E (npx playwright test)
  |
  v
Build (paralelo):
  - Backend (npm run build --workspace=backend)
  - Frontend (npm run build --workspace=frontend)
  |
  v
Seguridad (paralelo):
  - npm audit
  - TruffleHog (secretos)
```

1. Ejecutar pipeline completo en CI.
2. Si falla, ir a `debugging-and-error-recovery` para diagnosticar.
3. Si es un bug, aplicar Prove-It: escribir prueba que falla, corregir, verificar.
4. Validar en navegador real con Playwright MCP solo si el cambio es visual.

**Compuerta:** Pipeline CI verde (lint, typecheck, tests, build, security).

---

## Fase 5: Revision (REVIEW)

**Skills:** `code-review-and-quality`, `revision-codigo`, `security-and-hardening`, `seguridad`, `code-simplification`
**Agentes:** `revisor-de-codigo`, `code-reviewer`, `auditor-de-seguridad`, `security-editor`

1. `code-reviewer` revisa en 5 ejes: correctitud, legibilidad, arquitectura, seguridad, rendimiento.
2. `security-editor` revisa si el cambio toca autenticacion, datos sensibles o APIs publicas.
3. Verificar que `ponytail` se aplico: no hay abstracciones innecesarias, no hay dependencias nuevas sin justificacion.

**Compuerta:** Code review aprobado, sin hallazgos critical/high sin resolver.

---

## Fase 6: Despliegue (SHIP)

**Skills:** `despliegue-azure-proyecto-nuevo`, `ci-cd-and-automation`, `shipping-and-launch`, `git-workflow-and-versioning`
**Agentes:** `agente-despliegue-azure`

### CD Pipeline (automatico al hacer merge a main)

```
Merge a main
  |
  v
[CI pasa] -> [CD se activa]
  |
  v
Autenticar Azure (AZURE_CREDENTIALS)
  |
  v
Crear/actualizar infraestructura (Bicep)
  |
  v
Desplegar backend + frontend
  |
  v
Ejecutar migraciones
  |
  v
Verificar salud (curl /api/health)
  |
  v
Reporte de despliegue
```

1. Seguir `flujos/desplegar-en-azure.md` si es el primer despliegue.
2. Para despliegues subsecuentes, el pipeline CD automatiza todo.
3. Verificar health check y pruebas post-despliegue.
4. Si falla, ejecutar rollback: `git revert HEAD && git push`.

**Compuerta:** Aplicacion funcionando en produccion, health check OK, pruebas de integracion pasan.

---

## Fase 7: Documentacion y Cierre

**Skills:** `documentation-and-adrs`, `documentacion-tecnica`, `ahorro-contexto`
**Agentes:** `agente-documentacion`, `agente-contexto`

1. Seguir `flujos/revision-y-cierre.md`.
2. Actualizar memoria del proyecto con cambios, decisiones y riesgos.
3. Si hubo Azure, guia operativa final con comandos reales.

---

## Matriz de Skills por Fase

| Fase | Skills locales | Skills agent-skills |
|------|---------------|---------------------|
| INICIAR | `crear-y-configurar-proyecto` | - |
| ESPECIFICAR | `analisis-requerimientos` | `spec-driven-development`, `idea-refine` |
| PLANIFICAR | - | `planning-and-task-breakdown` |
| DESARROLLAR | `backend-dominio-limpio`, `prisma-base-de-datos`, `ui-ux-pro-max`, `ponytail` | `incremental-implementation`, `test-driven-development`, `api-and-interface-design`, `frontend-ui-engineering`, `context-engineering` |
| VERIFICAR | `playwright-mcp-testing` | `browser-testing-with-devtools`, `debugging-and-error-recovery` |
| REVISAR | `revision-codigo`, `seguridad` | `code-review-and-quality`, `code-simplification`, `security-and-hardening` |
| DESPLEGAR | `despliegue-azure-proyecto-nuevo` | `ci-cd-and-automation`, `shipping-and-launch`, `git-workflow-and-versioning` |
| DOCUMENTAR | `documentacion-tecnica`, `ahorro-contexto` | `documentation-and-adrs` |

## Reglas Globales

1. No saltar fases. Toda funcionalidad debe pasar por especificacion -> plan -> desarrollo -> verificacion -> revision -> despliegue.
2. CI debe pasar antes de hacer merge a main. Sin excepciones.
3. No desplegar sin CI verde. Si es urgente, documentar el riesgo y obtener aprobacion humana explicita.
4. E2E solo para flujos criticos. Lo demas con unitarias o integracion.
5. Toda dependencia nueva debe justificarse en la revision.
6. `ponytail` aplica en cada fase de desarrollo: preguntar si realmente se necesita.
7. Los nombres de commits en espanol usando `commits-espanol`.
