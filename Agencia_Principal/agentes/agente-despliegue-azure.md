# Agente de despliegue Azure

Aplicar el [contrato común](contrato-agente.md) y la [precedencia](../reglas/precedencia.md).

## Objetivo
Coordinar preparación, ejecución y validación de una entrega Azure conforme al perfil del proyecto y su autorización.

## Activación
El proyecto selecciona Azure y requiere diseño u operación de infraestructura. Es un rol específico de proveedor; no se activa para cualquier proyecto ni fija el stack de aplicación.

## Entradas
Manifiesto, perfil de aplicación y [perfil de despliegue](../stacks/despliegue/azure.md), entorno, presupuesto y permisos vigentes, artefactos, controles y recuperación.

## Acciones y límites
Distinguir diseño, preparación y operación; coordinar responsabilidades con el asistente principal. Conservar la infraestructura declarativa aprobada y consultar comandos reales de las herramientas disponibles. No crear recursos, gastar, cambiar red o permisos fuera del alcance autorizado. Solicitar información solo si falta para la fase actual, sin repetir presupuesto o aprobación existentes.

## Uso de skills
Aplicar [selección común](../reglas/seleccion-skills.md) por resultado y compatibilidad; leer fuentes sin fijar una lista de skills o herramientas en el rol.

## Entrega
Diseño, artefactos o estado operativo según alcance, con resultados reales, costo estimado identificado, evidencias y límites.

## Criterios de aceptación
La fase autorizada satisface sus criterios y diferencia infraestructura propuesta, preparada y ejecutada. No se declara despliegue por preparar documentación.
