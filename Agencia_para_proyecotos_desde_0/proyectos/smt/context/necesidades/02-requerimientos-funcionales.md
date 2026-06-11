# Requerimientos funcionales y no funcionales

## Resumen

Este documento formaliza los requerimientos iniciales para el inventario central de unidades y gestion de usuarios de SMT. Los requerimientos deben validarse con el humano antes de iniciar implementacion tecnica.

## Requerimientos funcionales

### RF-01 Catalogo global de unidades

El sistema debe permitir registrar y consultar unidades desde un catalogo global de SMT.

Criterios de aceptacion:

- Cada unidad tiene un identificador interno unico.
- Cada unidad tiene un numero economico unico y no reutilizable.
- Las aplicaciones externas consultan unidades desde la API central.
- Las unidades inactivas permanecen en historial.

### RF-02 Alta de unidades por administrador global

El sistema debe permitir que solo usuarios con rol autorizado creen nuevas unidades.

Criterios de aceptacion:

- Un usuario sin permiso no puede crear unidades.
- El alta requiere datos minimos de identificacion.
- El sistema rechaza numeros economicos duplicados.
- El alta queda trazada con usuario, fecha y origen.

Campos base para alta inicial:

- Numero de unidad.
- Marca.
- Tipo.
- Serie.
- Motor, salvo unidades donde no aplique como cajas o remolques.
- Placas.
- Factura o referencia documental.
- T/C, interpretada inicialmente como tarjeta de circulacion.
- Numero de poliza.
- Vigencia de poliza o estado documental.

Campos complementarios detectados en el parque vehicular:

- Modelo o anio modelo.
- Color.
- Verificacion.
- Contaminantes.
- Fisico-mecanica.
- Costo, pendiente de validar si pertenece al inventario o a un modulo financiero.

### RF-03 Edicion controlada de unidades

El sistema debe permitir actualizar datos maestros de una unidad bajo permisos definidos.

Criterios de aceptacion:

- Solo roles autorizados pueden modificar datos sensibles.
- Cambios de estado, categoria o asignacion quedan auditados.
- No se permite borrar fisicamente una unidad con historial operativo.

### RF-04 Estados de unidad

El sistema debe manejar estados iniciales de unidad.

Estados:

- `disponible`.
- `en_taller`.
- `en_mantenimiento`.
- `fuera_servicio`.
- `inactiva`.

Criterios de aceptacion:

- Solo unidades `disponible` aparecen para uso operativo.
- Una unidad `en_taller` no puede asignarse a turismo, fletes, ATAH, Oaxaca, tracto ni transporte de personal.
- Una unidad `inactiva` permanece consultable en historial.

### RF-05 Categorias de unidad

El sistema debe clasificar unidades por categoria operativa.

Categorias iniciales:

- `ATAH`.
- `oaxaca`.
- `turismo`.
- `tracto`.
- `transporte_personal`.

Criterios de aceptacion:

- La categoria permite filtrar unidades por area o aplicacion consumidora.
- La categoria puede cambiarse solo por rol autorizado.
- Los cambios de categoria quedan registrados.

### RF-06 Consulta por disponibilidad

El sistema debe exponer consultas de unidades disponibles.

Criterios de aceptacion:

- La consulta excluye unidades no disponibles.
- La consulta respeta permisos del usuario.
- La respuesta puede filtrarse por categoria, capacidad, area o atributos tecnicos confirmados.

### RF-07 Reasignacion temporal de unidades

El sistema debe permitir registrar que una unidad sea usada temporalmente por otra area.

Criterios de aceptacion:

- La reasignacion registra area origen, area destino, motivo, fechas y usuario responsable.
- La unidad conserva su historial de pertenencia o categoria previa.
- Las reasignaciones vencidas o finalizadas dejan de afectar disponibilidad operativa.

### RF-08 Registro de taller

El sistema debe permitir marcar una unidad como enviada a taller.

Criterios de aceptacion:

- Al entrar a taller, la unidad cambia a `en_taller`.
- La unidad deja de aparecer en consultas de disponibilidad.
- Se registra motivo, fecha, responsable y observaciones.
- Al salir de taller, la unidad puede volver a `disponible` si no tiene bloqueo adicional.

### RF-09 Mantenimiento y alertas

El sistema debe permitir consultar unidades proximas a mantenimiento.

Criterios de aceptacion:

- Se muestran alertas a 30, 15 y 3 dias cuando exista fecha de mantenimiento.
- Las unidades con 3 dias o menos aparecen como prioridad alta.
- Se debe poder registrar mantenimiento preventivo o correctivo.
- La regla por kilometraje queda pendiente de confirmacion si se usara ademas de fecha.

