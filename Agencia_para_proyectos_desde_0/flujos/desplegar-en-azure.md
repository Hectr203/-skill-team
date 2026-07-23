# Flujo de Azure para Proyectos Nuevos

## Objetivo

Incorporar Azure desde la arquitectura inicial sin adelantar el aprovisionamiento y desplegar después un sistema validado con la tecnología obligatoria de la agencia.

## Fase 1: Diseñar para ejecución

1. Aprobar requerimientos y arquitectura de software.
2. Confirmar React/TypeScript, Node.js 22/Express/TypeScript y PostgreSQL/Prisma en el manifiesto.
3. Definir perfil de ejecución: SPA/SSR, API, jobs, archivos, tiempo real, tráfico, disponibilidad, región, seguridad y presupuesto.
4. Activar `agente-despliegue-azure` y `despliegue-azure-proyecto-nuevo`.
5. Comparar servicios y registrar la decisión Azure con alternativas y costo relativo.
6. Incorporar contratos de nube al desarrollo: variables, puerto, health, CORS, persistencia, migraciones, identidad y observabilidad.

Esta fase no crea ni modifica recursos Azure.

## Fase 2: Desarrollar y validar

1. Implementar funcionalidades siguiendo la arquitectura aprobada.
2. Mantener actualizada la matriz de variables sin secretos.
3. Ejecutar build, pruebas y migraciones en entorno controlado.
4. Verificar que el artefacto y el proceso de inicio sean reproducibles.
5. Ejecutar las validaciones preventivas del núcleo `deploy-azure-cli`.

## Fase 3: Aprobar y desplegar

1. Presentar estado de preparación, bloqueantes y plan.
2. Obtener aprobación humana para costo, entorno, red, secretos, migraciones y cambios productivos.
3. Crear y configurar Azure, un comando directo `az` por paso.
4. Desplegar datos, backend, frontend y complementos en su orden de dependencia.
5. Verificar cada paso antes de continuar.

## Fase 4: Validar y documentar

1. Verificar plano de administración, aplicación y experiencia externa.
2. Probar frontend→API, CORS, rutas SPA, persistencia, migraciones, jobs y observabilidad aplicables.
3. Ejecutar rollback si falla un criterio crítico.
4. Crear la guía operativa final con los comandos realmente ejecutados, sustituciones, resultados y verificaciones.
5. Actualizar manifiesto, informe de cierre y memoria independiente.

## Criterio de cierre

No cerrar mientras la infraestructura no corresponda a la arquitectura aprobada, falten validaciones críticas o la documentación describa un estado distinto del desplegado.
