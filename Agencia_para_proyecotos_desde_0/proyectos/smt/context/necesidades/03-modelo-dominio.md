# Modelo de dominio inicial

## Resumen

Este modelo describe las entidades necesarias para iniciar el diseno de base de datos y API del inventario central de unidades SMT. No es todavia un `schema.prisma`; es una especificacion de dominio para validar antes de implementar.

## Entidades principales

### Unidad

Representa cualquier vehiculo o equipo operativo administrado por SMT.

Atributos iniciales:

- `id`.
- `numeroUnidad`.
- `numeroEconomico`.
- `numeroAutomovil`.
- `nombrePublico`.
- `grupoDocumental`.
- `marca`.
- `modelo`.
- `anio`.
- `color`.
- `tipo`.
- `categoria`.
- `estado`.
- `placas`.
- `numeroSerie`.
- `numeroMotor`.
- `facturaReferencia`.
- `tarjetaCirculacionEstado`.
- `verificacionEstado`.
- `contaminantesEstado`.
- `fisicoMecanicaEstado`.
- `capacidad`.
- `tarifaBase`.
- `sueldoOperador`.
- `rendimientoRegular`.
- `rendimientoBajo`.
- `numeroEjes`.
- `costoReferencia`.
- `fuenteImportacion`.
- `areaActual`.
- `activa`.
- `creadoEn`.
- `actualizadoEn`.
- `eliminadoEn`.

Reglas:

- `numeroEconomico` es unico y no reutilizable.
- `numeroUnidad` identifica la unidad durante la captura. Si existe `numeroEconomico`, ambos deben mapearse sin perder ceros iniciales.
- Una unidad con historial no debe eliminarse fisicamente.
- La unidad es propiedad logica del inventario global, no de una aplicacion consumidora.
- Los valores heredados del Excel como `NO TIENE`, `EXCENTO`, celdas vacias o numeros seriales de fecha deben normalizarse antes de guardarse.

### Usuario

Representa una persona que accede a una o mas aplicaciones de SMT.

Atributos iniciales:

- `id`.
- `nombre`.
- `correo`.
- `contrasenaHash`.
- `activo`.
- `ultimoAccesoEn`.
- `creadoEn`.
- `actualizadoEn`.
- `eliminadoEn`.

Reglas:

- El usuario se autentica contra la API central.
- Los permisos efectivos se calculan a partir de roles y permisos.
- Usuarios desactivados no pueden obtener tokens validos.

### Rol

Agrupa permisos para usuarios y aplicaciones.

Atributos iniciales:

- `id`.
- `nombre`.
- `descripcion`.
- `activo`.
- `creadoEn`.
- `actualizadoEn`.

Roles iniciales propuestos:

- `administrador_global`.
- `taller`.
- `mantenimiento`.
- `turismo`.
- `fletes`.
- `transporte_personal`.
- `consulta`.

Reglas:

- Los roles existentes de Angel y Roberto deben integrarse despues de recibir evidencia.
- Un rol no debe otorgar acceso amplio sin justificacion.

### Permiso

Representa una accion autorizada dentro del sistema.

Atributos iniciales:

- `id`.
- `clave`.
- `descripcion`.
- `creadoEn`.
- `actualizadoEn`.

Permisos iniciales propuestos:

- `unidades.consultar`.
- `unidades.crear`.
- `unidades.editar`.
- `unidades.cambiar_estado`.
- `unidades.reasignar`.
- `mantenimientos.consultar`.
- `mantenimientos.crear`.
- `mantenimientos.finalizar`.
- `usuarios.consultar`.
- `usuarios.crear`.
- `usuarios.editar`.
- `roles.administrar`.

### Mantenimiento

Representa un servicio preventivo, correctivo o programado asociado a una unidad.

Atributos iniciales:

- `id`.
- `unidadId`.
- `tipo`.
- `estado`.
- `descripcion`.
- `fechaProgramada`.
- `fechaInicio`.
- `fechaFinalizacion`.
- `kilometrajeProgramado`.
- `kilometrajeReal`.
- `prioridad`.
- `responsableId`.
- `creadoEn`.
- `actualizadoEn`.

Estados propuestos:

- `programado`.
- `en_proceso`.
- `finalizado`.
- `cancelado`.

Reglas:

- Un mantenimiento en proceso puede cambiar la unidad a `en_mantenimiento`.
- Las alertas por dias se calculan con `fechaProgramada`.
- Las alertas por kilometraje quedan pendientes de validacion.

