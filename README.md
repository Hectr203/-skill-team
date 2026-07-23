# Skill Team - Sistema de Agencias de IA

Bienvenido al repositorio central de nuestras **Agencias de IA**. Este documento sirve como la guia principal para desarrolladores, arquitectos y mantenedores del equipo.

Aqui documentamos como esta estructurado nuestro ecosistema de asistentes, para que sirve cada "Agencia" (entornos de desarrollo de IA) y como colaboran las diferentes *skills* para crear, mantener y disenar software.

---

## Arquitectura General

Dividimos nuestras capacidades de IA en entornos aislados o **Agencias**. Cada agencia cuenta con un **Asistente Principal (Orquestador)**, **agentes especializados** y una carpeta de *skills* con reglas estrictas.

La division principal obedece a la etapa del ciclo de vida del software:

1. **`Agencia_para_proyectos_desde_0`**: Para software nuevo (*Greenfield*).
2. **`Agencia_Proyectos_Existentes`**: Para mantenimiento y evolucion (*Brownfield*).

---

## 1. Agencia para Proyectos Desde 0

**Carpeta:** `Agencia_para_proyectos_desde_0/`

### Proposito

Agencia constructora disenada exclusivamente para **analizar, definir, planificar y programar proyectos totalmente nuevos**. Asume que no hay deuda tecnica y tiene libertad para implementar la arquitectura estandar desde el primer commit.

### Flujo y Arquitectura

- **Levantamiento inicial:** El Asistente Principal entrevista al usuario y define la arquitectura.
- **Estandares rigurosos:** Node.js 22 LTS, Express, TypeScript, PostgreSQL y Prisma en backend (Clean Architecture). React, Tailwind CSS, Zustand en frontend (Atomic Design).
- **Memoria persistente:** Cloud Mem para frontend visual; Mem Palace para secretos, reglas de negocio y datos sensibles.
- **Minimalismo:** `ponytail` evalua antes de crear codigo para evitar configuraciones y dependencias innecesarias.

### Agentes Especializados

| Agente | Rol |
|--------|-----|
| `analista-requerimientos` | Convierte informacion cruda en requerimientos estructurados |
| `agente-arquitectura` | Decisiones estructurales y ADRs |
| `agente-backend` | APIs, servicios, casos de uso, capa de datos |
| `agente-frontend` | Componentes React, Atomic Design, estado |
| `agente-base-de-datos` | Modelos Prisma, migraciones, semillas |
| `ingeniero-de-pruebas` | Testing con Playwright MCP, estrategia QA |
| `revisor-de-codigo` | Revision en 5 ejes (correctitud, legibilidad, arquitectura, seguridad, rendimiento) |
| `auditor-de-seguridad` | Deteccion de vulnerabilidades, OWASP |
| `agente-documentacion` | ADRs, bitacoras, informes de cierre |
| `agente-despliegue-azure` | Infraestructura y despliegue Azure |
| `agente-orquestador` | Coordinacion entre especialistas |
| `agente-contexto` | Gestion de memoria persistente |

### Skills Obligatorias

| Skill | Proposito |
|-------|-----------|
| `backend-dominio-limpio` | Clean Architecture para backend |
| `prisma-base-de-datos` | Esquemas Prisma, migraciones, transacciones |
| `ui-ux-pro-max` | Componentes visuales, accesibilidad, coherencia |
| `ahorro-contexto` | Memoria persistente (Python scripts) |
| `commits-espanol` | Trazabilidad en espanol |
| `ponytail` | YAGNI, stdlib primero, minimalismo |
| `despliegue-azure-proyecto-nuevo` | Azure CI/CD e infraestructura |
| `playwright-mcp-testing` | Testing E2E, integracion y QA con Playwright |
| `mejora-asesor` | Auditoria con dos modelos (caro analiza, barato ejecuta) |

---

## 2. Agencia de Proyectos Existentes

**Carpeta:** `Agencia_Proyectos_Existentes/`

