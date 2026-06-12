# Agencia Universal para Proyectos Existentes

## Proposito
Esta agencia esta disenada para continuar, mantener y mejorar proyectos que ya existen. Su regla principal es comprender primero el sistema actual y despues aplicar cambios pequenos, trazables y compatibles con la arquitectura, tecnologia, base de datos, reglas de negocio y convenciones ya definidas.

No impone un stack, framework, ORM, metodologia ni estructura de carpetas. Si el proyecto ya funciona con una arquitectura definida, los agentes deben conservarla salvo que exista una razon tecnica clara, documentada y validada para cambiarla.

## Estructura

```txt
Agencia_Proyectos_Existentes/
├── README.md
├── asistente-principal.md
├── agentes/
├── skills/
├── context/
├── guias/
├── flujos/
├── plantillas/
├── reglas/
├── proyectos/
├── scripts/
└── compatibilidad-ia/
```

## Carpetas principales

| Carpeta | Proposito |
| --- | --- |
| `agentes/` | Define roles especializados, responsabilidades, entradas, salidas, limites y criterios de uso. |
| `skills/` | Define habilidades reutilizables que pueden combinarse con agentes segun el tipo de tarea. |
| `context/` | Guarda guias para leer, resumir y conservar informacion del proyecto existente. |
| `guias/` | Explica como seleccionar agentes, skills y combinaciones recomendadas. |
| `flujos/` | Documenta flujos de trabajo para analizar, modificar, revisar, probar y cerrar cambios. |
| `plantillas/` | Incluye formatos base para nuevos agentes, nuevas skills, requerimientos, auditorias y bitacoras. |
| `reglas/` | Contiene reglas generales para preservar arquitectura, decidir cambios y evitar modificaciones innecesarias. |
| `proyectos/` | Contiene proyectos independientes, cada uno con su propia memoria contextual en `.memoria/`. |
| `scripts/` | Herramientas operativas de la agencia, incluida la memoria independiente por proyecto. |
| `compatibilidad-ia/` | Lineamientos para usar la agencia con Codex, Claude, Gemini, GitHub Copilot u otras IA. |

## Principios obligatorios
1. Leer antes de modificar.
2. Respetar la arquitectura existente.
3. Cambiar solo lo necesario para cumplir el objetivo.
4. Reutilizar patrones, nombres, carpetas, librerias y convenciones locales.
5. No instalar dependencias ni introducir frameworks sin justificacion.
6. Documentar decisiones que alteren arquitectura, base de datos, seguridad o reglas de negocio.
7. Validar con pruebas o verificacion manual segun el riesgo.
8. Mantener trazabilidad de archivos afectados, decisiones, riesgos y pendientes.

## Uso rapido
1. Inicia con [`asistente-principal.md`](asistente-principal.md).
2. Aplica [`context/lectura-proyecto-existente.md`](context/lectura-proyecto-existente.md) para entender el repositorio.
3. Selecciona agentes con [`guias/criterios-activacion-agentes.md`](guias/criterios-activacion-agentes.md).
4. Selecciona skills con [`guias/criterios-activacion-skills.md`](guias/criterios-activacion-skills.md).
5. Sigue el flujo apropiado en `flujos/`.
6. Cierra con documentacion usando las plantillas de `plantillas/`.

## Memoria por proyecto
Cada proyecto debe vivir en `proyectos/<nombre-proyecto>/` y tener memoria propia en `proyectos/<nombre-proyecto>/.memoria/`.

Para crear un proyecto desde la plantilla:

```bash
cp -R proyectos/_plantilla_proyecto proyectos/mi-proyecto
python3 scripts/memoria_proyecto.py --proyecto proyectos/mi-proyecto init
```

Antes de trabajar:

```bash
python3 scripts/memoria_proyecto.py --proyecto proyectos/mi-proyecto start
```

Despues de cambios importantes:

```bash
python3 scripts/memoria_proyecto.py --proyecto proyectos/mi-proyecto close \
  --tareas "Cambios realizados" \
  --pendientes "Pendientes" \
  --decisiones "Decisiones tecnicas" \
  --riesgos "Riesgos" \
  --cloud-resumen "Resumen operativo" \
  --archivos "archivo.md"
```

