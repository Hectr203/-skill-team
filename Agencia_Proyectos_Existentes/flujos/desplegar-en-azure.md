# Flujo de Azure para Proyectos Existentes

## Objetivo

Desplegar un repositorio de tecnología desconocida sin imponer arquitectura y conservando el orden análisis, propuesta, corrección, infraestructura, despliegue, validación y documentación.

## Fase 1: Analizar sin modificar

1. Confirmar objetivo, repositorio, entorno y alcance.
2. Consultar la memoria independiente y documentación existente.
3. Activar `agente-analisis-proyecto-existente`.
4. Aplicar el descubrimiento de `despliegue-azure-proyecto-existente`.
5. Mapear todos los componentes, tecnologías, arquitectura, datos, artefactos, inicio, variables, red y dependencias.
6. Presentar evidencia, desconocidos, riesgos y estado de preparación.

No modificar archivos, instalar dependencias, autenticarse en Azure ni crear recursos en esta fase.

## Fase 2: Proponer y aprobar

1. Activar `agente-arquitectura`, `agente-despliegue-azure` y especialistas necesarios.
2. Comparar opciones Azure por componente.
3. Conservar tecnologías y arquitectura salvo incompatibilidad demostrada.
4. Presentar infraestructura, costo relativo, red, identidad, migración, observabilidad y rollback.
5. Obtener aprobación humana antes de cualquier mutación.

## Fase 3: Preparar el proyecto

1. Aplicar únicamente correcciones aprobadas.
2. Validar build, inicio, artefactos, health, CORS, variables, persistencia y migraciones.
3. Ejecutar pruebas de regresión.
4. Repetir la evaluación de preparación.

No continuar con bloqueantes abiertos.

## Fase 4: Crear infraestructura y desplegar

1. Consultar cuenta, suscripción, proveedores, ubicación, SKU y recursos existentes.
2. Crear y configurar infraestructura exclusivamente con comandos directos `az`.
3. Verificar cada comando antes del siguiente.
4. Desplegar datos, servicios y frontend en el orden derivado del proyecto.
5. Ejecutar migraciones aprobadas con backup y rollback definidos.

## Fase 5: Validar y documentar

1. Verificar recursos y configuración efectiva.
2. Verificar logs, salud y conectividad de dependencias.
3. Probar flujos externos, CORS, rutas, datos, jobs y tiempo real aplicables.
4. Corregir o revertir fallos críticos.
5. Solo entonces activar `agente-documentacion` para escribir la guía final con comandos y resultados reales.
6. Registrar cierre y memoria del proyecto sin secretos.

## Criterio de cierre

La entrega queda bloqueada si falta evidencia del análisis, existe una compuerta incumplida, la aplicación no funciona integrada o la documentación no coincide con el estado desplegado.
