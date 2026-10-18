# Simplicidad obligatoria en backend y frontend (Ponytail)

Fuente canónica de la política de simplicidad para todo trabajo de desarrollo y revisión en la agencia (backend, base de datos y frontend). Los agentes, stacks, flujos y plantillas enlazan aquí; no copiar este contenido en otros documentos. La regla original de la skill está en [skills/ponytail/skills/ponytail/SKILL.md](../skills/ponytail/skills/ponytail/SKILL.md) y su revisión de sobreingeniería en [ponytail-review](../skills/ponytail/skills/ponytail-review/SKILL.md).

## Alcance y nivel
Ponytail permanece activa durante toda tarea de backend, persistencia y frontend:
- Nuevas funcionalidades y pantallas/vistas.
- Correcciones de errores y bugs.
- Refactorizaciones y optimizaciones.
- APIs, endpoints y contratos DTO.
- Casos de uso, servicios y lógica de aplicación.
- Modelos, esquemas, migraciones y consultas de base de datos.
- Componentes de UI, hooks, estado de cliente y navegación.
- Estilos, maquetación y adaptabilidad.
- Validaciones (servidor y cliente).
- Integraciones externas y clientes HTTP.
- Procesos programados y tareas en segundo plano.
- Pruebas automatizadas y comprobaciones.
- Configuración, dependencias e infraestructura.
- Decisiones de arquitectura técnica y visual.

Aplica obligatoriamente al agente backend, agente de base de datos, agente frontend, revisor de código, ingeniero de pruebas, analista de requerimientos, agente de arquitectura y subagentes que intervengan en el código.

Nivel predeterminado: **`full`**. Solo el asistente principal o el usuario pueden cambiarlo (`lite`, `ultra` u `off`) de forma expresa; el cambio se registra en la tarea y dura hasta que se indique otro nivel o termine la tarea.

## Escalera de decisión (antes de escribir o modificar código)
Detenerse en el primer peldaño que resuelve el requerimiento por completo:

1. **¿La funcionalidad, componente o abstracción realmente necesita existir?** Una necesidad hipotética o especulativa se omite y se informa en una línea (YAGNI).
2. **¿El proyecto ya cuenta con una solución, componente, hook o utilidad reutilizable?** Reutilizar antes que crear.
3. **¿La plataforma nativa o el framework base ya lo resuelven?**
   - *Backend/persistencia:* JavaScript estándar, Node.js stdlib, Express nativo, PostgreSQL (restricciones, tipos, índices) o Prisma.
   - *Frontend:* HTML5 semántico nativo (`<dialog>`, `<details>/<summary>`, inputs nativos como `type="date"`), CSS nativo / utilidades de Tailwind ya instaladas, JavaScript estándar o hooks elementales de React (`useState`, `useRef`).
4. **¿Una dependencia ya instalada resuelve correctamente la necesidad?** Usar lo disponible. Nunca instalar paquetes npm nuevos (librerías pesadas de componentes, librerías de fechas, carruseles, iconos duplicados, capas de estado complejas) para lo que unas pocas líneas o lo instalado resuelven.
5. **¿Se resuelve modificando pocas líneas o adaptando un componente/servicio existente?** Preferir el cambio más corto y localizado.
6. **Solo entonces, código nuevo.**
7. **Implementar la solución mínima que cumpla completamente el requerimiento.**

Un requerimiento expreso del usuario nunca se descarta en el peldaño 1: se implementa, y si existe una alternativa más simple se menciona en una sola línea.

## Reglas contra la sobreingeniería

El agente deberá evitar:
- Crear abstracciones, interfaces, fábricas o adaptadores con una sola implementación o sin necesidad real.
- Crear envoltorios artificiales (wrappers), Contexts/Providers o Higher-Order Components para un único caso de uso.
- Introducir stores globales (Zustand, Redux, Context global) cuando un estado local `useState` o parámetros en la URL (`searchParams`) bastan.
- Crear archivos, clases, componentes, servicios o utilidades únicamente para un posible uso futuro.
- Instalar dependencias para resolver algo que puede hacerse con funciones nativas o pocas líneas de código.
- Duplicar lógica, validaciones o estilos que ya existen en el proyecto.
- Construir sistemas genéricos de UI o arquitectura cuando solo se necesita resolver un caso concreto.
- Dividir una funcionalidad o pantalla pequeña entre demasiados archivos o micro-componentes prematuros.
- Aplicar patrones arquitectónicos únicamente por formalidad o protocolo.
- Preparar configuraciones, temas o extensiones que no han sido solicitados.
- Realizar refactorizaciones amplias cuando un cambio localizado resuelve correctamente el problema.
- Añadir complejidad técnica que no produzca un beneficio comprobable.

Siempre deberá preferirse:
- Reutilización antes que creación.
- Eliminación antes que adición.
- Código nativo antes que nuevas dependencias.
- Restricciones de base de datos antes que validaciones duplicadas en servidor.
- Controles HTML/CSS nativos antes que dependencias pesadas de UI.
- Soluciones directas antes que patrones innecesarios.
- Menos archivos cuando mantengan una separación clara de responsabilidades.
- Cambios pequeños, verificables y fáciles de revertir.
- Código entendible antes que implementaciones ingeniosas.

## Relación con la arquitectura

