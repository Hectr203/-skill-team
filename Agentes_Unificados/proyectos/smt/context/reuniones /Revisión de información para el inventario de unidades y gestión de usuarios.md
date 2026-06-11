# Revisión de información para el inventario de unidades y gestión de usuarios

Durante la reunión se abordó la necesidad de definir qué información se requiere de cada unidad o vehículo para iniciar el desarrollo del módulo de inventario de autos y unidades.

Se comentó que existen diferentes tipos de vehículos, por lo que es necesario identificar cómo clasifica la empresa cada tipo de unidad y cómo manejan esa información en su operación. Esta información es importante para realizar cálculos y para construir correctamente el catálogo de vehículos.

Se solicitó a Ángel y Roberto un resumen de la información que necesitan de las unidades para sus respectivas áreas.

## Información requerida por Ángel

Ángel explicó que, para su área, principalmente necesita conocer el estado de las unidades cuando se encuentran en taller. Se mencionó que, cuando un autobús o unidad está en taller, puede quedar inutilizable de forma temporal o definitiva, dependiendo de su condición.

También se identificó que, para el control general de unidades, se requiere registrar información como:

* Marca.
* Modelo.
* Placas.
* Número económico.
* Odómetro.
* Seguro.
* Área a la que pertenece.
* Operadores que se le pueden asignar.

Se aclaró que esta no es necesariamente toda la información, pero sí representa lo más importante para el área. El resto podría manejarse mediante consultas específicas.

## Información requerida por Roberto

Roberto indicó que, para su área, necesita información relacionada con:

* Capacidad de la unidad.
* Tarifa base.
* Sueldo del operador o chofer.
* Rendimiento regular.
* Rendimiento bajo.
* Número de ejes.
* Disponibilidad de la unidad.
* Estado de la unidad.

Se aclaró que el dato de “sueldo” fue planteado originalmente para realizar cálculos, especialmente relacionados con costos de operación, kilometraje y servicios.

También se mencionó que existe una tabla previa con algunos de estos datos, la cual incluye información como:

* Número de automóvil.
* Número económico.
* Marca.
* Tipo.
* Número de serie.
* Número de motor.
* Modelo.
* Placas.
* Facturas.
* Póliza de seguro.
* Vigencia de la póliza.
* Información relacionada con emisiones o contaminantes.
* Datos similares para coches, camionetas y micros.

Con esta información se considera posible comenzar a trabajar el módulo de inventario de unidades.

## Necesidad de una fuente única de información

Se señaló que cada área necesita información específica, pero todas deben consultar una misma fuente de verdad. Aunque las áreas personalizan sus necesidades, la información principal de las unidades debe estar centralizada para evitar duplicidad o inconsistencias.

Por ejemplo, algunas áreas no necesitan conocer el modelo o el operador asignado, sino únicamente el número de serie o datos informativos específicos. Sin embargo, todas deben acceder a la información desde una misma base de datos o API.

Se propuso crear una API centralizada que contenga la información completa de las unidades. A partir de esa API, cada aplicación podrá consultar únicamente los datos que necesite, según el área y los permisos del usuario.

## Administración de usuarios y roles

Se planteó la necesidad de crear un sistema de usuarios centralizado para que cada aplicación pueda iniciar sesión utilizando una misma base de autenticación.

La propuesta consiste en que exista una API para gestionar:

* Inicio de sesión.
* Cierre de sesión.
* Creación de usuarios.
* Roles.
* Validación de tokens.
* Permisos de acceso.

Cada aplicación deberá integrar esta API para validar que el usuario tenga permisos antes de acceder a cierta información.

Se mencionó que no es conveniente dejar la API abierta, ya que se trata de información de una empresa privada. Por ello, se debe proteger el acceso mediante tokens.

La idea es que cada usuario inicie sesión, reciba un token válido y, con ese token, pueda acceder a las consultas permitidas dentro de cada aplicación. El backend de cada sistema deberá validar constantemente que el token siga siendo válido.

También se solicitó a Ángel y Roberto compartir los roles existentes en sus sistemas actuales, ya sea mediante captura, script o archivo, para integrarlos sin romper la lógica de sus aplicaciones.

## Áreas identificadas

Se identificaron distintas áreas o tipos de operación relacionados con las unidades:

* Taller.
* Mantenimiento.
* Turismo.
* Cotizaciones.
* Transporte de personal.
* Fletes.
* ATAH.
* Oaxaca.
* Tracto.

Posteriormente se aclaró que las áreas o tipos de unidades principales son:

* ATAH.
* Oaxaca.
* Turismo.
* Tracto.
* Transporte de personal.

Aunque inicialmente se mencionó que podían ser seis, finalmente se identificaron cinco categorías principales.

## Asignación y disponibilidad de unidades

Se discutió que las unidades pueden pertenecer a un área específica, pero también puede existir dinamismo en su uso. Por ejemplo, una unidad de turismo podría utilizarse temporalmente para transporte de personal si otra unidad se encuentra descompuesta o en taller.

Por ello, se considera necesario que el sistema permita identificar a qué área pertenece una unidad, pero también que contemple posibles reasignaciones según la operación.

