# Precedencia y alcance de las reglas

Respeta primero las instrucciones del entorno y las decisiones explícitas del humano. Una autorización vigente para una tarea se conserva durante su ejecución; no se pide de nuevo por una recomendación genérica de una skill.

Dentro de la agencia, aplica este orden:

1. Seguridad y aislamiento de clientes: ninguna elección de stack permite mezclar memorias o incluir secretos en documentos.
2. Manifiesto y ADRs vigentes del proyecto: determinan su tecnología y convenciones. En proyectos existentes conserva las convenciones detectadas salvo cambio autorizado.
3. Perfil seleccionado en `stacks/`: el estándar JavaScript es el valor predeterminado para proyectos nuevos sin perfil propio. Un perfil alternativo sustituye los requisitos de tecnología del estándar para ese proyecto.
4. `AGENTS.md`, reglas de la agencia y asistente principal: definen el proceso común.
5. Fichas de agentes y ejemplos: aplican dentro del alcance anterior. Las skills son capacidades independientes seleccionadas por compatibilidad. Los ejemplos no obligan a instalar dependencias ni cambiar de lenguaje.

Una prohibición de TypeScript, ORM o motor de datos en una ficha del stack estándar no se extiende a un proyecto con otro perfil aprobado. Tampoco obliga a migrar proyectos existentes.

La fuente de selección de habilidades es `.agencia/catalogo-skills.json`. Las entradas de `.agencia/skills-activos/` remiten a sus fuentes; las variantes no se cargan automáticamente.

No afirmar que una herramienta está activa por estar documentada. Distinguir archivo presente, ejecutable probado, conexión comprobada y operación completada.

CodeGraph se consulta antes de explorar estructura o símbolos cuando está disponible y conforme al protocolo del entorno (usando directamente el comando nativo `codegraph`, nunca el prefijo `gentle-ai`). Graphify y Headroom se usan cuando están disponibles; si fallan o no están instalados, explicar la limitación y continuar con inspección localizada sin afirmar que hubo compresión.

Usa el chat o artefactos disponibles para planes; conserva los acuerdos estables y documentación necesaria en la ubicación acordada del proyecto. No inventes rutas de un IDE diferente.

Para operaciones sensibles, una notificación no constituye aprobación. El script de autorización devuelve 0 únicamente tras aprobación interactiva registrada; 1 ante rechazo o fallo y 2 si sigue pendiente. Una aprobación dada en el chat se registra por el mecanismo del entorno y no se sustituye por una solicitud nueva.

Antes de cerrar, comunicar pruebas ejecutadas, fallos, integraciones no comprobadas y próximos pasos concretos. Las capacidades comerciales deben basarse en resultados reales.