Ponytail no se utiliza para ignorar la arquitectura del proyecto, sino para evitar complejidad innecesaria dentro de la arquitectura aprobada:
- **Backend:** conserva la [arquitectura backend](../stacks/estandar/arquitectura-backend.md) modular por dominio, casos de uso independientes de Express/Prisma, validación en fronteras, seguridad, transacciones y roles. Pero no añade capas vacías, interfaces con una implementación ni archivos de dominio sin lógica reutilizada. Si basta ruta, controlador, caso de uso y repositorio existente, no se añaden más capas.
- **Frontend:** conserva la [arquitectura frontend modular por dominio](../stacks/estandar/arquitectura-frontend.md). Agrupa por módulo de negocio (componentes, hooks, servicios, contratos), pero **no obliga a crear carpetas ni archivos vacíos** (`store/`, `types/`, `hooks/`) si el módulo no los requiere. Los componentes locales permanecen en el mismo archivo hasta que su tamaño o reutilización justifique extraerlos.

## Aspectos que NUNCA deben simplificarse

Ponytail no podrá eliminar ni reducir indebidamente:
- Validación de entradas externas y datos de formularios en los límites de confianza.
- Autenticación, autorización, roles y permisos (con verificación obligatoria en servidor).
- Protección de información sensible, credenciales y secretos.
- Manejo de errores que evite pérdida de datos o estados bloqueados (estados de carga, error, vacío y éxito en cliente).
- Transacciones financieras e integridad referencial.
- Restricciones de base de datos.
- Auditoría y trazabilidad de operaciones importantes.
- Accesibilidad requerida (a11y: navegación por teclado, contraste suficiente, etiquetas/labels, foco visible, movimiento reducido).
- Pruebas esenciales de lógica no trivial.
- Requerimientos solicitados expresamente por el usuario.

La simplicidad debe reducir código innecesario, no reducir seguridad, calidad, accesibilidad ni confiabilidad.

## Pruebas mínimas obligatorias

Cada cambio que incluya condiciones, ciclos, procesamiento de datos, transformaciones complejas, cálculos monetarios, permisos, seguridad o reglas de negocio (tanto en backend como en frontend) deberá incorporar al menos una comprobación ejecutable con el runner del proyecto que falle si la funcionalidad deja de comportarse correctamente.

No deberán crearse suites extensas, configuraciones complejas ni pruebas redundantes cuando una prueba pequeña cubra el riesgo principal. Un cambio visual o trivial sin lógica no requiere prueba nueva.

## Registro de simplificaciones conscientes (`// ponytail:`)

Cuando se aplique una solución intencionalmente sencilla que tenga una limitación conocida, deberá documentarse mediante un comentario con el prefijo:

```js
// ponytail:
```

El comentario deberá indicar:
- Por qué la solución actual es suficiente.
- Cuál es su límite conocido.
- En qué situación real sería necesario ampliarla.

Ejemplos:
```js
// ponytail: consulta directa suficiente para el volumen actual;
// agregar paginación por cursor cuando el total supere el límite operativo definido.
```
```jsx
// ponytail: estado local con useState suficiente para este módulo;
// migrar a store compartido solo si otro módulo fuera de esta ruta necesita leerlo.
```

No deberán añadirse comentarios `ponytail` para justificar código trivial ni llenar los archivos con explicaciones innecesarias.

## Flujo de trabajo esperado (backend y frontend)

Para cada funcionalidad nueva o modificación, el agente deberá:
1. Leer el requerimiento.
2. Revisar la arquitectura y el código existente (usando CodeGraph primero cuando esté disponible).
3. Buscar una solución reutilizable dentro del proyecto.
4. Aplicar la escalera de decisión de Ponytail.
5. Determinar si la funcionalidad o componente es realmente necesario.
6. Proponer la solución mínima correcta.
7. Confirmar que respeta la arquitectura aprobada, la accesibilidad y las reglas del dominio.
8. Implementar el cambio con la menor cantidad razonable de archivos y código.
9. Ejecutar una comprobación proporcional al riesgo.
10. Documentar solamente las decisiones importantes.
11. Actualizar los grafos y la documentación cuando el cambio modifique la arquitectura o las relaciones del sistema.

## Preguntas de control
- ¿Esta funcionalidad o componente necesita existir?
- ¿Ya existe algo que pueda reutilizarse?
- ¿Puede resolverse con una capacidad nativa de la plataforma?
- ¿Necesitamos realmente una nueva dependencia?
- ¿La nueva abstracción o store tendrá más de un uso real?
- ¿Este archivo, capa o wrapper aporta valor?
- ¿La solución más corta también es segura, accesible y correcta?
- ¿Estamos resolviendo una necesidad actual o una posibilidad hipotética?

## Evidencia en la entrega y revisión de código

1. **En la entrega:** indicar nivel Ponytail aplicado, peldaño de la escalera donde se resolvió, qué se omitió y cuándo añadirlo, y la comprobación ejecutada.
2. **En la revisión de código:** el Revisor de Código incluye una pasada de sobreingeniería para cambios de backend y frontend con el formato de [ponytail-review](../skills/ponytail/skills/ponytail-review/SKILL.md) (`delete:`, `stdlib:`, `native:`, `yagni:`, `shrink:`), separada de la revisión de corrección funcional, accesibilidad y seguridad.
