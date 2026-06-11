# Propuesta Unificada de Agencia de Agentes de Desarrollo SMT

Este documento define la gobernanza tecnica, la arquitectura global, el flujo de trabajo y las reglas de memoria persistente para la agencia de agentes de desarrollo de **SMT (Soluciones de Movilidad Terrestre)**. Es la referencia obligatoria para el asistente principal, agentes especialistas, skills tecnicas, documentacion, desarrollo, pruebas y validacion con el humano.

---

## 1. Resumen ejecutivo de la agencia de agentes

La agencia de agentes funciona como un sistema coordinado por un **asistente principal** que actua como orquestador, arquitecto de software y gestor de coherencia. El asistente principal es el punto de entrada unico con el humano, clasifica la tarea, recupera contexto, selecciona agentes y skills, define entregables, valida avances y cierra la sesion con memoria persistente.

El objetivo es evitar decisiones tecnicas contradictorias entre frontend, backend, base de datos, diseno, pruebas y documentacion. Todo desarrollo debe mantenerse en espanol y respetar Clean Architecture, Clean Code, dominio limpio, arquitectura hexagonal, bajo acoplamiento, alta cohesion, modularidad, trazabilidad y validacion continua con el humano.

---

## 2. Arquitectura global propuesta

La arquitectura global se divide en tres frentes tecnicos integrados:

1. **Backend:** Node.js 22 LTS, Express.js, TypeScript, PostgreSQL y Prisma. Debe organizarse por modulos de negocio con separacion entre dominio, aplicacion, infraestructura e interfaces HTTP.
2. **Frontend:** React, TypeScript, Tailwind CSS, Lucide React, Sonner, Zustand, Axios y React Router DOM. Debe aplicar Atomic Design en `components` y arquitectura modular en `modules`.
3. **Base de datos:** PostgreSQL como motor definitivo y Prisma como ORM obligatorio. El acceso a datos se encapsula en repositorios de infraestructura y queda prohibido acoplar controladores o casos de uso directamente a Prisma.

La estructura debe ser simple, entendible y escalable. Se evita agregar frameworks, patrones o herramientas no aprobadas cuando no resuelvan una necesidad real.

---

## 3. Reglas tecnicas obligatorias

Todo agente debe cumplir estas reglas:

- El idioma del proyecto es espanol para documentacion, carpetas, archivos, variables, funciones, clases, interfaces, tipos, comentarios, logs, mensajes visuales, historias de usuario, casos de prueba, semillas y modelos de datos.
- Solo se permite ingles cuando sea obligatorio por sintaxis del lenguaje, palabras reservadas, dependencias, APIs externas, convenciones inevitables de framework o nombres oficiales de librerias.
- Backend obligatorio: Node.js 22 LTS, Express.js, TypeScript, PostgreSQL y Prisma.
- Frontend obligatorio: React, TypeScript, Tailwind CSS, Lucide React, Sonner, Zustand, Axios y React Router DOM.
- No se permite SQL Server, Knex ni consultas SQL crudas como criterio normal del proyecto.
- No se permite TanStack Query como dependencia base salvo aprobacion explicita del humano y justificacion documentada.
- PrismaClient solo puede vivir en infraestructura/repositorios. Ningun controlador, ruta o componente visual puede invocar Prisma.
- Todo cambio estructural debe quedar documentado y validado con el humano cuando afecte arquitectura, base de datos, reglas de negocio o seguridad.

Dependencias base obligatorias del backend:

```json
"devDependencies": {
  "@types/bcryptjs": "^2.4.2",
  "@types/cors": "^2.8.13",
  "@types/express": "^4.17.17",
  "@types/jsonwebtoken": "^9.0.2",
  "@types/node": "^20.19.39",
  "@types/pg": "^8.20.0",
  "prisma": "^7.8.0",
  "ts-node-dev": "^2.0.0",
  "typescript": "^5.1.6"
}
```

Dependencias base obligatorias del frontend:

