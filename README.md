# 🧠 Skill Team - Sistema de Agencias de IA

Bienvenido al repositorio central de nuestras **Agencias de IA**. Este documento sirve como la guía principal para los desarrolladores, arquitectos y mantenedores del equipo. 

Aquí documentamos cómo está estructurado nuestro ecosistema de asistentes, para qué sirve cada "Agencia" (entornos de desarrollo de IA) y cómo colaboran las diferentes *skills* (habilidades) para crear, mantener y diseñar software.

---

## 🏗️ Arquitectura General

Hemos dividido nuestras capacidades de Inteligencia Artificial en entornos aislados o **Agencias**. Cada agencia cuenta con un Asistente Principal (Orquestador), agentes especializados y una carpeta de *skills* con reglas estrictas.

La división principal obedece a la etapa del ciclo de vida del software en la que se va a trabajar:

1. **`Agencia_para_proyecotos_desde_0`**: Para software nuevo (*Greenfield*).
2. **`Agencia_Proyectos_Existentes`**: Para mantenimiento y evolución (*Brownfield*).
3. **`Agencia`**: Para flujos de diseño e iteraciones visuales.

A continuación, detallamos exhaustivamente cada una.

---

## 1. 🚀 Agencia para Proyectos Desde 0
**Carpeta:** `/Agencia_para_proyecotos_desde_0`

### ¿Para qué sirve?
Es la agencia constructora. Está diseñada exclusivamente para **analizar, definir, planificar y programar proyectos totalmente nuevos**. 
Asume que no hay deuda técnica y tiene libertad para implementar nuestra arquitectura estándar desde el primer commit.

### Flujo y Arquitectura
- **Levantamiento inicial:** El Asistente Principal entrevista al usuario y define la arquitectura.
- **Estándares rigurosos:** Se aplica Node.js, Express, TypeScript, PostgreSQL y Prisma en el backend (Clean Architecture); y React, Tailwind, Zustand en frontend (Atomic Design).
- **Memoria persistente:** Utiliza sistemas de *Cloud Mem* para frontend visual y *Mem Palace* para secretos, reglas de negocio y bases de datos sensibles.

### Skills Principales Inyectadas
Esta agencia posee directorios de skills profundos, enfocados en construir correctamente:
- `backend-dominio-limpio`: Asegura que se respeten los casos de uso, repositorios y puertos de Clean Architecture.
- `prisma-base-de-datos`: Manejo exclusivo de esquemas Prisma, migraciones, transacciones seguras y semilleros.
- `ui-ux-pro-max`: Estandariza la creación de componentes visuales altamente estéticos, accesibles y modulares.
- `ahorro-contexto`: Scripts en Python para inicializar la memoria, recuperar contexto y hacer cierres eficientes sin perder historial.
- `commits-espanol`: Regla estricta para que el control de versiones quede trazable y documentado en español.
- `ponytail`: *Ver sección de Ponytail.*

---

## 2. 🛡️ Agencia de Proyectos Existentes
**Carpeta:** `/Agencia_Proyectos_Existentes`

### ¿Para qué sirve?
Es la agencia auditora y mantenedora. Está orientada a **analizar, mantener, refactorizar y escalar proyectos que ya poseen un historial de código, reglas de equipo y deuda técnica**.

### Flujo y Arquitectura
- **Auditoría antes de acción:** Su regla maestra es "la arquitectura existente prevalece". No impone tecnologías genéricas si el proyecto ya funciona de otra forma.
- **Incrementos seguros:** Lee la arquitectura, detecta convenciones y realiza cambios incrementales, asegurándose de no romper código en producción.
- **Memoria aislada:** Cada proyecto gestionado bajo esta agencia requiere su propia carpeta `.memoria/` para evitar que un proyecto contamine a otro.

### Skills Principales Inyectadas
Esta agencia posee un abanico mucho más amplio de *skills* (muchas de ellas atómicas en archivos `.md`), pensadas para tareas específicas de mantenimiento:
- `lectura-arquitectura-existente` y `conservacion-estructura-actual`: Fuerzan a los agentes a leer y respetar los patrones antes de proponer cambios.
- `refactorizacion-controlada`: Guía paso a paso para mejorar código viejo sin alterar el comportamiento.
- `revision-codigo` y `seguridad`: Skills para revisar *pull requests*, auditar vulnerabilidades y analizar requerimientos.
- `ui-ux-pro-max`: Adaptada para modernizar interfaces sin romper la lógica del DOM existente.
- `ponytail`: *Ver sección de Ponytail.*

---

## 3. 🎨 Agencia de Diseño y Frontend
**Carpeta:** `/Agencia`

### ¿Para qué sirve?
Es un entorno especializado y aislado, enfocado puramente en el diseño visual y el prototipado rápido de interfaces. 

### Flujo y Arquitectura
- **Separación de responsabilidades:** Contiene flujos específicos (`diseños-frontend`) para abstraerse de la complejidad de servidores, bases de datos o lógica de negocio.
- **Iteración Visual:** Úsala para maquetar, refinar animaciones, ajustar CSS/Tailwind y estructurar componentes de UI antes de conectarlos a un backend real.

---

## 🐴 El rol de Ponytail (Skill Transversal)

**Ponytail** es el "senior dev flojo". Es una de las habilidades más importantes que comparten nuestras agencias.

### ¿Qué hace?
Enseña a la IA a escribir el **mínimo código posible**. Fuerza el principio *YAGNI* (*You Aren't Gonna Need It*), priorizando la biblioteca estándar o APIs nativas del navegador antes de crear abstracciones complejas o instalar nuevas dependencias de NPM.

### ¿Cómo interactúa Ponytail con cada Agencia?
- **En `Agencia_para_proyecotos_desde_0`**: Ponytail actúa en el andamiaje (*scaffolding*). Antes de programar, pregunta qué IDE usa el desarrollador (Cursor, Windsurf, Copilot, etc.) y le inyecta las reglas de minimalismo de Ponytail a ese IDE. Desde el día 1, el proyecto nace sin código inútil.
- **En `Agencia_Proyectos_Existentes`**: Actúa como un consultor respetuoso. Inspecciona si el repositorio *legacy* ya tiene reglas de código (como `.cursorrules`). Si las hay, las respeta y se fusiona progresivamente sin destruir las políticas de arquitectura estrictas que el equipo original estableció.

---

## 🚀 Evolución del Ecosistema

Este sistema de Agencias no es estático. Está diseñado bajo una arquitectura modular:
1. **Nuevos Agentes:** Crearemos nuevos roles que necesiten acceso seguro a infraestructura u otras responsabilidades.
2. **Nuevos Modelos de Lenguaje:** La memoria persistente en Python (Cloud Mem / Mem Palace) nos permite desacoplarnos y escalar el contexto si cambiamos los LLMs subyacentes.
3. **Creador de Habilidades:** Nuestras agencias tienen una skill llamada `creador-de-habilidades` / `creador-habilidades.md`, la cual le permite a la propia IA ayudar a redactar y estructurar nuevas *skills* en el formato correcto para el ecosistema.

> **Regla de oro para desarrolladores:** Nunca mezcles el flujo de las agencias. Si el proyecto es nuevo, usa la **Agencia 0**. Si el proyecto ya fue tocado por humanos u otras herramientas, respétalo y usa la **Agencia Existentes**.
