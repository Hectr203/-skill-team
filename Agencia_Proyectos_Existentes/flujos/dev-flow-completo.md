# Flujo Completo de Desarrollo y CI/CD para Proyectos Existentes

## Objetivo
Unificar el ciclo completo para proyectos existentes: desde el analisis inicial hasta el despliegue, respetando la arquitectura actual, con calidad continua y despliegue controlado.

## Ciclo de Vida

```
ANALISIS -> ESPECIFICACION -> PLANIFICACION -> DESARROLLO -> VERIFICACION -> REVISION -> DESPLIEGUE
                                                                                             |
                                                                                      MONITOREO
```

---

## Fase 0: Analisis Inicial

Aplica al retomar un proyecto existente. Seguir `flujos/analizar-y-continuar-proyecto.md`.

**Skills:** `lectura-arquitectura-existente`, `conservacion-estructura-actual`, `contextos`, `ahorro-contexto`
**Agentes:** `agente-analisis-proyecto-existente`, `agente-contexto`

1. Identificar proyecto y consultar memoria independiente.
2. Mapear: tecnologias, estructura, dependencias, scripts, CI existente.
3. Identificar framework de pruebas actual (Jest, Vitest, Mocha, Playwright, ninguno).
4. Leer ADRs y documentacion de arquitectura si existen.
5. NO modificar archivos en esta fase.

**Compuerta:** Inventario completo del proyecto documentado en memoria.

---

## Fase 1: Especificacion (DEFINE)

**Skills:** `spec-driven-development`, `analisis-requerimientos`, `interview`
**Agentes:** `analista-requerimientos`, `asistente-principal`

1. Definir cambio solicitado con criterios de aceptacion claros.
2. Identificar archivos y modulos afectados.
3. Evaluar riesgo: bajo (cambio localizado), medio (toca varias capas), alto (cambia comportamiento critico).
4. Si es alto riesgo, aplicar `/improve` con `mejora-asesor` (modelo caro analiza, barato ejecuta).

**Compuerta:** Humano aprueba alcance y riesgo.

---

## Fase 2: Planificacion (PLAN)

**Skills:** `planning-and-task-breakdown`, `incremental-implementation`
**Agentes:** `agente-arquitectura`, `asistente-principal`

1. Descomponer en cambios pequenos e independientes.
2. Cada cambio debe ser reversible o tener rollback documentado.
3. Identificar pruebas existentes que deben seguir pasando.

**Compuerta:** Tareas planificadas con orden de implementacion.

---

## Fase 3: Desarrollo (BUILD)

**Skills:** `backend-dominio-limpio`, `adaptacion-proyectos-existentes`, `conservacion-estructura-actual`, `ponytail`
**Agentes:** `engineer`, `agente-backend`, `agente-frontend`, `agente-base-datos`

### Subfase 3.1: Lectura de patrones
1. Leer archivos equivalentes en el proyecto para entender convenciones locales.
2. Identificar estilo de codigo, patrones de nombres, estructura de modulos.
3. NO imponer patrones de la agencia si el proyecto usa otros.

### Subfase 3.2: Implementacion incremental
1. Aplicar un cambio pequeno por vez.
2. Verificar localmente despues de cada cambio (`npm test`, `npm run build`).
3. Si el proyecto no tiene pruebas, agregar test de caracterizacion antes de modificar.

### Subfase 3.3: Anti-sobreingenieria
- No crear capas que no existen en el proyecto.
- No refactorizar "porque se ve mejor" si funciona.
- No agregar dependencias nuevas sin justificacion.
- Si el proyecto usa JS, no migrar a TypeScript sin autorizacion.
- Si el proyecto usa otro ORM, no migrar a Prisma sin autorizacion.

**Compuerta:** Cambio funciona localmente, pruebas existentes pasan.

---

## Fase 4: Verificacion (VERIFY)

**Skills:** `playwright-mcp-testing`, `testing`, `test-driven-development`, `browser-testing-with-devtools`
**Agentes:** `tester`, `code-reviewer`

### CI Pipeline (se adapta al proyecto)

El archivo `.github/workflows/ci.yml` se configura para detectar el stack existente:

```
Push/PR
  |
  v
Compuerta de Calidad:
  - Linter (si existe)
  - TypeScript (si existe)
  |
  v
Pruebas:
  - Framework detectado (Jest/Vitest/Mocha)
  - Playwright E2E (si se agrego)
  |
  v
Build (si existe script)
  |
  v
Seguridad:
  - npm audit
  - TruffleHog (secretos)
```

1. Ejecutar pruebas existentes del proyecto.
2. Si se agregaron pruebas E2E con Playwright, ejecutarlas.
3. Verificar que no hay regresiones.

**Compuerta:** CI verde. Si el proyecto no tenia CI, este pipeline es el primer paso.

---

## Fase 5: Revision (REVIEW)

**Skills:** `revision-codigo`, `code-review-and-quality`, `seguridad`, `security-and-hardening`
**Agentes:** `code-reviewer`, `security-editor`

1. Revisar que el cambio respeta la arquitectura existente.
2. Verificar que no se introdujeron dependencias nuevas sin justificacion.
3. Confirmar que las pruebas existentes siguen pasando.
4. Si el cambio toca seguridad, `security-editor` hace revision adicional.

**Compuerta:** Code review aprobado.

---

