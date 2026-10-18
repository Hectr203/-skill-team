# Proceso común de desarrollo

El [asistente principal](../asistente-principal.md) interactúa con el usuario y coordina roles. No existe un segundo orquestador ni una dependencia universal de IDE, lenguaje o proveedor de IA.

1. Identificar proyecto, objetivo, alcance y criterios. Recuperar contexto mínimo y registrar supuestos.
2. Resolver el [perfil](../stacks/README.md), contratos vigentes y estructura real; preservar cambios existentes.
3. Elegir flujo por resultado: [nuevo](proyecto-nuevo.md), [existente](proyecto-existente.md), [incremental](desarrollo-incremental.md), [urgente](correccion-urgente.md) o [auditoría](auditoria-seguridad.md).
4. Asignar un dueño por entregable y dependencias mediante [tarea/traspaso](../plantillas/tarea-agente.md). Los roles seleccionan [skills](../reglas/seleccion-skills.md) por resultado y compatibilidad. Una ficha no crea procesos.
5. Implementar dentro del alcance con controles proporcionales al riesgo; cambiar el enfoque según evidencia si falla. Continuar partes independientes ante un bloqueo. En backend, persistencia y frontend, aplicar antes de codificar la escalera de decisión de la [política de simplicidad](../reglas/simplicidad-ponytail.md) y seguir su flujo por funcionalidad.
6. Aplicar [revisión y cierre](revision-y-cierre.md). Registrar resultado, decisiones, pruebas y pendientes en el contexto apropiado.

Diseño, navegador, despliegue, operación comercial y publicación son flujos específicos según alcance; no son fases obligatorias de cualquier tarea. La autorización vigente se conserva y no se extiende a operaciones externas no solicitadas. La verificación local de la agencia y las pruebas de aplicaciones se registran por separado.
