# Operación unificada

La entrada es el [asistente principal](../asistente-principal.md). Las reglas comunes viven en [AGENTS](../AGENTS.md) y [precedencia](../reglas/precedencia.md); los roles aplican el [contrato compartido](../agentes/contrato-agente.md).

El manifiesto y [stacks](../stacks/README.md) definen arquitectura y tecnología; el estándar conserva frontend modular por dominio, backend con puertos/adaptadores y persistencia documentada. No se impone ese perfil a proyectos existentes o alternativos.

Las [skills](../reglas/seleccion-skills.md) son capacidades independientes seleccionadas por resultado. [Flujos](../flujos/dev-flow-completo.md) definen trabajo y controles; [memoria](flujo_memoria.md) conserva contexto por ID. MCP, CLI y el IDE son vías de acceso disponibles, no nuevas autoridades o permisos.

Cada entrega informa qué cambió, qué se comprobó y qué falta. La [verificación local](../reglas/verificacion-local.md) acredita controles del checkout de la agencia, sin certificar aplicaciones, servicios externos o resultados comerciales.
