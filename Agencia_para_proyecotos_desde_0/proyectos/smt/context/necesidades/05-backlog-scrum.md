# Backlog Scrum inicial

## Resumen

Este backlog organiza el primer ciclo del proyecto de inventario central de unidades y gestion de usuarios. La prioridad inicial es validar documentacion, cerrar decisiones criticas y preparar el desarrollo fullstack: API backend y frontend visual administrativo.

## Epica 1: Fuente unica de unidades

### HU-01 Catalogo global de unidades

Como administrador global, quiero registrar y consultar unidades en un catalogo central para que todas las aplicaciones consuman la misma informacion.

Criterios de aceptacion:

- El catalogo concentra unidades de todas las categorias iniciales.
- El numero economico es unico.
- Las unidades inactivas se conservan en historial.
- Las aplicaciones no necesitan crear inventarios locales para consultar unidades.

Prioridad: Alta.

### HU-02 Consulta de unidades disponibles

Como usuario de una aplicacion operativa, quiero consultar unidades disponibles para usar solo vehiculos aptos para mi operacion.

Criterios de aceptacion:

- La consulta excluye unidades en taller, mantenimiento, fuera de servicio e inactivas.
- La consulta respeta categorias y permisos.
- Turismo, Oaxaca, tracto, ATAH y transporte de personal pueden filtrar segun su necesidad.

Prioridad: Alta.

### HU-03 Historial de unidades inactivas

Como administrador global, quiero conservar el historial de unidades inactivas para evitar reutilizar numeros economicos y mantener trazabilidad.

Criterios de aceptacion:

- Una unidad inactiva no se elimina fisicamente.
- El numero economico no se puede reutilizar.
- La unidad puede consultarse como historica.

Prioridad: Alta.

## Epica 2: Seguridad, usuarios y permisos

### HU-04 Inicio de sesion centralizado

Como usuario de SMT, quiero iniciar sesion con una cuenta central para acceder a las aplicaciones autorizadas.

Criterios de aceptacion:

- El inicio de sesion devuelve token.
- El token contiene o permite consultar usuario, roles y permisos.
- Un usuario inactivo no puede iniciar sesion.

Prioridad: Alta.

### HU-05 Validacion de token por aplicaciones

Como backend consumidor, quiero validar tokens contra la API central para proteger informacion privada.

Criterios de aceptacion:

- Un token invalido rechaza consultas.
- Un token vencido no permite operaciones.
- La validacion devuelve permisos efectivos.

Prioridad: Alta.

### HU-06 Administracion de roles y permisos

Como administrador global, quiero administrar roles y permisos para controlar que informacion ve cada area.

Criterios de aceptacion:

- Los roles pueden asociarse a usuarios.
- Los permisos controlan endpoints y datos visibles.
- Los roles existentes de Angel y Roberto se incorporan despues de recibir evidencia.

Prioridad: Alta.

## Epica 3: Taller y mantenimiento

### HU-07 Entrada de unidad a taller

Como usuario de taller, quiero marcar una unidad como en taller para impedir que se use operativamente.

Criterios de aceptacion:

- La unidad cambia a `en_taller`.
- Deja de aparecer como disponible.
- Se registra motivo, fecha y responsable.

Prioridad: Alta.

### HU-08 Salida de unidad de taller

Como usuario de taller, quiero liberar una unidad cuando termine su reparacion para que vuelva a estar disponible si no tiene bloqueos.

Criterios de aceptacion:

- La unidad puede volver a `disponible`.
- El evento de salida queda registrado.
- La disponibilidad se actualiza para todas las aplicaciones consumidoras.

Prioridad: Alta.

### HU-09 Alertas de mantenimiento

Como responsable de mantenimiento, quiero ver unidades proximas a servicio para atenderlas a tiempo.

Criterios de aceptacion:

- Se muestran alertas a 30, 15 y 3 dias.
- Las unidades con 3 dias o menos se muestran con prioridad alta.
- El sistema permite finalizar mantenimiento.

Prioridad: Media.

### HU-10 Lecturas de odometro

Como responsable operativo, quiero registrar kilometraje para planear mantenimientos por uso real.

Criterios de aceptacion:

- Cada lectura guarda kilometraje, fecha y usuario.
- La unidad muestra su lectura mas reciente.
- La regla de mantenimiento por kilometraje queda preparada para definicion posterior.

Prioridad: Media.

## Epica 4: Documentacion vehicular

### HU-11 Seguros y vigencias

Como administrador global, quiero registrar seguros y vigencias para consultar el estado documental de cada unidad.

Criterios de aceptacion:

- Se registra poliza, aseguradora y vigencia.
- Se puede identificar poliza vigente.
- Se conserva historial de polizas anteriores.

Prioridad: Media.

### HU-12 Tarjeta de circulacion y documentos

Como administrador global, quiero saber quien tiene documentos de la unidad para evitar perdida de tarjetas o archivos.

Criterios de aceptacion:

- Se registra tipo de documento, ubicacion y responsable actual.
- Se puede consultar documentacion por unidad.
- Se puede actualizar responsable o ubicacion.

Prioridad: Media.

## Epica 5: Reasignaciones y reportes

### HU-13 Reasignacion temporal

