# Necesidades de negocio

## Resumen

SMT necesita una fuente centralizada para administrar unidades, disponibilidad, estados operativos, mantenimiento, documentacion vehicular y acceso por usuarios. Las aplicaciones de turismo, ATAH, Oaxaca, tracto, transporte de personal, fletes, taller y mantenimiento deben consultar una misma fuente de verdad en lugar de mantener inventarios aislados.

## Problema principal

Actualmente existen flujos y aplicaciones que tratan las unidades como informacion propia de cada modulo. Esto genera riesgo de duplicidad, datos desactualizados, diferencias entre areas y exposicion innecesaria de informacion privada.

La informacion de unidades tambien se maneja parcialmente en Excel o en registros separados, por ejemplo kilometraje, mantenimientos y documentacion. Esto obliga a las areas a buscar manualmente los datos que les corresponden y dificulta saber si una unidad esta disponible, en taller, proxima a mantenimiento o fuera de servicio.

## Necesidades detectadas
no vamos a implementar nada sobre taller ni tampoco sobre viajes solamente vamos a hacer la implementación completa sobre la administración de inventario de unidades no queremos ahorita implementar nada de taller solamente se va a poder modificar el estado de si están si se encuentra en taller o está descompuesta esta información debe de ser disponible para modificar solamente si está disponible en taller en mantenimiento fuera del servicio o está intacta esta información se va a mantenerse pero no quiero mantener nada de de procesos relacionados con la administración de taller solamente quiero que sea un estado no como la unidad de negocio precisamente como lo planteaste además de ello necesitaré que las necesidades estén contempladas
### Fuente unica de unidades

- Centralizar autos, trailers, autobuses, camiones, camionetas, micros y otros tipos de unidades en un catalogo global.
- Permitir que cada sistema consulte las unidades necesarias sin ser dueño de la informacion.
- Evitar que turismo, fletes, transporte de personal u otros modulos creen bases de datos aisladas de unidades.
- Mantener informacion historica aunque una unidad quede inactiva o deje de existir.

### Disponibilidad operativa

- Consultar en tiempo real si una unidad esta disponible para ser usada.
- Impedir que unidades en taller, mantenimiento, fuera de servicio o inactivas aparezcan como disponibles.
- Permitir que cada aplicacion filtre unidades segun categoria, capacidad, estado, area o permisos del usuario.

### Taller y mantenimiento

- Tratar taller como proceso o estado de una unidad, no como unidad de negocio al mismo nivel que turismo o fletes.
- Registrar entradas y salidas de taller, reparaciones, mantenimientos preventivos y correctivos.
- Permitir que taller actualice el estado de una unidad cuando entra o sale de mantenimiento.
- Generar alertas de mantenimiento por fecha, kilometraje u otra regla confirmada.

### Odometro y servicios

- Registrar lecturas de odometro para planear mantenimientos.
- Sustituir el control manual en Excel por consultas y reportes personalizados.
- Permitir que diferentes areas consulten solo las unidades que les correspondan.

### Documentacion vehicular

- Registrar numero de unidad, numero economico cuando aplique, marca, tipo, serie, motor, placas, factura, tarjeta de circulacion, numero de poliza, vigencia, verificacion, contaminantes, revision fisico-mecanica y documentos relacionados.
- Controlar quien tiene documentos fisicos o digitales cuando se prestan entre areas.
- Evitar perdida de trazabilidad sobre documentos asociados a cada unidad.
- Normalizar valores heredados del Excel como celdas vacias, `NaN`, `NO TIENE`, `EXCENTO`, fechas en texto y numeros seriales de Excel.

### Usuarios, roles y permisos

- Crear una API central para inicio de sesion, cierre de sesion, usuarios, roles, permisos y validacion de tokens.
- Permitir que las aplicaciones existentes integren esta API para validar acceso.
- Evitar exponer datos de una empresa privada mediante endpoints abiertos.
- Respetar roles existentes de aplicaciones actuales cuando Angel y Roberto compartan scripts, capturas o archivos.

### Administracion global

- Usar como regla inicial un administrador global para dar de alta, modificar y desactivar unidades.
- Evitar que cada area cree unidades sin coordinacion.
- Conservar el numero economico como historial no reutilizable.
- Permitir reasignaciones controladas cuando una unidad de un area se use temporalmente en otra.

## Areas y categorias iniciales

Categorias principales confirmadas para el arranque:

- ATAH.
- Oaxaca.
- Turismo.
- Tracto.
- Transporte de personal.

Areas o procesos relacionados:

- Taller.
- Mantenimiento.
- Cotizaciones.
- Fletes.
- Administracion global.

## Necesidades por persona o area

### Angel

- Consultar estado de unidades cuando estan en taller.
- Ver unidades inutilizables temporal o definitivamente.
- Acceder a informacion general de marca, modelo, placas, numero economico, odometro, seguro, area y operadores asignables.
- Tener acceso amplio por su relacion con taller y mantenimiento.

### Roberto

- Consultar datos necesarios para turismo, Oaxaca y calculos operativos.
- Usar capacidad, tarifa base, sueldo de operador, rendimiento regular, rendimiento bajo, numero de ejes, disponibilidad y estado.
- Integrar la informacion central a su aplicacion sin duplicar unidades.

### Administrador global

- Dar de alta nuevas unidades.
- Mantener datos maestros de cada unidad.
- Desactivar unidades sin reutilizar su numero economico.
- Autorizar cambios criticos, reasignaciones y correcciones.

### Aplicaciones existentes

- Seguir trabajando temporalmente con sus flujos actuales mientras se termina la API central.
- Migrar despues a consumo de unidades existentes desde la API.
- Validar usuarios y tokens contra la API central.

## Reglas de negocio iniciales

- Toda unidad pertenece al inventario global de SMT.
- Ninguna unidad de negocio es dueña absoluta de una unidad desde el punto de vista del sistema central.
- Una unidad en taller, mantenimiento, fuera de servicio o inactiva no debe estar disponible para asignacion operativa.
- El numero economico no se reutiliza.
- Las aplicaciones consumidoras consultan informacion segun permisos.
- Los datos sensibles no se exponen sin autenticacion.
- Las reasignaciones entre areas deben quedar trazadas.

## Alcance del primer ciclo

El primer ciclo consiste en documentacion, backlog y validacion. No incluye todavia creacion de backend, frontend, base de datos, migraciones ni pantallas.
