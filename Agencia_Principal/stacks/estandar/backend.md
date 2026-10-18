# Perfil estándar: Backend

## Tecnología
Node.js con Express y JavaScript ES Modules; PostgreSQL y Prisma para persistencia. Conservar la versión fijada por el proyecto. Zod para validación de entradas del perfil; JSDoc para contratos útiles. Autenticación y hash de contraseñas se eligen conforme al flujo y requisitos del proyecto; conservar JWT/bcryptjs donde ya estén aprobados. No añadir autenticación a endpoints públicos sin un requisito.

No copiar versiones de paquetes de ejemplos antiguos ni actualizar versiones mayores incidentalmente. Prisma, su cliente y sus adaptadores deben ser compatibles con la versión instalada. Otros perfiles seleccionan sus propias tecnologías sin cambiar este perfil.

## Arquitectura y archivos
Aplicar [arquitectura backend](arquitectura-backend.md): módulos de negocio, casos de uso independientes de Express y Prisma, y composición por módulo. Los puertos y adaptadores son límites de dependencia, no capas o archivos obligatorios. La fuente define árbol, responsabilidades, flujo, validación y transacciones; no duplicarlos en la ficha del agente.

## Simplicidad
Todo trabajo backend aplica Ponytail en nivel `full` según la [política de simplicidad](../../reglas/simplicidad-ponytail.md): reutilizar antes de crear, capacidades nativas de JavaScript, Node.js, Express, PostgreSQL y Prisma antes que dependencias nuevas, y ninguna capa o archivo sin necesidad actual.

## Integración y calidad
Aplicar el [contrato del perfil](contrato-integracion.md) y [persistencia](base-datos.md). Validar comportamiento, errores, autorización por cliente, contratos API e integridad. Usar comandos reales del proyecto y registrar controles pendientes. No devolver trazas o credenciales en respuestas.