Como administrador autorizado, quiero reasignar temporalmente una unidad a otra area para cubrir necesidades operativas.

Criterios de aceptacion:

- Se registra area origen, area destino, fechas, motivo y autorizacion.
- La unidad conserva historial.
- La reasignacion puede finalizarse.

Prioridad: Media.

### HU-14 Reportes personalizados por area

Como usuario de area, quiero recibir reportes filtrados para consultar solo unidades relevantes a mi operacion.

Criterios de aceptacion:

- El reporte filtra por permisos, categoria y disponibilidad.
- Los usuarios no ven informacion fuera de su alcance.
- El reporte reduce busquedas manuales en Excel.

Prioridad: Baja.

## Epica 6: Frontend administrativo

### HU-15 Estructura visual administrativa

Como administrador global, quiero una interfaz administrativa organizada para operar el inventario sin depender de peticiones manuales a la API.

Criterios de aceptacion:

- Existe layout administrativo con navegacion protegida.
- El frontend usa React, TypeScript, Tailwind CSS, React Router DOM, Axios, Zustand, Lucide React y Sonner.
- La estructura respeta Atomic Design y modulos funcionales.
- Las rutas visuales se organizan por autenticacion, tablero, unidades, documentos, mantenimientos, usuarios y reportes.
- La propuesta visual sigue `08-lineamientos-visuales-administrativos.md`.

Prioridad: Alta.

### HU-16 Inicio de sesion visual

Como usuario de SMT, quiero iniciar sesion desde la interfaz visual para acceder solo a las funciones autorizadas.

Criterios de aceptacion:

- La pantalla de inicio de sesion consume `POST /api/autenticacion/iniciar-sesion`.
- El token se conserva en el estado de sesion.
- Las rutas protegidas bloquean acceso sin sesion.
- El cierre de sesion limpia token y estado local.

Prioridad: Alta.

### HU-17 Tablero administrativo

Como responsable administrativo, quiero ver un tablero general para supervisar disponibilidad, mantenimientos y documentos.

Criterios de aceptacion:

- El tablero muestra unidades por estado.
- Muestra mantenimientos proximos y prioridad de 3 dias o menos.
- Muestra documentos o polizas pendientes, vencidos o proximos a vencer.
- Los datos visibles respetan permisos del usuario.

Prioridad: Alta.

### HU-18 Administracion visual de unidades

Como administrador global, quiero crear, editar y consultar unidades desde formularios visuales para controlar el inventario central.

Criterios de aceptacion:

- El listado consume `GET /api/unidades`.
- El alta consume `POST /api/unidades`.
- El formulario incluye campos base: numero de unidad, marca, tipo, serie, motor, placas, factura, T/C, poliza y vigencia.
- El formulario contempla campos complementarios: modelo, color, verificacion, contaminantes, fisico-mecanica y costo si aplica.
- Las acciones se muestran segun permisos.

Prioridad: Alta.

### HU-19 Gestion visual de documentos y mantenimientos

Como responsable autorizado, quiero administrar documentos y mantenimientos desde la interfaz para mantener la operacion actualizada.

Criterios de aceptacion:

- Se pueden consultar documentos por unidad.
- Se pueden consultar mantenimientos proximos.
- Los estados documentales usan valores normalizados.
- Las acciones criticas muestran confirmacion visual.

Prioridad: Media.

## Sprint 0 recomendado

Objetivo: cerrar requerimientos y preparar desarrollo sin escribir todavia backend o frontend productivo.

Tareas:

- Validar esta carpeta `context/necesidades` con el humano.
- Confirmar responsable real de altas de unidades.
- Solicitar a Angel y Roberto scripts, capturas o archivos de roles actuales.
- Confirmar campos obligatorios para alta minima de unidad.
- Confirmar reglas de mantenimiento por dias y kilometraje.
- Definir permisos iniciales por rol.
- Definir vistas iniciales, navegacion y permisos visuales del frontend administrativo.
- Validar la direccion visual con base en las capturas de referencia.
- Definir contratos API necesarios para las primeras pantallas.
- Preparar historias seleccionadas para Sprint 1.

## Sprint 1 recomendado

Objetivo: construir base tecnica fullstack: API central y frontend administrativo minimo.

Historias sugeridas:

- HU-04 Inicio de sesion centralizado.
- HU-05 Validacion de token por aplicaciones.
- HU-06 Administracion de roles y permisos.
- HU-01 Catalogo global de unidades.
- HU-02 Consulta de unidades disponibles.
- HU-15 Estructura visual administrativa.
- HU-16 Inicio de sesion visual.
- HU-18 Administracion visual de unidades.

Dependencias:

- Validacion humana de modelo de dominio.
- Confirmacion de campos minimos.
- Confirmacion de roles iniciales.
- Confirmacion de permisos por vista y accion.
- Base PostgreSQL disponible.
- Contratos de API definidos para autenticacion y unidades.

## Criterios de cierre del primer ciclo documental

- Todos los documentos de `context/necesidades` existen.
- Las necesidades de reuniones estan trazadas a requerimientos o pendientes.
- Los pendientes criticos estan identificados.
- El humano valida si el desarrollo puede pasar a Sprint 1.
