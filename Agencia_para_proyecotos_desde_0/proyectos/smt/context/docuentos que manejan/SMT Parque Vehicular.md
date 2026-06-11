# SMT Parque Vehicular

Fecha de actualización: 2026-06-10

## Propósito del documento

Este documento describe cómo debe interpretarse y capturarse la información del parque vehicular de SMT dentro del sistema central de inventario de unidades.

La información proviene del archivo `SMT Parque Vehicular.xlsx`, el cual contiene registros operativos separados por tipo de unidad. El Excel se usa como fuente de referencia, pero la documentación no debe replicar sus tablas fila por fila. El objetivo de este Markdown es transformar esa información en reglas claras de captura, normalización y validación para nuevas unidades.

## Alcance

El sistema debe permitir registrar unidades vehiculares y equipos asociados al parque vehicular de SMT, incluyendo:

- Coches.
- Camionetas.
- Midibuses.
- Micros.
- Buses.
- Tractos.
- Cajas o remolques.
- Unidades identificadas dentro de ATAH.

La unidad debe entenderse como una entidad global del inventario de SMT. El tipo, grupo o área de operación sirve para clasificarla y consultarla, pero no convierte a cada aplicación en dueña de la información.

## Estructura detectada en el Excel

El archivo analizado contiene seis hojas principales:

- `COCHES`.
- `CAMIONETAS`, con una sección adicional de `MIDIBUS`.
- `MICROS`.
- `BUSES`.
- `TRACTOS`, con una sección adicional de `CAJAS`.
- `ATAH`, con secciones de unidades integrales, convencionales de chasis y camionetas.

Las hojas comparten una base común de información, pero no todas tienen exactamente los mismos campos. Por ejemplo, coches incluye `COLOR` y `VERIFICACION`; camionetas y tractos incluyen `CONTAMINANTES` y `FÍSICO-MECÁNICA`; cajas no tienen `MOTOR`; ATAH agrega un campo de `COSTO` en algunos registros.

Por esta razón, el sistema debe manejar campos base obligatorios y campos complementarios opcionales según el tipo de unidad.

## Información base para crear una unidad

Al dar de alta una nueva unidad, el sistema debe solicitar como mínimo los campos siguientes.

| Campo | Descripción | Reglas de llenado |
| --- | --- | --- |
| Número de unidad | Identificador operativo de la unidad dentro del parque vehicular. En el Excel puede aparecer como `NO`, `NO. ECO` o número económico según la hoja. | Debe capturarse sin modificar ceros iniciales. No debe reutilizarse si la unidad queda inactiva o fuera de operación. |
| Marca | Fabricante de la unidad. | Capturar el nombre comercial en mayúsculas o en formato normalizado definido por el sistema. Ejemplos detectados: VOLKSWAGEN, MERCEDES BENZ, VOLVO, DINA, FREIGHTLINER. |
| Tipo | Línea, clase o configuración de la unidad. | Debe describir el tipo real de unidad, por ejemplo VENTO, SPRINTER, HIACE, ZAFIRO, INTEGRAL, CASCADIA o CAJA SECA. |
| Serie | Número de serie o VIN. | Debe ser único cuando exista. Si el dato no se tiene, debe registrarse como pendiente y no dejarse como `NaN` o celda vacía. |
| Motor | Número de motor o referencia equivalente. | Obligatorio para unidades motorizadas cuando exista. En cajas o remolques puede marcarse como no aplica. |
| Placas | Placa vehicular vigente o última placa registrada. | Debe capturarse sin espacios innecesarios. Si la unidad aún no tiene placas, registrar el estado como pendiente. |
| Factura | Información documental de factura. | Puede representar folio, emisor, propietario, ubicación o referencia documental según el dato disponible. Debe validarse el significado exacto antes de automatizarlo como folio único. |
| T/C | Tarjeta de circulación o estado documental asociado. | Se interpreta inicialmente como tarjeta de circulación. Valores detectados: ORIGINAL, CERTIFICADA, SIMPLE, EN UNIDAD, NO, NO TIENE. Debe normalizarse a un catálogo. |
| Número de póliza | Número de póliza de seguro asociada a la unidad. | Si no existe, registrar `no_tiene`. Si está pendiente de confirmación, registrar `pendiente`. |
| Vigencia | Fecha de vencimiento de póliza u obligación documental indicada en la columna. | Debe registrarse en formato `AAAA-MM-DD`. Los números seriales de Excel deben convertirse a fecha real antes de guardarse. |

