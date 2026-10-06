# Guía Maestra: Cómo Iniciar y Desarrollar un Proyecto con la Agencia Principal

> **Para Desarrolladores y Asistentes de IA:** Esta guía es el protocolo definitivo paso a paso para arrancar cualquier proyecto de software desde cero en un repositorio nuevo donde se copia o integra la carpeta `Agencia_Principal`. Explica la estructura de carpetas, los comandos de inicio, el flujo de capas y los **prompts exactos para copiar y pegar en el chat de la IA** desde cualquier entorno (Cursor, Antigravity, Claude Code, Windsurf, VS Code, Gemini CLI u OpenCode).

---

## 1. Arquitectura del Repositorio: Dónde va la Agencia y Dónde va tu Código

Cuando creas un nuevo repositorio vacío en Git (ej. `mi-nuevo-proyecto`), la carpeta `Agencia_Principal` actúa como el **cerebro y motor de ingeniería**, mientras que la aplicación se construye a su lado.

### Estructura Recomendada (Directorio Raíz)

```txt
mi-nuevo-proyecto/                          # Raíz de tu repositorio Git
│
├── Agencia_Principal/                      # Carpeta de la agencia (Cerebro / Orquestador)
│   ├── asistente-principal.md             # Contrato maestro para la IA
│   ├── AGENTS.md                          # Reglas globales inmutables
│   ├── GUIA-INICIO-PROYECTO.md            # Esta guía
│   ├── scripts/                           # CLI operativa y motor MCP
│   ├── agentes/                           # Los 18 agentes especializados
│   ├── skills/                            # Habilidades técnicas (Prisma, Stitch, Clean Arch, etc.)
│   └── contexts/projects/                 # Memoria técnica persistente de cada proyecto
│
├── backend/                                # Tu aplicación Backend (Node.js 22 + TS + Express + Prisma)
│   ├── src/
│   ├── prisma/
│   ├── tests/
│   └── package.json
│
├── frontend/                               # Tu aplicación Frontend (React + TS + Tailwind + Vite)
│   ├── src/
│   ├── public/
│   └── package.json
│
├── .gitignore
└── README.md
```

> [!IMPORTANT]
> **Regla de Oro de Separación:**
> El código fuente de tu aplicación (`backend/`, `frontend/`, etc.) **NUNCA debe colocarse dentro de `Agencia_Principal/`**. La carpeta de la agencia sólo almacena su propio motor, agentes, skills y la memoria persistente en `contexts/projects/<nombre-del-proyecto>/`.

---

## 2. El Flujo de Trabajo en 5 Pasos Universales

```
[PASO 1: DIAGNÓSTICO & MEMORIA]
               │
               ▼
[PASO 2: BRAINSTORMING & PLAN EN ARTEFACTO] ──► (Compuerta Humana: Aprobación del Plan)
               │
               ▼
[PASO 3: ANDAMIAJE DEL PROYECTO (SCAFFOLD)]
               │
               ▼
[PASO 4: CONSTRUCCIÓN POR CAPAS CON TDD]
         ├── 4.1 Base de Datos & Prisma (agente-base-datos)
         ├── 4.2 Backend Clean Architecture (agente-backend)
         └── 4.3 Frontend con Alto Craft (agente-frontend + diseno-motion)
               │
               ▼
[PASO 5: QA, EVIDENCIA & CIERRE DE SESIÓN]
```

---

### Paso 1: Diagnóstico y Registro de Memoria (1 minuto)

Antes de escribir una sola línea de código, verifica que tu entorno local cuenta con las herramientas necesarias y registra el proyecto en la memoria de la agencia:

```bash
# 1. Situarse en la carpeta de la agencia
cd Agencia_Principal

# 2. Verificar que Python, Node, Git y linters estén en orden
python3 scripts/agencia.py doctor

# 3. Crear el registro y memoria del nuevo proyecto
python3 scripts/agencia.py nuevo mi-proyecto --cliente "Nombre Cliente o Propio" --tipo "nuevo"

# 4. Iniciar sesión y cargar el contexto inicial optimizado en tokens
python3 scripts/agencia.py arranque mi-proyecto --prime
```