### Seguro

Representa informacion de poliza y vigencia de una unidad.

Atributos iniciales:

- `id`.
- `unidadId`.
- `aseguradora`.
- `numeroPoliza`.
- `vigenciaInicio`.
- `vigenciaFin`.
- `archivoReferencia`.
- `activo`.
- `creadoEn`.
- `actualizadoEn`.

Reglas:

- Una unidad puede tener historico de seguros.
- Solo una poliza debe marcarse como activa cuando aplique.

### DocumentoUnidad

Representa documentos asociados a una unidad.

Atributos iniciales:

- `id`.
- `unidadId`.
- `tipo`.
- `folio`.
- `vigenciaInicio`.
- `vigenciaFin`.
- `ubicacion`.
- `responsableActualId`.
- `observaciones`.
- `creadoEn`.
- `actualizadoEn`.

Tipos iniciales:

- `factura`.
- `tarjeta_circulacion`.
- `verificacion`.
- `contaminantes`.
- `fisico_mecanica`.
- `emisiones`.
- `otro`.

Reglas:

- Debe permitir conocer donde esta la tarjeta de circulacion o quien la tiene.
- Debe soportar documentos sin vigencia cuando aplique.
- Debe diferenciar documentos vencidos, vigentes, exentos, pendientes, inexistentes y no aplicables.

### LecturaOdometro

Representa una lectura historica de kilometraje.

Atributos iniciales:

- `id`.
- `unidadId`.
- `kilometraje`.
- `fechaLectura`.
- `origen`.
- `usuarioId`.
- `observaciones`.
- `creadoEn`.

Reglas:

- La lectura mas reciente alimenta consultas operativas.
- Debe registrarse el origen si viene de captura manual, importacion o integracion.

### ReasignacionUnidad

Representa el uso temporal o cambio controlado de una unidad entre areas.

Atributos iniciales:

- `id`.
- `unidadId`.
- `areaOrigen`.
- `areaDestino`.
- `fechaInicio`.
- `fechaFin`.
- `motivo`.
- `estado`.
- `autorizadoPorId`.
- `creadoEn`.
- `actualizadoEn`.

Estados propuestos:

- `activa`.
- `finalizada`.
- `cancelada`.

Reglas:

- La reasignacion no borra el historial de categoria o area original.
- Debe tener responsable autorizado.

## Enumeraciones iniciales

### EstadoUnidad

- `disponible`.
- `en_taller`.
- `en_mantenimiento`.
- `fuera_servicio`.
- `inactiva`.

### CategoriaUnidad

- `ATAH`.
- `oaxaca`.
- `turismo`.
- `tracto`.
- `transporte_personal`.

### TipoMantenimiento

- `preventivo`.
- `correctivo`.
- `servicio`.
- `reparacion`.

### PrioridadMantenimiento

- `baja`.
- `media`.
- `alta`.
- `critica`.

## Relaciones iniciales

- `Unidad` tiene muchos `Mantenimiento`.
- `Unidad` tiene muchos `Seguro`.
- `Unidad` tiene muchos `DocumentoUnidad`.
- `Unidad` tiene muchas `LecturaOdometro`.
- `Unidad` tiene muchas `ReasignacionUnidad`.
- `Usuario` tiene muchos `Rol` mediante relacion intermedia.
- `Rol` tiene muchos `Permiso` mediante relacion intermedia.
- `Usuario` puede crear o autorizar altas, cambios, mantenimientos y reasignaciones.

## Pendientes del modelo

- Confirmar si `areaActual` sera entidad propia o enumeracion.
- Confirmar si `numeroUnidad`, `numeroEconomico` y `numeroAutomovil` deben mantenerse como campos separados o consolidarse segun el tipo de unidad.
- Confirmar si `T/C` significa tarjeta de circulacion y si debe vivir como estado de documento o como documento independiente.
- Confirmar si `facturaReferencia` representa folio, emisor, propietario, ubicacion fisica o archivo relacionado.
- Confirmar si `sueldoOperador` pertenece a la unidad, al operador o a una regla de calculo por servicio.
- Confirmar si `costoReferencia` de ATAH pertenece al inventario o a un modulo financiero.
- Confirmar si operadores se modelaran en esta API o en otro servicio.
- Confirmar reglas exactas de mantenimiento por dias, kilometraje o ambos.