Se mencionó que Roberto, por ejemplo, podría tener acceso principalmente a las unidades de turismo y Oaxaca, mientras que Ángel, por trabajar con taller, podría necesitar acceso a todas las unidades.

## Alta de nuevas unidades

Se identificó una duda importante: definir quién será responsable de dar de alta nuevas unidades en el sistema.

Existen dos posibilidades:

1. Que cada área registre sus propias unidades.
2. Que exista una persona responsable de administrar globalmente todas las unidades.

Se consideró que lo más adecuado podría ser contar con una persona encargada de administrar todas las unidades para evitar duplicidad o desorden en la información.

También se mencionó que, si una unidad se descompone o deja de existir, su número económico no debería reutilizarse. Por ejemplo, si la unidad 211 era un Volvo, ese registro debe conservarse para mantener el historial, aunque la unidad ya no esté activa.

Se acordó preguntar a la persona correspondiente si existe alguien encargado de administrar todas las unidades o si cada área registra sus propias unidades cuando llegan vehículos nuevos.

## Flujo propuesto para las aplicaciones

Se planteó que, por ahora, cada equipo continúe trabajando con su flujo actual, incluso si sus aplicaciones permiten registrar unidades.

Sin embargo, una vez que esté lista la API centralizada de unidades, deberán ajustar sus sistemas para dejar de crear unidades localmente y comenzar a consumir la información existente desde la API.

De esta manera, las aplicaciones podrán consultar las unidades registradas sin duplicar información.

El flujo propuesto es el siguiente:

1. El usuario inicia sesión mediante la API central.
2. La API valida sus credenciales.
3. El sistema genera un token de acceso.
4. Cada aplicación utiliza ese token para validar permisos.
5. La aplicación consulta únicamente la información permitida.
6. El backend valida constantemente que el token siga siendo válido.

## Módulo de mantenimiento y notificaciones

También se habló sobre un módulo de mantenimiento para las unidades.

Se comentó que la responsable desea visualizar un historial o listado de unidades próximas a recibir servicio. La prioridad estaría basada en los días restantes para el mantenimiento.

La idea es que, si una unidad está cerca de requerir servicio, el sistema muestre una notificación. Por ejemplo:

* Faltan 15 días para el mantenimiento.
* Faltan 3 días para el mantenimiento.
* La unidad ya requiere mantenimiento.

Se mencionó que las unidades con prioridad de tres días o menos deberían aparecer de forma destacada para que puedan atenderse de inmediato.

También se aclaró que esto dependerá de la información de las unidades y de cómo se registre la fecha de servicio o mantenimiento.

## Problemas identificados

Durante la conversación se identificaron varios problemas que deben resolverse antes de continuar:

* Cada integrante desarrolló partes del sistema sin tener el contexto completo del proyecto.
* Algunas aplicaciones tienen flujos distintos para registrar unidades.
* Puede existir duplicidad de información si cada aplicación maneja su propia base de datos de unidades.
* No está claro quién debe administrar las unidades nuevas.
* Es necesario definir roles y permisos.
* Es necesario proteger la API mediante autenticación y tokens.
* Algunas áreas necesitan información específica que otras áreas no requieren.
* Se deben estandarizar los tipos de unidades y las áreas a las que pertenecen.
* Falta terminar entrevistas o confirmar información con algunas personas responsables.

## Pendientes acordados

Se acordaron los siguientes pendientes:

1. Definir qué información necesita cada área sobre las unidades.
2. Solicitar a Ángel y Roberto los roles existentes en sus aplicaciones.
3. Compartir scripts, capturas o archivos relacionados con usuarios y roles.
4. Crear la base de datos central de unidades.
5. Crear la API para consultar la información completa de las unidades.
6. Crear la API de usuarios, roles, inicio de sesión y validación de tokens.
7. Definir si cada área podrá registrar unidades o si habrá una persona administradora general.
8. Confirmar con la persona correspondiente quién administra las unidades nuevas.
9. Adaptar las aplicaciones existentes para consumir la API central.
10. Definir los permisos de acceso según el rol de cada usuario.
11. Continuar con el desarrollo de los módulos específicos de cada área.
12. Revisar avances con Ángel y Roberto.
13. Integrar el módulo de notificaciones para mantenimientos próximos.

## Conclusión

Se concluyó que es necesario centralizar la información de las unidades y usuarios para evitar duplicidad, inconsistencias y exposición innecesaria de datos.

La prioridad será desarrollar una API central que permita gestionar unidades, usuarios, roles y permisos. Cada aplicación deberá consumir esa API para acceder a la información que le corresponde.

También se acordó que, mientras se termina la API, los equipos podrán continuar trabajando en sus respectivas interfaces o estructuras base. Posteriormente, deberán adaptar sus sistemas para conectarse a la fuente central de información.

Finalmente, se resaltó la importancia de confirmar quién será responsable de administrar las unidades nuevas y cómo se manejarán las reasignaciones entre áreas, ya que esta decisión afectará directamente el diseño de la base de datos y los permisos del sistema.