*(Si utilizas un IDE con el servidor MCP `agencia` registrado, la IA ejecutará `agencia_doctor`, `agencia_nuevo` y `agencia_arranque` directamente).*

---

### Paso 2: Brainstorming y Plan de Implementación en Artefacto del IDE

1. **Apertura en el Chat de la IA:** Copia y pega el **Prompt Maestro 1** (véase la sección 3).
2. **Clarificación y Alcance:** La IA adoptará el rol de [analista-requerimientos.md](agentes/analista-requerimientos.md) y [asistente-principal.md](asistente-principal.md). Si tu requerimiento tiene partes ambiguas, te hará 2 o 3 preguntas concisas.
3. **Plan de Implementación Exclusivo en Artefacto:**
   - La IA redactará el plan detallado con historias de usuario, criterios de aceptación verificables y tareas atómicas (< 1 día).
   - **Cero Basura en el Workspace:** El plan **NO** se guarda en carpetas `docs/specs/` ni `plans/`. Se emite directamente como un **Artefacto interactivo del IDE** (`<appDataDir>/brain/<conversation-id>/plan_implementacion.md`).
4. **Compuerta Humana (HITL):** Revisa el plan en el visor de artefactos de tu IDE y responde *"Aprobado, procede con el Paso 3"* o solicita ajustes.

---

### Paso 3: Andamiaje (Scaffold) del Proyecto

Una vez aprobado el plan, la IA creará las carpetas y configuraciones base en la raíz del repositorio:

#### Backend (Node.js 22 + TypeScript + Express + Prisma):

```bash
# En la raíz del repositorio
mkdir backend && cd backend
npm init -y
npm install express dotenv cors helmet
npm install -D typescript ts-node-dev @types/express @types/node @types/cors jest @types/jest ts-jest prisma
npx tsc --init
npx prisma init --datasource-provider postgresql
```

#### Frontend (React + TypeScript + Vite + Tailwind CSS + Lucide + Sonner):

```bash
# En la raíz del repositorio
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm install lucide-react sonner zustand axios clsx tailwind-merge
npm install -D tailwindcss @tailwindcss/vite
```

---

### Paso 4: Construcción por Capas con TDD Estricto

Para evitar retrabajos y bugs, el desarrollo siempre sigue el orden de capas **Data-First**:

#### 4.1 Base de Datos Relacional ([agente-base-datos.md](agentes/agente-base-datos.md) + [GUIA-PRISMA-AGENCIA.md](skills/prisma-skills/GUIA-PRISMA-AGENCIA.md))

- Define los modelos en `backend/prisma/schema.prisma` con nombres descriptivos en español, claves foráneas e índices.
- Genera la migración aditiva: `npx prisma migrate dev --name init`.
- Crea un seed inicial con datos de prueba realistas en `backend/prisma/seed.ts`.
- Valida con `npx prisma validate`.

#### 4.2 Backend con Clean Architecture ([agente-backend.md](agentes/agente-backend.md) + [GUIA-CLEAN-ARCHITECTURE.md](skills/clean-architecture-skills/GUIA-CLEAN-ARCHITECTURE.md))

- **Ley de Hierro de TDD:**
  1. **Rojo:** Escribe primero el test del caso de uso en `backend/tests/` y confirma que falla (`npm test`).
  2. **Verde:** Implementa la lógica mínima en el caso de uso, repositorio y controlador Express.
  3. **Refactor:** Asegura tipado estricto (`tsc --noEmit`), manejo de excepciones de dominio y código limpio sin librerías innecesarias.

#### 4.3 Frontend con Alto Craft ([agente-frontend.md](agentes/agente-frontend.md) + [diseno-motion.md](agentes/diseno-motion.md) + [GUIA-EMILKOWALSKI.md](skills/emilkowalski-skills/GUIA-EMILKOWALSKI.md))

- Diseña componentes atómicos en `frontend/src/components/`.
- Aplica micro-interacciones fluidas (físicas elásticas, transiciones sutiles a 60 fps).
- Notificaciones de usuario con `sonner` (`toast.success()`, `toast.error()`).
- Gestión de estado global ligera con `zustand`.
- Cero colores genéricos o estilos planos de plantilla; diseño pulido y premium.