```json
"dependencies": {
  "axios": "^1.6.0",
  "lucide-react": "^0.300.0",
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-router-dom": "^6.20.0",
  "sonner": "^2.0.7",
  "zustand": "^4.4.7"
}
```

---

## 4. Agentes definidos y responsabilidades

La agencia debe contar como minimo con estos agentes:

| Agente | Responsabilidad | Entregables |
| --- | --- | --- |
| Asistente principal | Orquestar el flujo, hacer preguntas, seleccionar agentes y skills, validar coherencia y cerrar sesion. | Plan de trabajo, asignacion de agentes, criterios de validacion y cierre documentado. |
| Agente de levantamiento de requerimientos | Convertir informacion cruda del humano en requerimientos, historias de usuario, alcance, restricciones y reglas de negocio. | Requerimientos funcionales/no funcionales, historias de usuario y criterios de aceptacion. |
| Agente de desarrollo | Construir backend, frontend e integraciones respetando arquitectura global. | Codigo TypeScript, modulos, componentes, servicios API y documentacion tecnica. |
| Agente de testeo | Validar que el sistema cumpla requerimientos, historias, reglas de negocio y criterios de aceptacion. | Casos de prueba, resultados, evidencias y retroalimentacion al desarrollo. |
| Agente de diseno | Mantener coherencia visual, Atomic Design, accesibilidad basica y experiencia clara. | Sistema de diseno, componentes base y criterios UI/UX aplicados. |
| Agente de base de datos | Disenar modelos, migraciones, semillas, relaciones, restricciones e integridad referencial con Prisma/PostgreSQL. | `schema.prisma`, migraciones, semillas y repositorios alineados al dominio. |
| Agente de documentacion | Mantener trazabilidad de decisiones, cambios, riesgos, pendientes y entregables. | Documentacion tecnica, ADRs, bitacoras y reportes de cierre. |

---

## 5. Flujo de comunicacion entre agentes

El flujo inicia siempre con el asistente principal:

1. El humano plantea una necesidad.
2. El asistente principal clasifica el tipo de tarea y determina la herramienta de memoria persistente.
3. Si el contexto no esta claro, el asistente principal pregunta hasta definir alcance, herramientas, agentes, skills, restricciones y entregables.
4. El agente de requerimientos formaliza especificaciones cuando el trabajo lo requiera.
5. El humano valida requerimientos y alcance.
6. El asistente principal asigna tareas al agente de desarrollo, diseno, base de datos o testeo segun corresponda.
7. Desarrollo y testeo trabajan con la misma especificacion para evitar desviaciones.
8. El agente de testeo reporta incumplimientos al asistente principal y al agente de desarrollo.
9. El humano valida entregables criticos.
10. El asistente principal documenta cierre, decisiones, pendientes y memoria persistente.

Los agentes especialistas no se auto-invocan entre si. Toda coordinacion pasa por el asistente principal para mantener trazabilidad y evitar duplicidad.

---

## 6. Aplicacion de skills

Las skills obligatorias se aplican asi:

- **`prisma-base-de-datos`:** Obligatoria en todo cambio de modelo, migracion, semilla, repositorio, transaccion o acceso a datos relacional.
- **`backend-dominio-limpio`:** Obligatoria en todo endpoint, caso de uso, servicio, controlador, middleware o logica de backend.
- **`ui-ux-pro-max`:** Obligatoria en diseno visual, componentes, layouts, accesibilidad, experiencia de usuario y sistemas de diseno.
- **`ahorro-contexto`:** Obligatoria al iniciar y cerrar sesiones para evitar perdida de contexto y reducir lectura innecesaria de archivos.
- **`commits-espanol`:** Obligatoria para commits, reportes de cambios, pull requests y trazabilidad en control de versiones.

Cada agente recibe solo las skills necesarias para su tarea. Si una tarea mezcla frontend con backend o base de datos, el asistente principal separa el contexto visual del contexto critico.

---

## 7. Arquitectura backend