### Proposito

Agencia auditora y mantenedora orientada a **analizar, mantener, refactorizar y escalar proyectos que ya poseen historial de codigo, reglas de equipo y deuda tecnica**.

### Principio Rector

> **La arquitectura existente prevalece** sobre cualquier preferencia generica de la agencia, salvo que exista una razon tecnica concreta para modificarla.

### Flujo y Arquitectura

- **Auditoria antes de accion:** Lee la arquitectura, detecta convenciones, realiza cambios incrementales.
- **Sin imposiciones:** No impone tecnologias si el proyecto ya funciona de otra forma.
- **Memoria aislada:** Cada proyecto tiene su propia carpeta `.memoria/` para evitar contaminacion entre proyectos.
- **Ponytail respetuoso:** Inspecciona reglas existentes y se fusiona sin sobrescribir.

### Agentes Especializados

| Agente | Rol |
|--------|-----|
| `analista-requerimientos` | Requerimientos para cambios existentes |
| `agente-analisis-proyecto-existente` | Mapeo de repositorios desconocidos |
| `agente-arquitectura` | Decisiones estructurales con conservacion |
| `agente-backend` | APIs, servicios (respeta stack actual) |
| `agente-frontend` | UI (respeta framework actual) |
| `agente-base-datos` | Modelos y migraciones (respeta ORM actual) |
| `tester` | Testing con Playwright MCP + framework existente |
| `code-reviewer` | Revision en 5 ejes para cambios |
| `security-editor` | Endurecimiento y auditoria de seguridad |
| `engineer` | Implementacion de cambios respetando estructura |
| `agente-integracion` | APIs externas, webhooks, colas |
| `agente-refactorizacion` | Simplificacion controlada sin cambiar comportamiento |
| `agente-mantenimiento` | Bugs menores y salud del sistema |
| `agente-despliegue-azure` | Azure para proyectos existentes |
| `agente-documentacion` | ADRs, informes, guias |
| `agente-contexto` | Memoria y contexto del proyecto |

### Skills Locales

| Skill | Proposito |
|-------|-----------|
| `adaptacion-proyectos-existentes` | Adaptacion a repositorios iniciados |
| `lectura-arquitectura-existente` | Lectura de estructura y capas |
| `conservacion-estructura-actual` | Prevencion de reestructuraciones |
| `refactorizacion-controlada` | Mejora sin alterar comportamiento |
| `revision-codigo` | Revision de PRs y cambios |
| `seguridad` | Vulnerabilidades y hardening |
| `testing` | Pruebas proporcionales al riesgo |
| `documentacion-tecnica` | ADRs, guias, bitacoras |
| `backend-dominio-limpio` | Adaptado al patron local del proyecto |
| `ui-ux-pro-max` | Modernizacion de interfaces existentes |
| `spec-driven-development` | Especificaciones antes de implementar |
| `respuestas-simples` | Respuestas directas sin rodeos |
| `comunicacion-espanol` | Documentacion en espanol claro |
| `contextos` | Informacion relevante del proyecto |
| `interview` | Extraccion de requerimientos del cliente |
| `referrals` | Materiales de referidos |
| `playwright-mcp-testing` | Testing E2E con Playwright (se suma al framework actual) |
| `mejora-asesor` | Auditoria con dos modelos (conservando arquitectura) |
| `creador-habilidades` | Creacion de nuevas skills documentadas |

---

## 3. Ecosistema agent-skills (addyosmani)

Integrado en ambas agencias via `skills/agent-skills/`. Aporta **23 skills profesionales** que cubren todo el ciclo de vida del desarrollo:

