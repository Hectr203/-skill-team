# Estructura de la agencia

La estructura vigente mantiene una base reutilizable y contextos aislados; no requiere duplicar la agencia por cliente ni mover las skills por proyecto.

- `agentes/`: roles, límites y entregas. El asistente principal coordina.
- `stacks/`: contratos tecnológicos y arquitectónicos por perfil.
- `flujos/`: procedimientos por tipo de resultado, independientes del runtime de IA.
- `reglas/`: precedencia, permisos, aislamiento y selección de capacidades.
- `plantillas/`: entradas y entregables reutilizables.
- `contexts/`: proyectos, clientes, marcas, campañas y operación de la agencia.
- `scripts/` y `tests/`: operación local y comprobaciones.
- `mcp/`: adaptadores y estados de integraciones.
- `skills/`: fuentes independientes, propias o de terceros; su contenido no forma parte de esta auditoría general.
- `.agencia/`: catálogo y entradas de descubrimiento generadas; la evidencia local se regenera para cada contenido.

El manifiesto vincula proyecto y perfil. Las skills se seleccionan por tarea mediante [contrato](../reglas/seleccion-skills.md), no por ubicación de un cliente. El código de aplicación queda fuera de esta carpeta. Una nueva organización de fuentes requiere una tarea explícita; no copiar árboles paralelos para resolver nombres.
