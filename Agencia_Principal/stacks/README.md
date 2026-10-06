# Sistema Multi-Stack Modular y Auto-Adaptable — Agencia Principal

Este directorio define la arquitectura y los contratos técnicos para la selección, ejecución y adaptación de perfiles tecnológicos en la **Agencia Principal**.

---

## 1. Principio de Resolución y Herencia

1. **Stack Predeterminado Oficial (`stacks/estandar/`)**:
   - Por defecto, toda nueva iniciativa creada con `python3 scripts/agencia.py nuevo <nombre>` utiliza este perfil.
   - Especifica de forma exhaustiva las reglas, dependencias, carpetas y contratos para **Node.js 22 LTS, Express.js, JavaScript moderno (ES Modules), PostgreSQL, Prisma ORM, React 18+ (JSX) y Tailwind CSS**.
   - Diseñado para máxima agilidad de desarrollo, sin sobrecargas ni fatiga de tipado de TypeScript.
   - Este estándar es **inmutable** frente a proyectos alternativos: nunca se sobreescribe ni se elimina al trabajar con otras tecnologías.

2. **Agnosticismo de Lenguaje y Perfiles Tecnológicos Alternativos (`stacks/alternativos/`)**:
   - La Agencia Principal es intrínsecamente agnóstica al lenguaje de programación: puede operar con JavaScript, Python, PHP, Go o cualquier tecnología requerida.
   - Cuando un proyecto específico requiera un ecosistema diferente (por ejemplo, `Laravel + Livewire + Alpine.js`, `FastAPI + Vue 3`, etc.), su definición vive en su propio subdirectorio bajo `stacks/alternativos/<id_stack>/`.
   - El proyecto específico vincula su `manifiesto.md` con este stack, indicando a los agentes especialistas (`agente-backend`, `agente-frontend`, `agente-base-datos`) que adopten dichos contratos exclusivamente para ese proyecto.

---

## 2. Capacidad de Auto-Adaptación ante Nuevas Tecnologías

Si al momento de plantear un requerimiento o crear un proyecto se solicita un stack no existente en `stacks/alternativos/`:

1. **Detección**: El Asistente Principal detecta que la tecnología solicitada no cuenta con perfil registrado.
2. **Generación Automática**: El agente orquestador genera automáticamente la carpeta `stacks/alternativos/<nombre-stack>/` utilizando la plantilla oficial `stacks/plantillas/nuevo-stack.md`.
3. **Documentación de Contratos**: Se investigan y formalizan las dependencias oficiales, la estructura recomendada de directorios, las convenciones de código y los comandos de prueba para esa tecnología.
4. **Asignación sin Impacto Global**: El nuevo proyecto se inicializa apuntando al nuevo stack sin alterar las reglas del stack estándar.

---

## 3. Catálogo de Stacks Disponibles

| Identificador | Descripción | Estado |
| :--- | :--- | :--- |
| `estandar` | Node.js 22 LTS, Express, JavaScript (ES Modules), PostgreSQL, Prisma, React (JSX), Tailwind CSS | Oficial (Predeterminado) |
| `laravel-livewire-alpine` | PHP 8.3+, Laravel 11/12, Livewire 3, Alpine.js, Tailwind CSS, ApexCharts | Alternativo (Soportado) |