| Fase | Skills |
|------|--------|
| **DEFINIR** | `spec-driven-development`, `idea-refine` |
| **PLANIFICAR** | `planning-and-task-breakdown` |
| **CONSTRUIR** | `incremental-implementation`, `test-driven-development`, `api-and-interface-design`, `frontend-ui-engineering`, `context-engineering`, `source-driven-development`, `doubt-driven-development` |
| **VERIFICAR** | `browser-testing-with-devtools`, `debugging-and-error-recovery` |
| **REVISAR** | `code-review-and-quality`, `code-simplification`, `security-and-hardening`, `performance-optimization` |
| **ENTREGAR** | `git-workflow-and-versioning`, `ci-cd-and-automation`, `deprecation-and-migration`, `documentation-and-adrs`, `shipping-and-launch` |
| **META** | `using-agent-skills` |

Ademas incluye 3 **agentes especializados**: `code-reviewer`, `test-engineer`, `security-auditor` y referencias de testing, seguridad, rendimiento y accesibilidad.

---

## 4. Playwright MCP Testing

El framework de testing unificado es **Playwright** con integracion MCP para que los agentes interactuen con navegadores reales.

### Herramientas MCP disponibles

- `browser_navigate` - Navegar a URLs
- `browser_click` - Hacer clic en elementos
- `browser_snapshot` - Inspeccionar DOM accesible
- `browser_take_screenshot` - Capturar pantallazos
- `browser_type` - Escribir en campos
- `browser_evaluate` - Ejecutar JS en pagina
- `browser_network_requests` - Capturar trafico de red

### Niveles de prueba

| Nivel | Tecnologia | Cuando |
|-------|-----------|--------|
| Unitario | Playwright Test | Logica pura sin I/O |
| Integracion | Playwright `request` | Endpoints de API |
| E2E | Playwright MCP browser | Flujos criticos de usuario |

### Skills de testing

- `playwright-mcp-testing` - Configuracion, estructura y CI para proyectos nuevos y existentes.
- `agent-skills/skills/test-driven-development/SKILL.md` - TDD clasico Red-Green-Refactor.
- `agent-skills/skills/browser-testing-with-devtools/SKILL.md` - Debugging visual con DevTools MCP.
- `agent-skills/references/testing-patterns.md` - Patrones de pruebas.

---

## 5. Patron de Dos Modelos (mejora-asesor)

Wrapper sobre `shadcn/improve` que implementa un flujo de auditoria y mejora con dos modelos para optimizar costo y calidad.

### Flujo

```
Humano solicita mejora
        |
        v
Fase 1: MODELO CARO (INTELIGENCIA)
  - Claude Opus 4 / Sonnet 4
  - GPT-5 / GPT-5.2
  - DeepSeek-V4
  - Gemini 2.5 Pro
  - Hace Recon + Audit en 9 categorias
  - Genera planes priorizados en plans/
        |
        v
Humano aprueba planes
        |
        v
Fase 2: MODELO BARATO (IMPLEMENTACION)
  - Claude Haiku / Sonnet 4
  - GPT-4o mini / GPT-5.3
  - DeepSeek-V3 / DeepSeek-R1
  - Gemini 2.5 Flash
  - Ejecuta planes paso a paso
        |
        v
Fase 3: VALIDACION (modelo caro revisa diff)
  - Verifica alcance, pruebas, regresiones
```

### Invocacion

- `/improve` - Audit estandar (modelo caro -> humano -> barato)
- `/improve quick` - Audit rapido con ejecucion inmediata
- `/improve deep` - Audit profundo con 8 subagentes
- `/improve execute <plan>` - Ejecutar plan con modelo barato

### Reglas

1. El analisis SIEMPRE con el modelo mas caro disponible.
2. La ejecucion SIEMPRE con el modelo mas barato disponible.
3. Si el modelo barato no puede completar, escalar al caro.
4. No ejecutar planes sin aprobacion humana previa.
5. Fase 1 es estrictamente read-only (no modifica codigo).

---

## 6. Ponytail - Anti-sobreingenieria Transversal

**Ponytail** es el "senior dev flojo". Su objetivo es escribir el **minimo codigo posible** aplicando YAGNI en cada decision.

### Reglas principales