---

### Paso 5: QA, Pruebas y Cierre de Sesión

1. **Ejecución de Pruebas:**
   - La IA ejecuta las suites de backend y frontend comprobando el `exit code 0`.
   - Si surge algún error, la IA tiene un límite estricto de **5 loops de corrección** antes de consultar al humano.
2. **Verificación de Seguridad y Linters:**
   - [auditor-seguridad.md](agentes/auditor-seguridad.md) revisa que no haya variables `.env` o credenciales expuestas en Git.
3. **Cierre y Memoria:**
   ```bash
   python3 scripts/agencia.py cierre mi-proyecto --tareas "Módulo de usuarios y autenticación completado" --decisiones "Uso de Argon2 para hash de passwords" --notificar
   ```

   *(Esto actualiza la memoria persistente en `contexts/projects/mi-proyecto/memoria.md` y emite una alerta sonora en tu entorno).*

---

## 3. Prompts Maestros: Copiar y Pegar en el Chat de la IA

Usa estos prompts exactos en el chat de tu IDE según el momento del proyecto.

### 🌟 Prompt Maestro 1: Arranque de Proyecto Nuevo (Kickoff)

> Copia este texto en el primer mensaje de chat al abrir el repositorio:

```markdown
Hola. Estamos iniciando un nuevo proyecto en este repositorio. Actúa como el **Orquestador Principal de la Agencia** siguiendo estrictamente los lineamientos de @Agencia_Principal/asistente-principal.md y @Agencia_Principal/AGENTS.md.

**Detalles del Proyecto:**
- Nombre del Proyecto: [NOMBRE_DEL_PROYECTO, ej: mi-saas-facturacion]
- Objetivo y Requerimientos: [DESCRIBE AQUÍ TU PROYECTO O PEGA TU ESPECIFICACIÓN]

**Tus Instrucciones Inmediatas:**
1. Ejecuta el diagnóstico de herramientas (`doctor`) y registra la memoria del proyecto con `nuevo_proyecto.py` o los comandos MCP correspondientes.
2. Si algún requisito es ambiguo, hazme un máximo de 3 preguntas breves para clarificar.
3. Genera el Plan de Implementación Paso a Paso con historias de usuario y tareas atómicas.
4. **REGLA MANDATORIA DE CERO BASURA:** Presenta el plan EXCLUSIVAMENTE como un **Artefacto interactivo del IDE**. No crees carpetas como `docs/specs/` ni archivos sueltos de notas en el repositorio.
5. Detén tu ejecución y espera mi aprobación del plan antes de crear archivos de código.
```

---

### 🔄 Prompt Maestro 2: Reanudar Sesión de Trabajo (Siguiente Tarea)

> Úsalo cuando abras un nuevo chat o continúes el desarrollo al día siguiente:

```markdown
Continuamos el desarrollo de [NOMBRE_DEL_PROYECTO]. Actúa como el Orquestador Principal siguiendo @Agencia_Principal/asistente-principal.md.

Por favor:
1. Carga la memoria del proyecto (`python3 scripts/agencia.py arranque [NOMBRE_DEL_PROYECTO] --prime` o MCP `agencia_arranque`).
2. Revisa el estado actual del código y la última tarea completada.
3. Muéstrame en un breve resumen el próximo paso a ejecutar según el plan y consúltame si procedemos con él.
```

---

### 🚀 Prompt Maestro 3: Construcción de una Nueva Funcionalidad (Feature)

> Úsalo cuando vayas a implementar una nueva funcionalidad:

```markdown
Vamos a implementar la siguiente funcionalidad en [NOMBRE_DEL_PROYECTO]:
"[DESCRIBE LA FEATURE AQUÍ]"

Sigue los lineamientos de @Agencia_Principal/asistente-principal.md:
1. Aplica la Ley de Hierro de TDD (The Iron Law): escribe primero los tests unitarios/integración en rojo.
2. Si requiere base de datos, delega en @Agencia_Principal/agentes/agente-base-datos.md y actualiza Prisma.
3. En backend, aplica Clean Architecture con @Agencia_Principal/agentes/agente-backend.md.
4. En frontend, aplica diseño con alto craft y micro-interacciones con @Agencia_Principal/agentes/agente-frontend.md y @Agencia_Principal/agentes/diseno-motion.md.
5. Todo el código, variables, comentarios y logs deben estar en español técnico neutro.
6. Demuestra evidencia de ejecución exitosa (`exit code 0`) antes de dar la tarea por finalizada.
```