## Fase 6: Despliegue (SHIP)

**Skills:** `despliegue-azure-proyecto-existente`, `ci-cd-and-automation`, `git-workflow-and-versioning`
**Agentes:** `agente-despliegue-azure`

### CD Pipeline

```
Merge a main
  |
  v
[CI pasa] -> [CD se activa]
  |
  v
Autenticar Azure
  |
  v
Validar recursos existentes (no recrear sin necesidad)
  |
  v
Desplegar aplicacion
  |
  v
Ejecutar migraciones (con backup)
  |
  v
Verificar salud
  |
  v
Pruebas post-despliegue
  |
  v
Reporte
```

1. Para el primer despliegue, seguir `flujos/desplegar-en-azure.md` completo.
2. Para despliegues subsecuentes, el pipeline CD automatiza.
3. Toda migracion debe tener rollback planificado.

**Compuerta:** Aplicacion funcionando, health check OK.

---

## Fase 7: Documentacion y Cierre

**Skills:** `documentacion-tecnica`, `documentation-and-adrs`, `ahorro-contexto`
**Agentes:** `agente-documentacion`, `agente-contexto`

1. Seguir `flujos/revision-y-cierre.md`.
2. Actualizar memoria independiente del proyecto.
3. Documentar decisiones, riesgos y pendientes.

---

## Matriz de Skills por Fase

| Fase | Skills locales | Skills agent-skills |
|------|---------------|---------------------|
| ANALIZAR | `lectura-arquitectura-existente`, `conservacion-estructura-actual`, `contextos` | - |
| ESPECIFICAR | `analisis-requerimientos`, `interview` | `spec-driven-development`, `idea-refine` |
| PLANIFICAR | - | `planning-and-task-breakdown` |
| DESARROLLAR | `adaptacion-proyectos-existentes`, `backend-dominio-limpio`, `ponytail` | `incremental-implementation`, `test-driven-development`, `context-engineering` |
| VERIFICAR | `testing`, `playwright-mcp-testing` | `browser-testing-with-devtools`, `debugging-and-error-recovery` |
| REVISAR | `revision-codigo`, `seguridad` | `code-review-and-quality`, `code-simplification`, `security-and-hardening` |
| DESPLEGAR | `despliegue-azure-proyecto-existente` | `ci-cd-and-automation`, `git-workflow-and-versioning`, `shipping-and-launch` |
| DOCUMENTAR | `documentacion-tecnica`, `ahorro-contexto` | `documentation-and-adrs` |

## Loop de iteraciones (Fase 8: Ciclo de Correccion)

Despues de la Fase 5 (Revision), si existen criterios de aceptacion incumplidos, se activa el ciclo de correccion:

### Fase 8.1: Evaluacion de resultados
1. Clasificar cada criterio de aceptacion como: Cumplido, Incumplido, Parcialmente, Bloqueado o No aplicable.
2. Para cada incumplimiento, registrar:
   - Requerimiento afectado.
   - Resultado esperado vs. obtenido.
   - Evidencia (captura, log, traza).
   - Posible causa.
   - Accion correctiva recomendada.

### Fase 8.2: Correccion
1. Enviar errores al agente de desarrollo con evidencias.
2. Aplicar correcciones especificas respetando la arquitectura existente.
3. No repetir una correccion identica que ya haya fallado.
4. Verificar localmente antes de reingresar a validacion.

### Fase 8.3: Re-validacion
1. Ejecutar nuevamente las pruebas afectadas.
2. Verificar que las correcciones no introdujeron regresiones en pruebas existentes.
3. Recopilar nuevas evidencias.
4. Actualizar el registro de iteraciones.

### Fase 8.4: Control del ciclo
1. Registrar cada iteracion con su numero correlativo.
2. Maximo 5 iteraciones por defecto.
3. Si un error persiste tras 3 intentos, documentar bloqueo y escalar al humano.
4. No declarar exito si las pruebas no pueden ejecutarse.
5. Cuando una validacion no sea posible, indicar que queda sin verificar.

### Registro de iteracion

Cada ciclo debe documentarse en el informe de cierre con:

| Iteracion | Objetivo | Agentes | Pruebas | Errores | Correcciones | Criterios OK | Criterios pendientes | Estado |
|-----------|----------|---------|---------|---------|--------------|-------------|---------------------|--------|
| 1 | Implementar X | Desarrollo, Pruebas | Unitarias, E2E | Error en Y | Se corrigio Z | CA-001, CA-002 | CA-003 | En progreso |

## Reglas para Proyectos Existentes

1. La arquitectura existente prevalece. No imponer tecnologias nuevas.
2. Todo cambio debe ser reversible o tener rollback documentado.
3. CI debe incluir las pruebas existentes. Si no hay, ese es el primer hallazgo.
4. Playwright se agrega solo si el proyecto tiene interfaz web.
5. No reemplazar framework de pruebas existente sin autorizacion.
6. Las migraciones de BD siempre con backup y rollback.
7. `ponytail` aplica: preguntar si realmente se necesita cambiar algo o solo documentar.
8. Si el proyecto no tiene CI, crearlo como primer paso antes de cualquier cambio funcional.
9. Ninguna tarea se cierra sin evidencias de que todos los criterios de aceptacion obligatorios estan cumplidos.
10. El orquestador no acepta "esta terminado" sin revisar resultados de pruebas y evidencias concretas.