1. preguntar si realmente se necesita construir algo.
2. Si la stdlib lo resuelve, usarla.
3. Si una API nativa del navegador lo cubre, usarla.
4. Si una dependencia ya instalada lo resuelve, usarla.
5. Intentar resolverlo en una linea.
6. Solo entonces: escribir el minimo codigo que funcione.

### Anti-sobreingenieria en cada agente

Cada agente en ambas agencias incluye ahora una seccion explicita de anti-sobreingenieria:

| Agente | Reglas de anti-sobreingenieria |
|--------|--------------------------------|
| `agente-desarrollo` | No abstracciones no solicitadas, stdlib first, sin boilerplate |
| `engineer` | Cambio mas pequeno que cumpla el requerimiento |
| `agente-backend` (existentes) | No crear capas que no existen, no refactorizar sin razon |
| `agente-frontend` (existentes) | No imponer Atomic Design, no crear componentes de un solo uso |
| `agente-refactorizacion` | Chesterton's Fence, no refactorizar "porque se ve feo" |
| `agente-documentacion` | No documentar trivialidades que el codigo ya explica |

---

## 7. Guias de Activacion

### Agentes

| Necesidad | Agente |
|-----------|--------|
| Requerimientos ambiguos | `analista-requerimientos` |
| Backend, APIs, servicios | `agente-backend` |
| Frontend, UI, componentes | `agente-frontend` |
| Base de datos, migraciones | `agente-base-de-datos` |
| Tests, estrategia QA | `tester` / `ingeniero-de-pruebas` |
| Code review | `code-reviewer` |
| Seguridad | `security-editor` / `auditor-de-seguridad` |
| Arquitectura | `agente-arquitectura` |
| Refactorizacion | `agente-refactorizacion` |
| Documentacion | `agente-documentacion` |
| Azure | `agente-despliegue-azure` |
| Auditoria profunda | `mejora-asesor` (skill de dos modelos) |

### Skills del ecosistema

Ver `guias/criterios-activacion-skills.md` en cada agencia para la matriz completa de 30+ skills.

---

## 8. Mejoras Recientes

### v2.0 - Julio 2026

- **Playwright MCP Testing:** Nueva skill unificada de testing con ejemplos de configuracion, unitarias, integracion, E2E y CI. Los agentes de testing ahora usan `browser_navigate`, `browser_click`, `browser_snapshot`, etc.
- **Integracion agent-skills (addyosmani):** 23 skills profesionales copiadas a `Agencia_para_proyectos_desde_0/skills/agent-skills/`. Mapeadas por fase del ciclo de vida en ambos orquestadores.
- **mejora-asesor (wrapper de shadcn/improve):** Skill de dos modelos que ejecuta analisis con el modelo mas caro y ejecucion con el mas barato. Incluye validacion cruzada.
- **Anti-sobreingenieria reforzada:** Secciones explicitas de YAGNI/ponytail en todos los agentes de desarrollo, backend, frontend, refactorizacion y documentacion.
- **Testing.md actualizado:** Referencia a Playwright MCP como herramienta E2E, manteniendo frameworks existentes para unitarias.
- **Activacion de skills expandida:** 18 nuevas entradas en las tablas de criterios de activacion (ambas agencias).
- **CI/CD Pipeline:** GitHub Actions completo para CI (lint, typecheck, tests, build, seguridad) y CD (despliegue Azure, migraciones, health check) en ambas agencias.
- **Flujo de desarrollo unificado:** `flujos/dev-flow-completo.md` en cada agencia con el ciclo completo especificacion -> planificacion -> desarrollo -> verificacion -> revision -> despliegue.
- **Flujos actualizados:** Todos los `flujos/` existentes ahora referencian CI/CD, Playwright y las nuevas skills.
- **Documentacion de arquitectura:** Este README actualizado con el estado completo del ecosistema.

---

## 9. Flujo de Desarrollo y CI/CD

Cada agencia tiene un **Flujo Completo de Desarrollo y CI/CD** documentado en `flujos/dev-flow-completo.md` que unifica el ciclo desde la especificacion hasta el despliegue.