### RF-10 Lecturas de odometro

El sistema debe permitir registrar lecturas de odometro por unidad.

Criterios de aceptacion:

- Cada lectura registra kilometraje, fecha, usuario y origen.
- La lectura mas reciente puede consultarse desde el resumen de unidad.
- Las lecturas sirven como insumo para mantenimiento.

### RF-11 Seguros y documentacion

El sistema debe registrar informacion documental de cada unidad.

Criterios de aceptacion:

- Se puede registrar poliza, vigencia de poliza, facturas, tarjeta de circulacion y documentos relacionados.
- Se puede registrar verificacion, contaminantes y revision fisico-mecanica como cumplimientos documentales independientes.
- Se puede consultar vencimiento de documentos.
- Se puede registrar prestamo o ubicacion de tarjeta de circulacion cuando aplique.
- El sistema diferencia `pendiente`, `no_tiene`, `no_aplica`, `en_unidad` y estados equivalentes para evitar valores ambiguos heredados del Excel.

### RF-12 Usuarios centralizados

El sistema debe permitir administrar usuarios desde una fuente central.

Criterios de aceptacion:

- Se puede crear, editar, activar y desactivar usuarios.
- Cada usuario tiene roles y permisos asociados.
- Las aplicaciones consumidoras no deben mantener identidades incompatibles con la API central.

### RF-13 Inicio y cierre de sesion

El sistema debe permitir inicio y cierre de sesion mediante API central.

Criterios de aceptacion:

- El inicio de sesion devuelve un token valido.
- El cierre de sesion invalida el token si se implementa lista de sesiones o revocacion.
- Las aplicaciones consumidoras validan el token antes de permitir operaciones.

### RF-14 Validacion de tokens

El sistema debe exponer validacion de token para aplicaciones integradas.

Criterios de aceptacion:

- Un token invalido o vencido rechaza la operacion.
- La validacion devuelve usuario, roles y permisos necesarios para la aplicacion.
- Ninguna consulta privada funciona sin token valido.

### RF-15 Reportes personalizados

El sistema debe permitir reportes filtrados por area, categoria, disponibilidad o permisos.

Criterios de aceptacion:

- Cada area recibe solo las unidades que debe consultar.
- El reporte puede servir como reemplazo de busquedas manuales en Excel.
- Los filtros iniciales se documentan y se amplian despues de validar necesidades por area.

### RF-16 Frontend administrativo

El sistema debe incluir una interfaz visual administrativa para operar y supervisar el inventario central.

Criterios de aceptacion:

- El usuario puede iniciar sesion desde una vista visual conectada a la API central.
- El frontend permite administrar unidades, documentos, mantenimientos, usuarios, roles y permisos segun autorizacion.
- El tablero muestra informacion operativa relevante: unidades por estado, mantenimientos proximos, documentos pendientes o vencidos y unidades no disponibles.
- Las vistas consumen la API mediante servicios centralizados con Axios.
- Las acciones visibles en frontend respetan permisos, sin reemplazar las validaciones del backend.
- Los formularios de unidad aplican los campos base y complementarios documentados para el parque vehicular.
- Las notificaciones visuales se muestran con Sonner y los iconos con Lucide React.

## Requerimientos no funcionales

### RNF-01 Arquitectura

El backend debe usar Node.js 22 LTS, Express.js, TypeScript, PostgreSQL y Prisma bajo Clean Architecture, dominio limpio y arquitectura hexagonal.

### RNF-02 Frontend

El frontend debe usar React, TypeScript, Tailwind CSS, Lucide React, Sonner, Zustand, Axios y React Router DOM bajo Atomic Design y modulos funcionales.

### RNF-03 Seguridad

Toda API privada debe requerir autenticacion por token y validacion de permisos.

### RNF-04 Privacidad

Las respuestas deben exponer solo los datos necesarios segun rol, permiso y aplicacion consumidora.

### RNF-05 Trazabilidad

Altas, cambios de estado, modificaciones criticas, reasignaciones y cierres de mantenimiento deben registrar usuario, fecha y motivo cuando aplique.

### RNF-06 Integridad

El numero economico no debe reutilizarse. Las unidades con historial no se eliminan fisicamente; se desactivan o marcan como inactivas.

### RNF-07 Idioma

Documentacion, carpetas, archivos, variables, funciones, clases, tipos, errores, mensajes y semillas deben mantenerse en espanol salvo restricciones tecnicas inevitables.

### RNF-08 Validacion humana

Requerimientos, cambios de base de datos, permisos, dependencias relevantes y entregables finales requieren validacion humana antes de considerarse cerrados.
