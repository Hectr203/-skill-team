# Auditoría integral de la agencia

Fecha: 2026-10-08. Alcance: documentación, agentes, reglas, flujos, perfiles, configuración MCP, plantillas, scripts y pruebas de esta agencia. Se respetan los cambios anteriores y la arquitectura modular acordada.

## Correcciones aplicadas

- El asistente principal coordina, asigna responsables y consolida resultados. El rol orquestador apoya sin competir por la comunicación ni autorizar nuevas operaciones.
- Los agentes remiten al contrato común y al stack elegido. El frontend conserva módulos por dominio; backend y base de datos toman sus decisiones del perfil y del contrato de integración. Azure tiene un perfil de despliegue opcional.
- La selección de skills usa un catálogo único, búsqueda de metadatos y resolución exacta de fuentes. El CLI y MCP no ejecutan una skill por encontrarla. Se leen sus instrucciones y recursos cuando corresponde al alcance, las herramientas disponibles y los permisos.
- Las plantillas permiten registrar nuevos agentes sin listas obligatorias de skills. La plantilla de skill define activación, límites, entradas, recursos y procedencia sin exigir la arquitectura de un proyecto.
- Se eliminaron mandatos generales de IDE, proveedor, framework de pruebas y aprobación para cada edición local. Los flujos distinguen actividades autorizadas y operaciones externas que requieren autorización.
- La memoria permanece local; encontrar un ejecutable externo ya no provoca transferencias. Los contextos usan identificadores exactos y rechazan enlaces simbólicos que desvían la lectura.
- Una validación pendiente devuelve código 2. Un fallo al registrar autorización impide devolver aprobación. Las notificaciones respetan silencio y generan archivos temporales privados en lugar de publicar datos en ejemplos versionados.
- La guía de inicio describe lo que el CLI realmente crea: contexto y memoria, no una aplicación. Se corrigieron rutas y capacidades obsoletas; las evidencias anteriores se conservan como históricas.

## Cobertura y límites

El [registro por archivo](evidencias/auditoria-archivos.json) enumera cada archivo del alcance y distingue revisión documental, comprobación estructural, evidencia histórica y metadatos privados. Los audios se comprueban como recursos binarios; no se certifica su contenido sonoro. No se descifraron almacenes ni se publicaron claves.

Las 827 fuentes y recursos bajo `skills/` conservan sus bytes respecto al inicio de esta revisión. Sus cambios anteriores al inicio permanecen; esta auditoría no certifica la calidad de sus procedimientos ni ejecuta sus suites. Los adaptadores generados se validan como interfaz del catálogo.

La revisión inicial cerró con 41 pruebas de operación, aislamiento, integración de skills, registro de agentes, MCP y controles de aprobación. Ejecutar `python3 scripts/agencia.py verificar` y después `comprobar` para consultar evidencia vinculada al contenido actual. `doctor` verifica el entorno y el protocolo local.

No se conectaron servicios externos, desplegaron aplicaciones ni modificaron índices de Git. La configuración externa, las credenciales y las pruebas de cada aplicación requieren comprobaciones independientes. El contrato documental reduce contradicciones; su cumplimiento por un modelo exige comprobar resultados y evidencias en cada tarea.

## Refuerzo posterior de calidad

Se incorporó `scripts/control_entregas.py`, disponible también mediante `agencia.py entregas`, con plantilla de registro y contrato de cierre. Rechaza criterios pendientes declarados completos, evidencias ausentes o alteradas, rutas externas o simbólicas, tiempos inconsistentes y métricas inválidas. No ejecuta instrucciones de los registros.

El primer refuerzo amplió la suite a 51 pruebas. Las métricas separan costos por moneda, mantienen valores desconocidos y rechazan tareas duplicadas. Los [escenarios operativos](evaluacion-operativa.md) dejan criterios para probar agentes y servicios reales sin atribuirles resultados todavía no observados. Estas mejoras refuerzan los controles; no son una certificación universal ni demuestran por sí solas una agencia de 10.

## Coordinación transaccional y revisión con grafos

Se consultó CodeGraph para localizar `cmd_estado`, `evaluar`, `metricas` y `huellas`, y Graphify para comprobar sus consumidores. El grafo del 2026-10-08 contiene 3314 nodos y 7359 relaciones en el repositorio completo; estos conteos describen el índice, no la calidad de la agencia. Las relaciones sirvieron para delimitar pruebas de CLI, MCP y controles compartidos; no sustituyen la lectura del código actual.

Las correcciones de esta fase incorporan:

- Planes locales transaccionales con tareas, roles registrados, criterios, archivos responsables y dependencias sin ciclos. No crean agentes ni contactan terceros.
- Revisiones esperadas que rechazan actualizaciones simultáneas obsoletas sin perder escrituras. Estados con reglas de inicio, bloqueo, cancelación, reapertura y cierre.
- Cierres ligados al proyecto, tarea, criterios y huellas de artefactos. Cambiar código, informe, evidencia o un antecesor invalida su vigencia; no iniciar ni cerrar dependientes hasta corregirla.
- Nuevas fases que archivan planes anteriores en una transacción y conservan historial. La consulta MCP `agencia_plan` comparte el mismo almacén que el CLI.
- Rechazo de almacenes de proyectos o informes de verificación redirigidos. Los IDs malformados de JSON-RPC ya no producen respuestas con IDs inválidos; el servidor continúa atendiendo solicitudes válidas.
- Resolución de metadatos de una skill exacta sin leer las descripciones de todas las otras fuentes. No se modificó contenido de skills.

La suite actual contiene 67 pruebas, incluidas concurrencia real en SQLite, ciclo CLI/MCP, dependencias, cierre con evidencia, invalidación en cascada, fases, corrupción y rutas externas. Para comprobar el estado del contenido ejecutar `verificar` y `comprobar`.

Límites: las rutas de los informes y evidencias deben conservarse para reanudar. El almacén es local y editable por el usuario del equipo; no constituye una firma ni una autorización de publicación. El control no supervisa procesos ya abiertos, no interpreta la calidad semántica de logs y no certifica el comportamiento de todos los modelos. No se probaron cuentas externas ni aplicaciones de clientes en esta fase.