## Contenido Actual del Proyecto

A continuación se lista un resumen de los recursos disponibles actualmente en esta agencia:

### 🤖 Agentes Disponibles (`agentes/`)
- **Análisis y Arquitectura:** `agente-analisis-proyecto-existente`, `agente-arquitectura`, `analista-requerimientos`, `agente-contexto`.
- **Desarrollo:** `agente-backend`, `agente-frontend`, `agente-base-datos`, `agente-desarrollo`, `engineer`.
- **Mantenimiento y Calidad:** `agente-mantenimiento`, `agente-refactorizacion`, `agente-integracion`, `code-reviewer`, `security-editor`, `tester`, `agente-documentacion`.

# Agencia Universal para Proyectos Existentes

## Proposito
Esta agencia esta disenada para continuar, mantener y mejorar proyectos que ya existen. Su regla principal es comprender primero el sistema actual y despues aplicar cambios pequenos, trazables y compatibles con la arquitectura, tecnologia, base de datos, reglas de negocio y convenciones ya definidas.

No impone un stack, framework, ORM, metodologia ni estructura de carpetas. Si el proyecto ya funciona con una arquitectura definida, los agentes deben conservarla salvo que exista una razon tecnica clara, documentada y validada para cambiarla.

## Estructura

```txt
Agencia_Proyectos_Existentes/
├── README.md
├── asistente-principal.md
├── agentes/
├── skills/
├── context/
├── guias/
├── flujos/
├── plantillas/
├── reglas/
├── proyectos/
├── scripts/
└── compatibilidad-ia/
```

## Carpetas principales

| Carpeta | Proposito |
| --- | --- |
| `agentes/` | Define roles especializados, responsabilidades, entradas, salidas, limites y criterios de uso. |
| `skills/` | Define habilidades reutilizables que pueden combinarse con agentes segun el tipo de tarea. |
| `context/` | Guarda guias para leer, resumir y conservar informacion del proyecto existente. |
| `guias/` | Explica como seleccionar agentes, skills y combinaciones recomendadas. |
| `flujos/` | Documenta flujos de trabajo para analizar, modificar, revisar, probar y cerrar cambios. |
| `plantillas/` | Incluye formatos base para nuevos agentes, nuevas skills, requerimientos, auditorias y bitacoras. |
| `reglas/` | Contiene reglas generales para preservar arquitectura, decidir cambios y evitar modificaciones innecesarias. |
| `proyectos/` | Contiene proyectos independientes, cada uno con su propia memoria contextual en `.memoria/`. |
| `scripts/` | Herramientas operativas de la agencia, incluida la memoria independiente por proyecto. |
| `compatibilidad-ia/` | Lineamientos para usar la agencia con Codex, Claude, Gemini, GitHub Copilot u otras IA. |

## Principios obligatorios
1. Leer antes de modificar.
2. Respetar la arquitectura existente.
3. Cambiar solo lo necesario para cumplir el objetivo.
4. Reutilizar patrones, nombres, carpetas, librerias y convenciones locales.
5. No instalar dependencias ni introducir frameworks sin justificacion.
6. Documentar decisiones que alteren arquitectura, base de datos, seguridad o reglas de negocio.
7. Validar con pruebas o verificacion manual segun el riesgo.
8. Mantener trazabilidad de archivos afectados, decisiones, riesgos y pendientes.

## Uso rapido
1. Inicia con [`asistente-principal.md`](asistente-principal.md).
2. Aplica [`context/lectura-proyecto-existente.md`](context/lectura-proyecto-existente.md) para entender el repositorio.
3. Selecciona agentes con [`guias/criterios-activacion-agentes.md`](guias/criterios-activacion-agentes.md).
4. Selecciona skills con [`guias/criterios-activacion-skills.md`](guias/criterios-activacion-skills.md).
5. Sigue el flujo apropiado en `flujos/`.
6. Cierra con documentacion usando las plantillas de `plantillas/`.