El backend debe organizarse bajo Clean Architecture, Clean Code, dominio limpio y arquitectura hexagonal. La estructura recomendada es:

```txt
backend/
└── src/
    ├── config/
    │   └── prisma.ts
    ├── modulos/
    │   └── administracion/
    │       └── almacen/
    │           ├── dominio/
    │           │   ├── entidades/
    │           │   └── repositorios/
    │           ├── aplicacion/
    │           │   ├── casos-uso/
    │           │   └── dto/
    │           ├── infraestructura/
    │           │   ├── prisma/
    │           │   └── repositorios/
    │           └── interfaces/
    │               └── http/
    │                   ├── controladores/
    │                   └── rutas.ts
    ├── compartido/
    │   ├── errores/
    │   ├── middlewares/
    │   └── validaciones/
    └── servidor.ts
```

Reglas backend:

- Los controladores reciben peticiones HTTP, validan DTOs, llaman casos de uso y devuelven respuestas.
- Los casos de uso contienen reglas de negocio y dependen de interfaces de repositorio.
- Los repositorios de infraestructura implementan las interfaces y son la unica capa autorizada para usar Prisma.
- Las entidades de dominio no deben depender de Express, Prisma ni librerias de infraestructura.
- Toda respuesta, error, log y comentario debe estar en espanol.
- Se documenta cualquier excepcion arquitectonica mediante una decision tecnica aprobada.

---

## 8. Arquitectura frontend

El frontend debe usar arquitectura modular y Atomic Design:

```txt
frontend/
└── src/
    ├── components/
    │   ├── atomos/
    │   ├── moleculas/
    │   ├── organismos/
    │   └── templates/
    ├── modules/
    │   └── administracion/
    │       └── almacen/
    │           ├── components/
    │           ├── services/
    │           ├── types/
    │           └── index.tsx
    ├── hooks/
    ├── pages/
    ├── services/
    ├── stores/
    ├── templates/
    ├── types/
    └── index.tsx
```

Reglas frontend:

- Primero se crean o reutilizan componentes base en `components/atomos`, `components/moleculas`, `components/organismos` y `components/templates`.
- Los modulos funcionales viven en `modules` y pueden tener componentes locales, pero deben basarse en componentes globales reutilizables.
- Las llamadas HTTP se centralizan en `services` mediante Axios. Ningun componente debe llamar directamente a `fetch` o `axios`.
- Los tipos e interfaces TypeScript se centralizan en `types` o en `modules/<modulo>/types`.
- Lucide React es la fuente obligatoria de iconos.
- Sonner es la herramienta obligatoria para notificaciones visuales.
- Zustand solo se usa cuando el estado global sea necesario; si el estado es local, se mantiene local.
- Tailwind CSS es el sistema de estilos obligatorio.

---

## 9. Uso de PostgreSQL y Prisma

PostgreSQL es la base de datos definitiva. Prisma es el unico ORM autorizado.

Reglas de base de datos:

- No se utiliza SQL Server por costo y por alineacion tecnica del proyecto.
- No se usa Knex ni query builders paralelos.
- No se escriben consultas SQL crudas salvo excepcion tecnica aprobada, documentada y probada.
- Todo modelo Prisma debe usar nombres en espanol, en singular y con `PascalCase`.
- Todo campo debe estar en espanol y `camelCase`, evitando acentos en identificadores por compatibilidad tecnica.
- Todo modelo persistente debe incluir `creadoEn`, `actualizadoEn` y, cuando aplique, `eliminadoEn` para borrado logico.
- Las migraciones se generan con nombres claros en espanol.
- Las semillas se documentan y se ubican en `prisma/seed.ts`.
- Las transacciones se realizan con Prisma cuando una operacion modifique varias entidades dependientes.

---

## 10. Metodologia Scrum por defecto

Scrum es la metodologia activa por defecto. El flujo minimo incluye:

1. Levantamiento de requerimientos.
2. Historias de usuario.
3. Criterios de aceptacion.
4. Priorizacion.
5. Backlog.
6. Planeacion de tareas.
7. Desarrollo guiado por especificaciones.
8. Pruebas.
9. Validacion con el humano.
10. Retroalimentacion.
11. Correccion.
12. Cierre de entregables.

El agente de testeo y el agente de desarrollo deben trabajar con la misma especificacion para que lo construido y lo validado coincidan.

---

## 11. Cambio flexible de metodologia

El humano, el desarrollador o el asistente principal pueden solicitar cambio de metodologia. El asistente principal adapta flujo, entregables, documentacion y validacion segun el marco elegido.

Metodologias permitidas:

- Scrum.
- Kanban.
- Cascada.
- Espiral.
- Extreme Programming.
- Desarrollo incremental.
- Desarrollo iterativo.
- Modelo en V.
- Metodologias hibridas.

El cambio de metodologia nunca altera las reglas tecnicas globales. Clean Architecture, Clean Code, dominio limpio, arquitectura hexagonal, PostgreSQL, Prisma, Atomic Design y documentacion en espanol siguen siendo obligatorios.

---

## 12. Integracion de memoria persistente

La memoria persistente forma parte permanente del flujo de orquestacion. Antes de iniciar una tarea, el asistente principal debe clasificar si el trabajo es visual/agil o critico/sensible.

Reglas de integracion:

- Antes de tareas criticas se verifica Mem Palace mediante `skills/ahorro-contexto/scripts/arranque.py`.
- Antes de cualquier modificacion importante se ejecuta `skills/ahorro-contexto/scripts/arranque.py` desde `Agentes_Unificados/` para recuperar Mem Palace y CloudMem local.
- Si la tarea es critica, se genera un prompt de arranque menor a 170 palabras con objetivo, modulo, herramientas, estado, decisiones relevantes, riesgos y resultado esperado.
- Al cerrar la sesion, el asistente principal registra decisiones, pendientes, riesgos y cambios mediante el mecanismo correspondiente.
- El cierre debe ejecutarse con `skills/ahorro-contexto/scripts/cierre.py` para acumular Mem Palace y, si aplica, registrar CloudMem local.
- Si una herramienta de memoria no esta instalada o disponible, el asistente principal debe reportarlo y generar instrucciones de instalacion o configuracion antes de continuar con tareas criticas.

Documento operativo: `context/flujo_memoria_persistente.md`.

### Memoria independiente por proyecto

Cada proyecto dentro de `Agentes_Unificados/proyectos/<nombre>/` debe contar con memoria propia en `proyectos/<nombre>/.memoria/`. Esta memoria contiene su Mem Palace local, su CloudMem local y su manifiesto de memoria.

Reglas:

- No se debe usar una memoria global para todos los proyectos.
- Las tareas de un proyecto concreto deben iniciar con `skills/ahorro-contexto/scripts/arranque.py --proyecto proyectos/<nombre>`.
- Las tareas de un proyecto concreto deben cerrar con `skills/ahorro-contexto/scripts/cierre.py --proyecto proyectos/<nombre>`.
- Al copiar `proyectos/_plantilla_proyecto`, se debe ejecutar `skills/ahorro-contexto/scripts/memoria_proyecto.py --proyecto proyectos/<nuevo> init`.
- La memoria raiz de la agencia solo conserva continuidad general de la agencia, no contexto especifico de proyectos.

---

## 13. Criterios de seleccion entre Cloud Mem y Mem Palace

Se usa **Cloud Mem** cuando la tarea sea:

- Visual.
- Rapida.
- De interfaz.
- Relacionada principalmente con React, Tailwind CSS, diseno o experiencia de usuario.
- De bajo riesgo tecnico.
- Un ajuste menor de componentes o vistas.
- Historial operativo no sensible de documentos, agentes, skills, guias o avances recientes.

Se usa **Mem Palace** cuando la tarea implique:

- Backend.
- Base de datos.
- PostgreSQL.
- Prisma.
- Logica de negocio.
- Inventarios.
- Produccion.
- Trazabilidad.
- Seguridad.
- Reglas criticas.
- Decisiones tecnicas sensibles.
- Modelos de datos o estructura interna del sistema.

Si existe duda sobre la sensibilidad de la informacion, se prioriza Mem Palace.

En ausencia de un servicio externo de Cloud Mem, la agencia usa **CloudMem local** en `.cloudmem.jsonl`, gestionado por `skills/ahorro-contexto/scripts/cloudmem.py`.

---

## 14. Seguridad y proteccion de informacion sensible

Queda prohibido almacenar en herramientas automaticas de nube informacion sensible del proyecto.

No debe enviarse a Cloud Mem:

- Credenciales.
- Secretos.
- Llaves de API.
- Configuraciones privadas.
- Modelos de datos sensibles.
- Reglas de negocio confidenciales.
- Inventarios.
- Produccion.
- Trazabilidad operativa.
- Seguridad.
- Decisiones tecnicas criticas.
- Informacion interna de backend o base de datos.

La informacion sensible debe mantenerse en Mem Palace o en documentacion local controlada. Cada agente recibe solo el contexto minimo necesario para cumplir su tarea.

---

## 15. Cierre de sesion y documentacion del contexto

Al finalizar una sesion, el asistente principal debe documentar:

- Cambios realizados.
- Archivos modificados.
- Decisiones tecnicas.
- Validaciones ejecutadas.
- Riesgos detectados.
- Pendientes.
- Siguiente paso recomendado.
- Herramienta de memoria utilizada.

Para tareas visuales o agiles, Cloud Mem conserva cambios de vistas, componentes, estilos y pendientes UI. Para tareas criticas, Mem Palace conserva decisiones de backend, base de datos, Prisma, reglas de negocio, seguridad y trazabilidad.

El cierre minimo debe indicar tareas completadas, archivos afectados, decisiones, riesgos, pendientes y herramienta de memoria utilizada. Cuando la informacion sea no sensible, tambien debe agregarse una entrada operativa en CloudMem local.

---

## 16. Mecanismos para evitar conflictos entre agentes

La agencia evita conflictos mediante:

- Asistente principal como punto unico de coordinacion.
- Especificaciones aprobadas antes de desarrollar.
- Skills obligatorias segun capa tecnica.
- Separacion estricta entre requerimientos, desarrollo, diseno, base de datos, pruebas y documentacion.
- Contratos API tipados y validados.
- Uso exclusivo de Prisma para persistencia.
- Componentes base centralizados en Atomic Design.
- Documentacion de decisiones tecnicas.
- Validacion humana en cambios criticos.
- Prohibicion de tecnologias paralelas no aprobadas.

---

## 17. Criterios de validacion con el humano

El humano debe validar:

- Alcance y requerimientos.
- Historias de usuario y criterios de aceptacion.
- Cambios de base de datos.
- Uso excepcional de SQL crudo.
- Nuevas dependencias relevantes.
- Decisiones de arquitectura.
- Entregables funcionales.
- Cierre de tareas criticas.

Ninguna fase critica debe cerrarse sin contemplar la validacion del humano.

---

## 18. Conclusion operativa

La agencia SMT queda unificada bajo un modelo de orquestacion centralizada, tecnologias obligatorias y reglas claras de memoria persistente. El asistente principal debe iniciar cada flujo, seleccionar agentes y skills, proteger informacion sensible, mantener al humano dentro del ciclo y asegurar que todo desarrollo respete Clean Architecture, Clean Code, dominio limpio, arquitectura hexagonal, React modular con Atomic Design, PostgreSQL y Prisma.

La regla operativa final es: **si la tarea afecta solo interfaz visual o ajustes rapidos de frontend, utiliza Cloud Mem; si afecta logica de negocio, backend, base de datos, inventarios, produccion o decisiones tecnicas criticas, utiliza Mem Palace.**