## Campos complementarios detectados

Además de la información base, el Excel contiene campos que deben considerarse para el modelo del sistema.

| Campo | Uso recomendado |
| --- | --- |
| Modelo | Año modelo de la unidad. Debe guardarse como año numérico cuando el dato represente un año. |
| Color | Dato descriptivo usado principalmente en coches. |
| Verificación | Periodo, fecha o estado de verificación. Puede contener valores como `VENCIDA`, `NO TIENE` o periodos como `FEB - MAR 2026`. |
| Contaminantes | Periodo, fecha, estado o exención relacionada con cumplimiento ambiental. |
| Físico-mecánica | Periodo, fecha, estado o exención de revisión físico-mecánica. |
| Costo | Campo detectado en ATAH. Su uso exacto debe validarse antes de convertirlo en dato obligatorio. |
| Grupo documental | Identifica si el registro proviene de coches, camionetas, midibus, micros, buses, tractos, cajas o ATAH. |

## Reglas de normalización

### Valores vacíos

No se deben guardar valores como `NaN`, celdas vacías sin significado o textos ambiguos. El sistema debe distinguir entre:

- `pendiente`: el dato se requiere, pero aún no se conoce.
- `no_tiene`: la unidad no cuenta con ese documento, póliza o dato.
- `no_aplica`: el dato no corresponde al tipo de unidad, por ejemplo motor en una caja seca.
- `en_unidad`: el documento físico se encuentra dentro de la unidad.
- `en_bodega`: el documento físico o evidencia se encuentra resguardado en bodega.

### Fechas

El Excel mezcla fechas escritas como texto y números seriales propios de Excel. Antes de guardar una vigencia, el sistema debe convertirla a una fecha real en formato `AAAA-MM-DD`.

Ejemplos de conversión detectados:

| Valor en Excel | Fecha normalizada |
| --- | --- |
| `45986` | `2025-11-25` |
| `46257` | `2026-08-23` |
| `46417` | `2027-01-30` |
| `46969` | `2028-08-04` |
| `47254` | `2029-05-16` |

Si el campo contiene un periodo textual, como `ENERO - JUNIO 2026`, `MAYO-AGOSTO 2026` o `FEB - MAR 2026`, debe guardarse como periodo documental y no como fecha exacta, salvo que el área responsable defina una regla de vencimiento.

### Catálogos recomendados

El sistema debe evitar captura libre cuando existan valores repetibles. Se recomiendan catálogos iniciales para:

- Tipo de unidad: coche, camioneta, midibus, micro, bus, tracto, caja.
- Grupo operativo o documental: SMT, ATAH u otra clasificación confirmada.
- Estado de tarjeta de circulación: original, certificada, simple, en unidad, no tiene, pendiente.
- Estado documental: vigente, vencida, no tiene, exento, pendiente, no aplica.
- Tipo de revisión: verificación, contaminantes, físico-mecánica.

## Reglas para alta de nuevas unidades

1. El usuario autorizado debe seleccionar el tipo de unidad.
2. El sistema debe solicitar los campos base obligatorios.
3. El sistema debe mostrar campos complementarios según el tipo de unidad.
4. El número de unidad o número económico debe validarse contra el inventario global para evitar duplicidad.
5. La serie debe validarse como dato único cuando exista.
6. Las fechas deben normalizarse antes de guardar.
7. Los documentos no disponibles deben registrarse con un estado claro, no con celdas vacías.
8. La unidad debe crearse inicialmente con estado operativo definido, por ejemplo `disponible`, `en_taller`, `en_mantenimiento`, `fuera_servicio` o `inactiva`.
9. Toda alta debe registrar usuario responsable, fecha de captura y fuente de información.
10. Si la información viene de Excel, debe conservarse una referencia de importación para auditoría.

## Reglas por tipo de unidad

### Coches

Los coches usan el número de registro de la hoja como identificador de referencia cuando no existe número económico separado. Deben capturarse marca, tipo, serie, motor, modelo, placas, color, factura, T/C, póliza, vigencia y verificación.

Observación: algunos registros no tienen póliza, vigencia o verificación. Estos casos deben registrarse como `no_tiene` o `pendiente` según corresponda.

### Camionetas

Las camionetas incluyen número económico, marca, tipo, serie, motor, modelo, placas, factura, T/C, póliza, vigencia, contaminantes y físico-mecánica.

