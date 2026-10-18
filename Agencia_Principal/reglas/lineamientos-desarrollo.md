# Lineamientos de desarrollo

## Contexto y arquitectura
Leer objetivo, criterios, código y decisiones vigentes. Resolver el perfil en [stacks](../stacks/README.md); conservar convenciones de proyectos existentes. Los agentes coordinan responsabilidades y no fijan tecnologías universales. Las fronteras de módulos y contratos se verifican según el perfil seleccionado.

## Implementación
Reutilizar comportamiento existente cuando corresponde. Separar responsabilidades y evitar archivos, comentarios o abstracciones que no aporten claridad. Los comentarios explican decisiones no evidentes; no repetir cada línea. Mantener español en comunicación y nombres propios nuevos sin romper APIs, convenciones o contratos externos. En backend, persistencia y frontend, aplicar la escalera de decisión de la [política de simplicidad](simplicidad-ponytail.md) antes de escribir código.

Aplicar [skills pertinentes](seleccion-skills.md) después de leer su contrato. Un ejemplo no ordena instalar una dependencia ni cambiar de lenguaje. Validar entradas en las fronteras, permisos en el sistema responsable e integridad donde se guardan datos.

## Datos, pruebas y documentación
Preparar cambios de datos con compatibilidad y recuperación. Elegir pruebas unitarias, integración o recorridos según riesgo; conservar el runner del proyecto. TDD puede ayudar a reproducir un defecto, pero no se exige Playwright ni un proceso único para toda tarea.

Actualizar contratos, instrucciones y decisiones realmente afectados. Mantener una fuente por regla; enlazarla en lugar de copiarla. Distinguir estado real, objetivo y ejemplo. Cerrar con evidencia del comportamiento, controles pendientes y riesgos, según [revisión y cierre](../flujos/revision-y-cierre.md).
