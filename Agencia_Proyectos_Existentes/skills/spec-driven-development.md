# Skill: Spec-Driven Development

## Proposito
Definir especificacion, criterios de aceptacion y limites antes de implementar.

## Base principal
- `Agencia_Proyectos_Existentes/skills/agent-skills/skills/spec-driven-development/SKILL.md`

## Rol en el sistema
Esta skill es la traduccion local del flujo de especificacion del nucleo. Convierte requerimientos difusos en una spec utilizable para planificar e implementar.

## Cuando usar
- Funcionalidades amplias.
- Reglas de negocio complejas.
- Cambios con varias capas.
- Ambiguedad funcional.

## Procedimiento
1. Definir objetivo.
2. Especificar alcance y fuera de alcance.
3. Documentar reglas de negocio.
4. Crear criterios de aceptacion.
5. Definir pruebas esperadas.

## Salidas
- Especificacion tecnica o funcional.
- Criterios de aceptacion.
- Plan de validacion.

## Integracion con el ciclo de iteraciones

La especificacion generada por esta skill es la fuente principal de verdad durante todo el ciclo de desarrollo.

### Uso en el loop
1. La especificacion se entrega al orquestador antes de iniciar la implementacion.
2. El orquestador la utiliza como referencia para definir criterios de aceptacion y casos de prueba.
3. Durante la validacion, cada criterio de aceptacion se evalua contra la especificacion original.
4. Si se detecta una contradiccion entre la implementacion y la especificacion, se corrige la implementacion.
5. Si la especificacion esta incorrecta o incompleta, se actualiza antes de continuar.

### Condiciones para avanzar
- No se debe iniciar implementacion sin una especificacion completa.
- No se debe pasar a pruebas sin que la implementacion corresponda a la especificacion.
- No se debe cerrar la tarea sin que todos los criterios de aceptacion esten verificados.

### Registro de trazabilidad
Cada requerimiento en la especificacion debe poder trazarse hasta:
- Las historias de usuario que lo originaron.
- Los criterios de aceptacion que lo verifican.
- Los casos de prueba que lo validan.
- Las iteraciones donde fue implementado y corregido.
