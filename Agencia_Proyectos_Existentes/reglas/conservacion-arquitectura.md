# Conservacion de Arquitectura Existente

## Objetivo
Evitar que los agentes sustituyan una estructura funcional por una preferencia generica.

## Conservar cuando
- La arquitectura actual resuelve el problema sin deuda critica.
- Hay patrones repetidos y consistentes en el proyecto.
- El cambio solicitado cabe en modulos existentes.
- La reestructuracion aumentaria el riesgo sin beneficio claro.
- No hay aprobacion humana para una migracion estructural.

## Adaptar cuando
- Existe una convencion local que debe extenderse a un nuevo caso.
- El modulo necesita una variacion menor para integrarse con una funcionalidad nueva.
- La tecnologia actual tiene una forma recomendada de resolver el problema dentro del mismo stack.

## Extender cuando
- Falta una pieza nueva pero la arquitectura ya tiene un lugar natural para ubicarla.
- Hay interfaces, servicios, componentes o repositorios existentes que pueden crecer sin romper contratos.

## Refactorizar cuando
- El codigo impide cumplir el requerimiento con seguridad.
- Existe duplicacion que ya provoca errores.
- Hay acoplamiento que bloquea pruebas o cambios necesarios.
- El comportamiento puede conservarse y verificarse.

## Reemplazar solo cuando
- La solucion actual es insegura, incorrecta o imposible de mantener.
- Existe evidencia tecnica, pruebas o incidentes.
- Hay plan de migracion y rollback.
- El humano valida el alcance.