---

### 🔒 Prompt Maestro 4: Auditoría de Calidad y Cierre de Fase

> Úsalo al finalizar un hito o antes de hacer commit:

```markdown
Hemos terminado las tareas de esta fase. Por favor, ejecuta el protocolo de cierre:
1. Delega en @Agencia_Principal/agentes/ingeniero-de-pruebas.md para ejecutar toda la suite de pruebas.
2. Delega en @Agencia_Principal/agentes/auditor-seguridad.md y @Agencia_Principal/agentes/revisor-de-codigo.md para auditar linting, tipos TypeScript y seguridad (sin `.env` comiteados).
3. Si todo está verde, registra el cierre con `python3 scripts/agencia.py cierre [NOMBRE_DEL_PROYECTO] --tareas "[RESUMEN_TAREAS]"` y notifícame.
```

---

## 4. Preguntas Frecuentes y Solución de Problemas (FAQ)

### ¿Qué hago si la IA empieza a crear carpetas de código dentro de `Agencia_Principal/`?

Recuérdale de inmediato:

> *"La carpeta `Agencia_Principal` es sólo el orquestador y la memoria. El código del proyecto va en la raíz del repositorio (`backend/`, `frontend/`). Mueve los archivos a la ubicación correcta."*

### ¿Qué hago si la IA intenta crear archivos `.md` de planes en el repositorio?

La agencia prohíbe taxativamente la basura documental. Dile:

> *"Recuerda la regla de Cero Basura en el Workspace de `asistente-principal.md`. Todos los planes y especificaciones deben ser emitidos como Artefactos del IDE, no como archivos en el repositorio."*

### ¿Cómo sabe la IA qué herramientas usar en mi IDE?

`asistente-principal.md` cuenta con una **Matriz de Ejecución Multi-Harness**:

1. Si el servidor MCP `agencia` está activo, usará herramientas como `agencia_arranque` y `agencia_doctor`.
2. Si cuenta con herramientas nativas de IDE (`ask_question`, generador de artefactos), las prioriza.
3. Si sólo tiene terminal bash, ejecutará directamente `python3 scripts/agencia.py <comando>`.

---

## 5. Resumen de Referencias Rápidas

| Necesidad                                 | Documento de Consulta                                                                                                     |
| :---------------------------------------- | :------------------------------------------------------------------------------------------------------------------------ |
| **Orquestación Global y Fases**    | [asistente-principal.md](asistente-principal.md)                                                                           |
| **Reglas Globales e Idioma**        | [AGENTS.md](AGENTS.md)                                                                                                     |
| **Metodología y Artefactos**       | [reglas/metodologia-superpowers-artefactos.md](reglas/metodologia-superpowers-artefactos.md)                               |
| **Guía de Prisma ORM**             | [skills/prisma-skills/GUIA-PRISMA-AGENCIA.md](skills/prisma-skills/GUIA-PRISMA-AGENCIA.md)                                 |
| **Guía de Google Stitch**          | [skills/stitch-skills/GUIA-STITCH-AGENCIA.md](skills/stitch-skills/GUIA-STITCH-AGENCIA.md)                                 |
| **Guía de Clean Architecture**     | [skills/clean-architecture-skills/GUIA-CLEAN-ARCHITECTURE.md](skills/clean-architecture-skills/GUIA-CLEAN-ARCHITECTURE.md) |
| **Guía de Micro-interacciones UI** | [skills/emilkowalski-skills/GUIA-EMILKOWALSKI.md](skills/emilkowalski-skills/GUIA-EMILKOWALSKI.md)                         |
| **Flujo de Proyecto Nuevo**         | [flujos/proyecto-nuevo.md](flujos/proyecto-nuevo.md)                                                                       |
