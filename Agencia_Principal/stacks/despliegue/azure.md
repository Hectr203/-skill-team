# Perfil de despliegue Azure

Aplicar únicamente cuando el proyecto selecciona Azure. El perfil de aplicación y el manifiesto definen lenguajes, servicios, requisitos, presupuesto y entorno; no se sustituye el stack del proyecto.

## Infraestructura y operación
Conservar la elección documentada de Bicep como infraestructura declarativa y Azure Developer CLI (`azd`) para proyectos que ya la adopten. Mantener `azure.yaml` en la raíz operativa y archivos de infraestructura en la ubicación del proyecto —por ejemplo `infraestructura/main.bicep`—. No crear hooks o pipelines si no son necesarios. Si existe otra infraestructura aprobada, conservarla y documentar diferencias antes de migrar.

Consultar ayuda/documentación oficial de la versión instalada para comandos de inicialización, entorno, aprovisionamiento, despliegue y selección de servicio. No ejecutar comandos de ejemplo como recetas universales ni inicializar sobre archivos existentes sin revisar consecuencias. La CLI `az` puede apoyar diagnóstico y operaciones acotadas.

## Fases y controles
Diseñar servicios por requisitos y capacidad operativa; presentar costo estimado y límites, usando presupuesto ya acordado o preguntando si falta y es necesario. Preparar artefactos, variables referenciadas, permisos, migraciones y recuperación. Ejecutar operaciones solo dentro de la autorización concreta vigente y comprobar resultados por servicio.

Entregar diseño o estado desplegado según la fase autorizada, comandos realmente ejecutados, controles externos y plan de recuperación. No declarar recursos provisionados por tener Bicep válido ni exigir un despliegue para cerrar una tarea de diseño.