### Ciclo de Vida Estandar

```
ESPECIFICACION -> PLANIFICACION -> DESARROLLO -> VERIFICACION -> REVISION -> DESPLIEGUE
                                                                                  |
                                                                           MONITOREO
```

### CI Pipeline (`.github/workflows/ci.yml`)

Se ejecuta en cada `push` y `pull_request` a `main`:

| Fase | Que valida |
|------|-----------|
| **Compuerta de Calidad** | Linter, TypeScript, Prisma validate |
| **Pruebas** | Unitarias, integracion (Playwright) y E2E con navegador real |
| **Build** | Backend + Frontend compilan |
| **Seguridad** | `npm audit` (vulnerabilidades) + TruffleHog (secretos expuestos) |

Para **proyectos existentes**, el CI se adapta:
- Detecta el framework de pruebas actual (Jest/Vitest/Mocha).
- Ejecuta pruebas existentes + Playwright E2E si se agrego.
- Si no hay CI preexistente, este pipeline se configura como el primero.

### CD Pipeline (`.github/workflows/deploy.yml`)

Se activa automaticamente cuando CI pasa en `main`:

```
CI verde en main
       |
       v
Autenticar Azure -> Validar/crear infraestructura -> Desplegar app -> Migraciones -> Health check -> Reporte
```

Para **proyectos nuevos**: el pipeline completo incluye Bicep y despliegue de backend + frontend.
Para **proyectos existentes**: el pipeline valida recursos existentes antes de crear, y se adapta al stack detectado.

### Flujos por agencia

| Agencia | Flujo completo | Archivos clave |
|---------|---------------|----------------|
| **Proyectos Desde 0** | `flujos/dev-flow-completo.md` | `crear-y-configurar-proyecto.md`, `desarrollo-incremental.md`, `desplegar-en-azure.md`, `.github/workflows/ci.yml`, `.github/workflows/deploy.yml` |
| **Proyectos Existentes** | `flujos/dev-flow-completo.md` | `analizar-y-continuar-proyecto.md`, `cambio-incremental.md`, `desplegar-en-azure.md`, `.github/workflows/ci.yml`, `.github/workflows/deploy.yml` |

### Reglas del flujo

1. No saltar fases: especificacion -> plan -> desarrollo -> verificacion -> revision -> despliegue.
2. CI debe pasar antes de hacer merge a main. Sin excepciones.
3. No desplegar sin CI verde. Si es urgente, documentar el riesgo y aprobacion humana.
4. E2E solo para flujos criticos. Lo demas con unitarias o integracion.
5. `ponytail` aplica en cada fase: preguntar si realmente se necesita.
6. Para proyectos existentes: la arquitectura actual prevalece, cambios reversibles, pruebas existentes deben seguir pasando.

---

## 10. Evolucion del Ecosistema

Este sistema de Agencias no es estatico. Esta disenado bajo una arquitectura modular:

1. **Nuevos Agentes:** Crearemos nuevos roles que necesiten acceso seguro a infraestructura u otras responsabilidades.
2. **Nuevos Modelos de Lenguaje:** La memoria persistente en Python (Cloud Mem / Mem Palace) permite desacoplarnos y escalar el contexto si cambiamos los LLMs subyacentes.
3. **Creador de Habilidades:** Las agencias tienen `creador-de-habilidades` / `creador-habilidades.md`, que permite a la IA redactar y estructurar nuevas *skills* en el formato correcto.
4. **SkillSpector:** Escaner de seguridad NVIDIA para validar skills antes de instalarlas (64+ patrones de vulnerabilidad).

> **Regla de oro:** Nunca mezcles el flujo de las agencias. Si el proyecto es nuevo, usa **Agencia_para_proyectos_desde_0**. Si el proyecto ya fue tocado por humanos u otras herramientas, respetelo y usa **Agencia_Proyectos_Existentes**.
