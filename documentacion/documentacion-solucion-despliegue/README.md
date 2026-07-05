# Documentación de Solución y Despliegue — VTP Transporte

Esta carpeta contiene la documentación técnica completa del proyecto **VTP Transporte**, enfocada en el diagnóstico y la resolución de los problemas de CORS (Cross-Origin Resource Sharing) en producción, la descripción de la arquitectura, la infraestructura como código con Bicep, los scripts de base de datos y automatización, y el procedimiento detallado para desplegar el sistema.

---

## Objetivo de la Documentación

El propósito de esta documentación es recopilar el conocimiento técnico del proyecto y proporcionar una guía exhaustiva para que cualquier desarrollador pueda:
1. Comprender el problema de CORS experimentado en producción y su causa raíz.
2. Analizar y replicar la solución implementada.
3. Entender la arquitectura y los archivos de infraestructura como código (Bicep).
4. Configurar el entorno de desarrollo y producción desde cero.
5. Ejecutar despliegues y migraciones de bases de datos de forma segura.

---

## Alcance

Esta documentación abarca:
- El análisis técnico del problema de CORS y su interacción con Azure App Service y Node.js/Express.
- La arquitectura general de la infraestructura en Azure.
- El uso de Azure Developer CLI (`azd`) y Azure CLI (`az`).
- El catálogo de scripts de migración de bases de datos y la administración de variables de entorno.
- Las lecciones aprendidas y recomendaciones de buenas prácticas para futuras implementaciones.

> [!WARNING]
> **Advertencia sobre Secretos:** En cumplimiento de las políticas de seguridad del proyecto, esta documentación **no contiene ni debe contener** contraseñas, secretos, tokens ni llaves de acceso reales. Todas las configuraciones sensibles están descritas únicamente por su nombre de variable, con ejemplos de valores seguros y ficticios.

---

## Estructura de los Documentos

La documentación se organiza de forma secuencial en los siguientes archivos:

| # | Archivo | Descripción |
|---|---|---|
| 01 | [01-descripcion-y-analisis-del-problema.md](./01-descripcion-y-analisis-del-problema.md) | Detalle de los síntomas y del impacto del fallo de CORS en producción. |
| 02 | [02-identificacion-de-la-causa-raiz.md](./02-identificacion-de-la-causa-raiz.md) | Explicación técnica de por qué ocurrió el fallo en la interacción Express-Azure. |
| 03 | [03-solucion-implementada.md](./03-solucion-implementada.md) | Resumen del enfoque adoptado, ventajas, limitaciones y alternativas evaluadas. |
| 04 | [04-proceso-de-implementacion.md](./04-proceso-de-implementacion.md) | Cambios exactos en archivos, parámetros de infraestructura y pasos seguidos. |
| 05 | [05-arquitectura-utilizada.md](./05-arquitectura-utilizada.md) | Modelo general del sistema, flujos de red, diagramas de arquitectura (Mermaid) y ambientes. |
| 06 | [06-herramientas-y-tecnologias.md](./06-herramientas-y-tecnologias.md) | Listado y versiones de los frameworks, lenguajes, CLIs y bases de datos del proyecto. |
| 07 | [07-bicep-configuracion-y-uso.md](./07-bicep-configuracion-y-uso.md) | Estructura detallada del archivo `main.bicep` y directivas de aprovisionamiento en Azure. |
| 08 | [08-scripts-y-comandos.md](./08-scripts-y-comandos.md) | Catálogo de comandos npm, scripts de base de datos y comandos útiles de la CLI de Azure. |
| 09 | [09-variables-configuracion-y-dependencias.md](./09-variables-configuracion-y-dependencias.md) | Tabla exhaustiva de variables de entorno y prerrequisitos del sistema local. |
| 10 | [10-proceso-completo-de-despliegue.md](./10-proceso-completo-de-despliegue.md) | Guía paso a paso para clonar, configurar, aprovisionar y desplegar desde cero. |
| 11 | [11-identificacion-diagnostico-y-solucion-de-errores.md](./11-identificacion-diagnostico-y-solucion-de-errores.md) | Catálogo de errores comunes y conocidos con sus respectivas soluciones. |
| 12 | [12-validaciones-y-resultados.md](./12-validaciones-y-resultados.md) | Pruebas realizadas para comprobar el éxito del sistema (incluye trazas de `curl`). |
| 13 | [13-recomendaciones-para-futuras-implementaciones.md](./13-recomendaciones-para-futuras-implementaciones.md) | Estrategias de mantenimiento continuo, observabilidad y mejores prácticas. |

---

## Orden Recomendado de Lectura

Para desarrolladores nuevos o externos, se sugiere el siguiente flujo de lectura:
1. **Comenzar con la Introducción General:** Leer este [README.md](./README.md) y la sección de [Herramientas y Tecnologías](./06-herramientas-y-tecnologias.md) junto con [Variables y Dependencias](./09-variables-configuracion-y-dependencias.md).
2. **Entender el Caso de Negocio y Arquitectura:** Leer la [Arquitectura Utilizada](./05-arquitectura-utilizada.md) para comprender la interacción entre frontend, backend y base de datos.
3. **Analizar el Fallo de CORS:** Leer secuencialmente desde el [Problema](./01-descripcion-y-analisis-del-problema.md), la [Causa Raíz](./02-identificacion-de-la-causa-raiz.md), la [Solución](./03-solucion-implementada.md) y el [Proceso de Implementación](./04-proceso-de-implementacion.md).
4. **Guías Operativas:** Consultar el [Proceso Completo de Despliegue](./10-proceso-completo-de-despliegue.md), [Bicep](./07-bicep-configuracion-y-uso.md) y los [Scripts](./08-scripts-y-comandos.md) para aprender a operar el sistema.
5. **Mantenimiento y Soporte:** Guardar como referencia rápida las secciones de [Errores Comunes](./11-identificacion-diagnostico-y-solucion-de-errores.md) y [Recomendaciones](./13-recomendaciones-para-futuras-implementaciones.md).

---

## Estado de la Documentación y Referencia

- **Estado actual:** Completo y verificado contra la infraestructura productiva actual.
- **Última revisión realizada:** 19 de Junio de 2026.
- **Entorno de validación:** Azure App Service (`smt-transportes-api`) y Azure Static Web App (`smt-transportes-web`).
- **Contacto del equipo de desarrollo:** creativasoftia@gmail.com