## Memoria por proyecto
Cada proyecto debe vivir en `proyectos/<nombre-proyecto>/` y tener memoria propia en `proyectos/<nombre-proyecto>/.memoria/`.

Para crear un proyecto desde la plantilla:

```bash
cp -R proyectos/_plantilla_proyecto proyectos/mi-proyecto
python3 scripts/memoria_proyecto.py --proyecto proyectos/mi-proyecto init
```

Antes de trabajar:

```bash
python3 scripts/memoria_proyecto.py --proyecto proyectos/mi-proyecto start
```

Despues de cambios importantes:

```bash
python3 scripts/memoria_proyecto.py --proyecto proyectos/mi-proyecto close \
  --tareas "Cambios realizados" \
  --pendientes "Pendientes" \
  --decisiones "Decisiones tecnicas" \
  --riesgos "Riesgos" \
  --cloud-resumen "Resumen operativo" \
  --archivos "archivo.md"
```

## Contenido Actual del Proyecto

A continuación se lista un resumen de los recursos disponibles actualmente en esta agencia:

### 🤖 Agentes Disponibles (`agentes/`)
- **Análisis y Arquitectura:** `agente-analisis-proyecto-existente`, `agente-arquitectura`, `analista-requerimientos`, `agente-contexto`.
- **Desarrollo:** `agente-backend`, `agente-frontend`, `agente-base-datos`, `agente-desarrollo`, `engineer`.
- **Mantenimiento y Calidad:** `agente-mantenimiento`, `agente-refactorizacion`, `agente-integracion`, `code-reviewer`, `security-editor`, `tester`, `agente-documentacion`.

### 🧠 Skills Principales (`skills/`)
- **Adaptación al Entorno:** `adaptacion-proyectos-existentes`, `conservacion-estructura-actual`, `lectura-arquitectura-existente`, `ahorro-contexto`, `contextos`.
- **Desarrollo Técnico:** `backend-dominio-limpio`, `ui-ux-pro-max`, `refactorizacion-controlada`, `seguridad`, `testing`.
- **Análisis y Comunicación:** `analisis-requerimientos`, `interview`, `spec-driven-development`, `comunicacion-espanol`, `respuestas-simples`.
- **Documentación y Cierre:** `documentacion-tecnica`, `revision-codigo`, `creador-habilidades`, `referrals`.

### 🔄 Flujos de Trabajo (`flujos/`)
- `analizar-y-continuar-proyecto.md`: Pasos para retomar un repositorio que ya tiene historia.
- `cambio-incremental.md`: Para añadir features poco a poco sin romper el sistema.
- `refactorizacion-controlada.md`: Mejorar código técnico de manera segura.
- `revision-y-cierre.md`: Pasos requeridos para dar por concluida una tarea.

## ¿Cómo Funciona la Estructura? (Arquitectura de Ejecución)

El repositorio está diseñado como un ecosistema modular donde los diferentes elementos se combinan de forma dinámica para resolver cualquier requerimiento respetando la arquitectura preexistente del proyecto. El funcionamiento general sigue este ciclo:

1. **Recepción del Requerimiento:** El `asistente-principal` analiza la tarea solicitada y el código base actual.
2. **Selección del Agente:** Se asigna el rol o perfil que va a liderar el trabajo (ej. `agente-frontend` si es un cambio visual, o `agente-backend` si es un endpoint de API).
3. **Inyección de Skills (Habilidades):** El Agente es por sí solo un perfil genérico. Para especializarlo, se "activan" las *Skills* leyendo sus archivos `.md`. Por ejemplo, si se va a modificar la interfaz, se inyecta la skill `ui-ux-pro-max`; si hay riesgo de romper la lógica, se inyecta `seguridad` y `backend-dominio-limpio`.
4. **Ejecución Guiada:** El Agente operará bajo las reglas estrictas definidas por las Skills activadas, procesando la tarea mediante un **Flujo de Trabajo** predefinido (ej. un `cambio-incremental`).
5. **Memoria y Cierre:** Se utiliza la skill `ahorro-contexto` y el script de la memoria para persistir todos los cambios realizados, las decisiones técnicas y los pendientes en la carpeta `.memoria/` de cada proyecto específico.
