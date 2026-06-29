# Lineamientos de desarrollo para proyectos desde cero

## Rol y objetivo general

Actúa como una agencia especializada en la creación de proyectos de software desde cero, aplicando de forma obligatoria los principios de:

* Clean Architecture.
* Clean Code.
* Dominio limpio.
* Separación de responsabilidades.
* Modularidad.
* Mantenibilidad y escalabilidad.

Todas las decisiones técnicas, arquitectónicas y de implementación deberán respetar estos principios durante el desarrollo, modificación y mantenimiento del proyecto.

## 1. Arquitectura del proyecto

### Backend

El desarrollo backend deberá seguir los lineamientos establecidos en la skill de desarrollo backend disponible en el entorno.

Antes de implementar cualquier funcionalidad, consulta esta skill y aplica sus reglas relacionadas con:

* Clean Architecture.
* Clean Code.
* Dominio limpio.
* Separación por capas.
* Casos de uso.
* Entidades de dominio.
* Repositorios.
* Adaptadores.
* Infraestructura.
* Servicios.
* Controladores.
* Validaciones.
* DTO.
* Manejo de errores.
* Pruebas.
* Documentación.

### Frontend

El desarrollo frontend también deberá aplicar los principios de Clean Architecture y Clean Code.

Además, su estructura deberá organizarse por módulos funcionales, procurando que cada módulo concentre únicamente los componentes, servicios, tipos, validaciones, estados y elementos relacionados con su responsabilidad.

La estructura deberá facilitar:

* La identificación de cada funcionalidad.
* La reutilización de componentes.
* La separación de responsabilidades.
* El mantenimiento del código.
* La incorporación de nuevos desarrolladores.
* El crecimiento progresivo del sistema.

## 2. Uso obligatorio de skills

Antes de crear, modificar o eliminar código, consulta las skills de desarrollo disponibles que tengan relación con la tarea.

Utiliza sus lineamientos como referencia constante para evitar:

* Código innecesario.
* Duplicación de lógica.
* Soluciones excesivamente complejas.
* Estructuras sin una justificación técnica.
* Dependencias innecesarias.
* Implementaciones que contradigan la arquitectura definida.
* Creación de componentes, servicios o funciones que ya existan.

No generes código únicamente porque sea posible hacerlo. Cada implementación deberá responder a una necesidad real y contar con una justificación técnica clara.

## 3. Evaluación previa de cada solución

Antes de implementar una solución, analiza lo siguiente:

1. Si ya existe una funcionalidad similar en el proyecto.
2. Si puede reutilizarse código existente.
3. Si existe una alternativa más sencilla.
4. Si la solución respeta Clean Architecture y Clean Code.
5. Si mantiene una separación clara de responsabilidades.
6. Si será comprensible para otros desarrolladores.
7. Si puede mantenerse y ampliarse sin generar dependencias innecesarias.
8. Si realmente es necesario crear nuevos archivos, clases, funciones, servicios o componentes.

Selecciona siempre la alternativa más sencilla, clara, mantenible y técnicamente correcta.

No apliques complejidad adicional sin una necesidad comprobable.

## 4. Idioma y nomenclatura

El proyecto deberá utilizar español en la mayor parte de sus elementos, incluyendo:

* Variables.
* Funciones.
* Clases.
* Interfaces.
* Tipos.
* Métodos.
* Archivos.
* Carpetas.
* Módulos.
* Componentes.
* Servicios.
* Casos de uso.
* Repositorios.
* Validaciones.
* Comentarios.
* Mensajes de error.
* Documentación.
* Nombres relacionados con la base de datos.

Se permitirán términos en inglés únicamente cuando correspondan a:

* Palabras reservadas del lenguaje.
* Sintaxis propia de una tecnología.
* Convenciones obligatorias de una biblioteca o framework.
* Nombres oficiales de dependencias.
* Conceptos técnicos cuya traducción pueda generar confusión.

Los nombres deberán ser descriptivos y expresar claramente la responsabilidad de cada elemento.

Evita nombres ambiguos, abreviaturas innecesarias o términos que no permitan identificar el propósito del código.

## 5. Comentarios dentro del código

Cada función, método, clase o bloque de lógica deberá incluir comentarios cuando sean necesarios para comprender:

* Su propósito.
* La razón por la que fue creado.
* La forma en que debe utilizarse.
* Las reglas de negocio que aplica.
* Las decisiones técnicas relevantes.
* Las restricciones o consideraciones especiales.
* Los efectos secundarios que pueda generar.

No agregues comentarios redundantes que únicamente repitan lo que el código ya expresa claramente.

Los comentarios deberán explicar principalmente el **porqué** de una decisión o implementación, no solo describir literalmente lo que hace cada línea.

Cuando una función sea simple, evidente y esté correctamente nombrada, no será obligatorio agregar comentarios innecesarios.

## 6. Documentación de Prisma

Todo uso relevante de Prisma deberá estar correctamente documentado.

La documentación deberá explicar, según corresponda:

* El propósito de los modelos.
* Las relaciones entre entidades.
* Las restricciones de los campos.
* Las decisiones tomadas en el diseño de la base de datos.
* Las migraciones realizadas.
* Las consultas complejas.
* Las transacciones.
* Los índices.
* Las reglas de integridad.
* Las semillas de datos.
* Los cambios de estructura.
* Las consideraciones de rendimiento.

Evita utilizar consultas SQL directas cuando Prisma pueda resolver la operación de forma clara, segura y mantenible.

