# Contrato Transversal de Agentes y Reglas Globales — Agencia Principal

Este documento establece las reglas obligatorias e inmutables que todo agente de inteligencia artificial (asistente principal, especialistas, revisores y evaluadores) debe acatar dentro de la **Agencia Principal**.

---

## 1. Regla Mandatoria de Idioma: Español Estricto
1. **Código y Persistencia**: Todas las variables, nombres de funciones, clases, métodos, tipos, interfaces, enums, modelos de Prisma/Base de datos, migraciones, semillas, endpoints y parámetros deben nombrarse en **español neutro**.
2. **Documentación y Comunicación**: Todos los comentarios de código, docstrings, mensajes de commit, logs de auditoría, bitácoras, historias de usuario, criterios de aceptación y reportes técnicos se redactan exclusivamente en español.
3. **Únicas Excepciones Permitidas**:
   - Palabras reservadas del lenguaje (`const`, `let`, `function`, `class`, `import`, `export`, `async`, `await`, etc.).
   - Convenciones inevitables de librerías externas o frameworks oficiales (`req`, `res`, `next`, `useState`, `useEffect`, etc.).
   - Protocolos y estándares de la industria (`HTTP`, `JSON`, `JWT`, `REST`, `SQL`).

---

## 2. FinOps de Contexto y Navegación Mandatoria por Grafos

> [!CAUTION]
> **PROHIBICIÓN RÍGIDA DE BÚSQUEDA CIEGA:**
> Queda terminantemente prohibido ejecutar búsquedas amplias e indiscriminadas de texto (`grep`, `find`, `rg`) o lecturas masivas de archivos a ciegas a través del repositorio sin haber consultado primero los grafos de conocimiento.

1. **Para consultas sobre código fuente, símbolos, jerarquía de llamadas y análisis de impacto**:
   - Se debe utilizar obligatoriamente **CodeGraph** antes de cualquier inspección en el sistema de archivos:
     - `codegraph explore <área>`: Exploración de área, símbolos relevantes y rutas de llamada.
     - `codegraph query <símbolo>`: Búsqueda rápida de símbolos y tipos.
     - `codegraph callers / callees <función>`: Trazabilidad de llamadas entrantes y salientes.
     - `codegraph impact <símbolo>`: Análisis de blast-radius antes de refactorizar.
2. **Para arquitectura conceptual, relaciones de módulos y dependencias de proyecto**:
   - Se debe consultar primero **Graphify** (`graphify query` o `graphify-out/graph.json`), inspeccionando las comunidades y los nodos centrales ("god nodes") para entender el flujo sin quemar tokens.
3. **Compresión Semántica (Headroom)**:
   - Toda salida extensa de terminal, traza de ejecución o diff de git debe comprimirse semánticamente con Headroom antes de ser reinyectada al contexto del LLM.

---

## 3. Filosofía Anti-Sobreingeniería (Ponytail & YAGNI)
Al refactorizar o escribir nuevo código, todo agente debe aplicar la jerarquía de `ponytail`:
1. **YAGNI absoluto**: Si una funcionalidad no fue solicitada explícitamente, no se implementa.
2. **Librería estándar sobre dependencias externas**: No añadir librerías para utilidades simples que resuelve la plataforma nativa.
3. **Dependencia ya instalada**: Si la dependencia ya existe en el proyecto, reutilizarla.
4. **Una línea clara antes que cinco abstracciones**: Evitar capas intermedias innecesarias o patrones de diseño que compliquen el entendimiento.
5. **Comentarios de simplificación**: Si se decide simplificar intencionalmente una solución, se debe marcar con el comentario `// ponytail: <justificación>`.

---

## 4. Gobernanza Multi-Stack y Resolución
1. **Stack Predeterminado**: La agencia asume por defecto el stack oficial especificado en `stacks/estandar/` (Node.js 22 LTS, Express.js, JavaScript moderno con ES Modules, PostgreSQL, Prisma ORM, React, Tailwind CSS), manteniendo la agencia intrínsecamente agnóstica a cualquier lenguaje.
2. **Stacks Alternativos**: Cuando un proyecto requiera tecnologías diferentes (ej. Laravel, Livewire, Alpine.js, FastAPI, Vue, etc.), la agencia consulta o genera un perfil en `stacks/alternativos/<nombre>/` sin alterar el estándar global.
3. **No Invención**: Todo requerimiento ambiguo se debe validar con el humano antes de asumir dependencias o cambios estructurales.

---

## 5. Compuertas Human-in-the-Loop (HITL) Obligatorias
El agente debe detenerse y ejecutar las alertas sonoras y visuales correspondientes en los siguientes escenarios:
- **`python3 scripts/solicitar_autorizacion.py --recurso "<descripción>"`**: Obligatorio antes de tocar archivos `.env`, borrar datos, ejecutar migraciones destructivas o realizar cambios con riesgo de seguridad. Reproduce 2x `Aprobación urgente..mp3` y registra en `.hitl_audit.jsonl`.
- **`python3 scripts/solicitar_validacion.py --preguntas "<pregunta>"`**: Obligatorio ante ambigüedad en requerimientos, decisiones de arquitectura abiertas o dudas de negocio. Reproduce 2x `Necesito Validación.mp3` y espera respuesta.
- **`python3 scripts/notificar_tarea.py --auto-completado --tarea "<resumen>"`**: Obligatorio una sola vez al finalizar completamente la tarea, justo antes de enviar la conclusión al humano. Reproduce 2x `termine la tarea.mp3`.

---

## 6. Ciclo de Iteraciones SDD y QA
1. **Ningún código sin especificación previa**: Toda implementación debe contar con Historias de Usuario (HU), Criterios de Aceptación (CA) y Casos de Prueba (CP) en formato Markdown.
2. **Validación estricta de QA**: El `ingeniero-de-pruebas` verifica la implementación con suites de Playwright o pruebas locales automatizadas con salida limpia (`exit code 0`).
3. **Límite de 5 loops**: Se permite un máximo de 5 iteraciones de corrección entre QA y Desarrollo. Si un fallo persiste en la quinta iteración, se detiene la ejecución y se escala al humano vía `solicitar_validacion.py`.
4. **Cierre por Evidencia**: Solo se declara completada una tarea cuando se cuenta con la salida real de pruebas (`exit code 0`).
