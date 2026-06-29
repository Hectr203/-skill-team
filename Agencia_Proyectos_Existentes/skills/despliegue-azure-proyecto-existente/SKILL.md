---
name: despliegue-azure-proyecto-existente
description: Analizar y desplegar en Azure proyectos existentes con tecnologías, arquitectura y base de datos inicialmente desconocidas. Usar al evaluar preparación cloud, diseñar infraestructura, corregir bloqueantes, desplegar o documentar un repositorio existente, obligando el orden análisis de solo lectura, propuesta aprobada, infraestructura y despliegue mediante Azure CLI, validación y documentación final.
---

# Desplegar un proyecto existente en Azure

## Núcleo obligatorio

Leer y aplicar `../../../deploy-azure-cli/SKILL.md` y sus referencias junto con las reglas de conservación de la agencia. Este adaptador hace más estricta la fase de descubrimiento; no impone el stack de la agencia de proyectos nuevos.

Si la ruta compartida no está disponible, detener el despliegue y reportar la dependencia.

## Orden inalterable

1. analizar el proyecto completo en modo de solo lectura;
2. presentar arquitectura, tecnologías, requisitos, riesgos y desconocidos;
3. proponer opciones Azure y obtener aprobación;
4. corregir bloqueantes aprobados y volver a validar;
5. crear y configurar infraestructura exclusivamente con comandos directos `az`;
6. desplegar componentes y datos en el orden de dependencias;
7. validar el sistema completo;
8. crear o actualizar la documentación operativa con resultados reales.

No crear infraestructura ni escribir la guía final de despliegue antes de completar el análisis. La evaluación y el plan previos pueden documentarse como artefactos temporales claramente marcados, pero no deben presentarse como infraestructura ejecutada.

## Descubrimiento obligatorio

Trabajar con `agente-analisis-proyecto-existente` y mapear:

- componentes, lenguajes, frameworks y versiones;
- arquitectura, fronteras y protocolos;
- build, artefactos, inicio, puertos y health checks;
- frontend estático, SSR o dinámico;
- base de datos, ORM, migraciones, semillas y persistencia;
- workers, jobs, tiempo real, almacenamiento y servicios externos;
- variables de build/runtime y secretos sin revelar valores;
- CI/CD e infraestructura existentes;
- requisitos no funcionales, red, región, disponibilidad y costo.

Cada conclusión debe tener evidencia. Usar `CONFIRMADO`, `INFERIDO`, `DESCONOCIDO` o `CONFLICTIVO`.

## Conservación

- No reemplazar framework, ORM, base de datos o arquitectura para acomodarlos a un servicio Azure preferido.
- Seleccionar Azure compatible con el proyecto. Proponer cambios de aplicación solo ante incompatibilidad demostrada o mejora aprobada.
- Si existe infraestructura Azure, consultar y preservar recursos antes de planear modificaciones.
- Separar remediaciones necesarias de refactorizaciones opcionales.

## Compuertas

- **A — Descubrimiento completo:** no hay desconocidos críticos sobre build, inicio, datos, red o secretos.
- **B — Propuesta aprobada:** servicio, costo, región, seguridad, migración y rollback están aceptados.
- **C — Preparación validada:** build y pruebas pasan; bloqueantes están cerrados.
- **D — Infraestructura verificada:** cada comando `az` tiene resultado y comprobación.
- **E — Sistema validado:** comunicación, datos, CORS, rutas, jobs y observabilidad funcionan.
- **F — Documentación final:** refleja únicamente el estado realmente desplegado.

Detenerse en la primera compuerta incumplida.

## Entregables

- informe de descubrimiento con evidencia;
- matriz de compatibilidad y alternativas Azure;
- correcciones aprobadas;
- plan y registro de comandos directos `az`;
- infraestructura y despliegue verificados;
- documentación operativa final y rollback;
- memoria independiente actualizada sin secretos.