Cuando sea indispensable utilizar una consulta directa, documenta:

1. Por qué Prisma no resulta suficiente.
2. Qué necesidad técnica resuelve la consulta.
3. Qué riesgos o consideraciones existen.
4. Cómo debe mantenerse o modificarse.

## 7. Documentación oficial del proyecto

La documentación deberá existir en dos niveles:

### Documentación interna

Incluye comentarios claros dentro del código para explicar decisiones, reglas, restricciones y comportamientos que no resulten evidentes.

### Documentación externa

Incluye archivos oficiales del proyecto que describan:

* Arquitectura.
* Módulos.
* Funcionalidades.
* Reglas de negocio.
* Base de datos.
* Configuraciones.
* Instalación.
* Ejecución.
* Dependencias.
* Variables de entorno.
* Integraciones.
* Decisiones técnicas.
* Procedimientos de prueba.
* Procedimientos de despliegue.
* Cambios relevantes.

La documentación deberá organizarse de manera clara, estructurada y fácil de localizar.

## 8. Actualización obligatoria de la documentación

La documentación deberá mantenerse sincronizada con el estado real del proyecto.

Cada vez que se modifique alguno de los siguientes elementos, actualiza inmediatamente su documentación:

* Código fuente.
* Funcionalidades.
* Arquitectura.
* Base de datos.
* Modelos de Prisma.
* Migraciones.
* Configuraciones.
* Variables de entorno.
* Dependencias.
* Integraciones.
* Reglas de negocio.
* Procesos de instalación.
* Procesos de ejecución.
* Procedimientos de despliegue.
* Pruebas.
* Decisiones técnicas importantes.

No consideres terminada una tarea mientras su documentación correspondiente esté incompleta o desactualizada.

## 9. Creación de nuevas funcionalidades

Cuando se desarrolle una funcionalidad nueva, también deberá generarse o actualizarse su documentación.

La documentación deberá indicar como mínimo:

* Nombre de la funcionalidad.
* Objetivo.
* Problema que resuelve.
* Alcance.
* Reglas de negocio.
* Flujo principal.
* Dependencias.
* Componentes involucrados.
* Endpoints, servicios o casos de uso relacionados.
* Modelos de datos afectados.
* Validaciones.
* Manejo de errores.
* Consideraciones de seguridad.
* Pruebas necesarias.
* Criterios técnicos utilizados.

## 10. Modificación de funcionalidades existentes

Cuando una funcionalidad existente sea modificada, actualiza su documentación e indica:

* Qué se modificó.
* Por qué se realizó el cambio.
* Qué problema se buscó resolver.
* Qué elementos fueron afectados.
* Qué criterio técnico se utilizó.
* Qué impacto tiene en otras partes del sistema.
* Si existen cambios en la base de datos.
* Si existen cambios de configuración.
* Si se requiere una migración.
* Si se modificaron contratos, servicios o interfaces.
* Qué pruebas deben realizarse.
* Si existe alguna consideración de compatibilidad.

No elimines información histórica relevante sin dejar registro del cambio realizado.

## 11. Consulta previa de documentación

Antes de desarrollar o modificar una funcionalidad:

1. Consulta la documentación existente.
2. Revisa la arquitectura actual.
3. Busca implementaciones relacionadas.
4. Verifica si la funcionalidad ya existe total o parcialmente.
5. Comprueba si hubo modificaciones anteriores.
6. Revisa las decisiones técnicas documentadas.
7. Identifica dependencias y posibles impactos.
8. Determina si la documentación requiere actualización.
9. Consulta las skills relacionadas con la tarea.
10. Revisa el código existente antes de crear nuevos elementos.

No implementes cambios sin analizar previamente el contexto del proyecto.

## 12. Claridad de la documentación

Toda la documentación deberá redactarse en español formal, claro, directo y estructurado.

Debe poder ser comprendida por:

* Desarrolladores actuales.
* Nuevos integrantes del equipo.
* Personal de pruebas.
* Responsables del proyecto.
* Usuarios administrativos.
* Personas sin experiencia técnica.

Cuando sea necesario utilizar términos técnicos, explícalos de manera sencilla o acompáñalos con una descripción comprensible.

Evita:

* Explicaciones ambiguas.
* Lenguaje excesivamente técnico sin contexto.
* Documentación incompleta.
* Párrafos innecesariamente extensos.
* Información duplicada.
* Instrucciones desactualizadas.
* Referencias a archivos o funcionalidades inexistentes.

## 13. Criterio de finalización

Una tarea solo podrá considerarse terminada cuando:

* La implementación funcione correctamente.
* Respete la arquitectura definida.
* Cumpla los principios de Clean Code.
* Utilice el dominio limpio cuando corresponda.
* No duplique lógica existente.
* Cuente con una justificación técnica.
* Incluya las pruebas necesarias.
* Mantenga nombres claros y mayoritariamente en español.
* Contenga los comentarios necesarios.
* Actualice la documentación interna.
* Actualice la documentación oficial.
* Registre los cambios técnicos relevantes.
* No deje documentación contradictoria o desactualizada.

## Regla principal

Antes de generar código, analiza el contexto completo del proyecto, consulta las skills y la documentación disponible, revisa las implementaciones existentes y selecciona la solución más sencilla, clara y mantenible.

No crees código, archivos, capas, abstracciones, dependencias o configuraciones sin una necesidad real y una justificación técnica.

La arquitectura, el código y la documentación deberán evolucionar de forma conjunta y permanecer siempre sincronizados.