Observación: dentro de esta hoja existe una sección de midibus con la misma estructura. El sistema debe permitir clasificar estas unidades como `midibus` aunque provengan de la hoja de camionetas.

### Micros

Los micros incluyen número económico, marca, tipo, serie, motor, modelo, placas, factura, T/C, póliza y vigencia.

Observación: algunos números económicos aparecen como `?` o con póliza/vigencia vacía. Esos registros deben tratarse como incompletos y requerir validación antes de importación definitiva.

### Buses

Los buses integrales incluyen número económico, marca, tipo, serie, motor, modelo, placas, factura, T/C, póliza y vigencia.

Observación: varios vencimientos aparecen como números seriales de Excel. Deben convertirse antes de guardar.

### Tractos

Los tractos incluyen número económico, marca, tipo, serie, motor, modelo, placas, T/C, póliza, vigencia, físico-mecánica y contaminantes.

Observación: se detectan estados como `EXCENTO` en revisiones. El sistema debe aceptar exención como estado documental controlado.

### Cajas

Las cajas o remolques se encuentran dentro de la hoja de tractos. Incluyen número económico, marca, tipo, serie, modelo, placas, factura, físico-mecánica, póliza y vencimiento.

Regla específica: el campo motor no aplica para cajas, salvo que se defina otra clasificación técnica.

### ATAH

La hoja ATAH contiene unidades integrales, convencionales de chasis y camionetas. Usa campos similares a buses y camionetas, con el campo adicional `COSTO` en algunos registros.

Observación: debe validarse si ATAH es una categoría operativa, una empresa, una fuente documental o una combinación de estas. Mientras no se confirme, debe conservarse como grupo documental y no sustituir el tipo de unidad.

## Requerimientos documentales derivados

- El sistema debe permitir registrar documentos por unidad sin limitarse a póliza o factura.
- Una unidad puede tener varios documentos asociados, cada uno con tipo, estado, vigencia, ubicación y responsable.
- La tarjeta de circulación debe manejarse como documento trazable porque puede estar en unidad, bodega o bajo resguardo de una persona.
- La póliza de seguro debe manejarse con número, vigencia y estado.
- Las revisiones de verificación, contaminantes y físico-mecánica deben manejarse como documentos o cumplimientos independientes.

## Validaciones mínimas del formulario

El formulario de alta debe validar:

- Número de unidad requerido.
- Marca requerida.
- Tipo requerido.
- Serie requerida para vehículos y remolques cuando exista.
- Motor requerido solo para unidades motorizadas.
- Placas requeridas o estado pendiente documentado.
- Póliza y vigencia opcionales, pero con estado documental obligatorio.
- T/C con valor normalizado.
- Vigencia en formato válido cuando exista fecha exacta.
- Rechazo de números económicos duplicados.
- Rechazo de series duplicadas cuando la serie esté capturada.

## Observaciones y puntos pendientes

- Confirmar el significado exacto de `T/C`; se interpreta inicialmente como tarjeta de circulación por el contexto documental.
- Confirmar si `NO` y `NO. ECO` deben almacenarse como campos separados o si ambos representan el número de unidad según el tipo de hoja.
- Confirmar si `FACTURA` representa folio, propietario, emisor, ubicación física o archivo relacionado.
- Confirmar si `COSTO` de ATAH debe formar parte del inventario o de un módulo financiero separado.
- Confirmar si `CONTAMINANTES`, `FÍSICO-MECÁNICA` y `VERIFICACION` deben generar alertas automáticas por vencimiento.
- Confirmar reglas para registros incompletos, por ejemplo unidades sin número económico, sin placas, sin póliza o con valor `?`.
- Confirmar si cajas/remolques deben manejarse como unidades independientes o como equipos vinculables a tractos.
- Confirmar si ATAH debe ser área, categoría, empresa, grupo documental o unidad de negocio.
- Definir una estrategia de importación del Excel para convertir fechas, limpiar valores vacíos y evitar duplicados.

## Relación con el inventario central

Esta documentación complementa los requerimientos del inventario central de unidades. Los campos aquí definidos deben incorporarse al modelo de dominio, al formulario de alta y a las reglas de importación cuando se inicie el desarrollo técnico.

La información sigue siendo incompleta para una implementación definitiva. Antes de construir base de datos y pantallas finales, se requiere validar los campos pendientes con las personas responsables del parque vehicular y con el administrador global de unidades.
