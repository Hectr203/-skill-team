# Perfiles de arquitectura y tecnología

Los agentes describen responsabilidades y coordinación. `stacks` define tecnologías, arquitectura, archivos, límites, integración y validación del perfil seleccionado. El manifiesto y ADRs registran decisiones particulares; aplicar [precedencia](../reglas/precedencia.md). Los perfiles pueden evolucionar mediante cambios autorizados; no se modifican por trabajar con otro cliente o tecnología.

## Resolución del perfil
1. Leer `Stack Tecnológico Asignado` en `contexts/projects/<id>/manifiesto.md` y confirmar la ruta registrada. No inferirlo por palabras de una tarea.
2. `estandar` se usa para proyectos nuevos sin otro perfil. Para proyectos existentes comprobar stack y arquitectura reales; no asignar ni migrar por defecto si falta la decisión. Documentar lo detectado y resolver lo imprescindible.
3. Leer entradas y contrato de la capa afectada. Los perfiles alternativos pueden definir todas las capas en `stack.md`; no heredan tecnologías estándar implícitamente. Una capa no utilizada se marca como no aplicable.
4. Seleccionar skills por resultado y compatibilidad con el perfil. El registro identifica roles; no limita qué skills pueden utilizar. Consultar la selección común por tarea.
5. Entregar perfil y documentos usados, ubicación de cambios, validaciones y desviaciones justificadas. No modificar fuera del alcance ni declarar ejecutado un despliegue o migración por haberlo diseñado.

## Perfil estándar
- [Frontend](estandar/frontend.md): tecnología y [arquitectura arquitectura modular por dominio](estandar/arquitectura-frontend.md).
- [Backend](estandar/backend.md): tecnología y [Clean Architecture con puertos/adaptadores](estandar/arquitectura-backend.md).
- [Base de datos](estandar/base-datos.md): esquema, persistencia, migraciones e integridad.
- [Integración](estandar/contrato-integracion.md): contratos, responsables y comprobaciones entre capas.

El frontend y el backend tienen estructuras distintas y comparten contratos públicos; la estructura arquitectura modular por dominio no se traslada al servidor. Los agentes consultan este perfil en lugar de duplicar sus árboles de carpetas.

## Otros perfiles
[Laravel, Livewire y Alpine](alternativos/laravel-livewire-alpine/stack.md) conserva su propio contrato. Registrar otro perfil mediante [plantilla](plantillas/nuevo-stack.md), completando capas y validación antes de seleccionarlo. El CLI rechaza rutas inexistentes y no genera perfiles vacíos; esto no equivale a comprobar automáticamente toda su arquitectura.

## Despliegue

El [perfil Azure](despliegue/azure.md) es un adaptador opcional, independiente del perfil de aplicación. Otros proveedores se documentan cuando un proyecto los requiere, sin imponer Azure a la agencia.
