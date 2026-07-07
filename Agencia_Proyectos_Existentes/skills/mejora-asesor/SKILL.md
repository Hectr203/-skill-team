---
name: mejora-asesor
description: Skill de mejora y auditoria con dos modelos. Primero /improve con el modelo mas capaz (caro) para analisis, luego ejecuta los planes con modelo barato. Para proyectos existentes, prioriza conservar arquitectura y no romper funcionalidad.
---

# Mejora Asesor para Proyectos Existentes

## Proposito
Aplicar la skill `shadcn/improve` con dos modelos en proyectos existentes, asegurando que las mejoras no rompan la arquitectura ni funcionalidad actual. El modelo caro planifica, el barato ejecuta.

## Diferencia clave con proyectos nuevos
En proyectos existentes, el auditor debe primero entender la arquitectura actual antes de proponer cambios. La regla "la arquitectura existente prevalece" se aplica tambien aqui.

## Integracion con shadcn/improve
Orquesta `shadcn/improve` (en `skills/improve/SKILL.md`). La skill original es read-only; esta skill anade la ejecucion con el modelo economico.

## Flujo adaptado para proyectos existentes

### Fase 1 - Recon con modelo caro
1. Leer README, AGENTS.md, estructura actual, package.json, configs.
2. Identificar framework de pruebas, linter, typechecker.
3. Leer ADRs o documentacion de arquitectura si existen.
4. NO asumir que el stack tecnico es el mismo que el de la agencia.

### Fase 2 - Audit con modelo caro
1. Ejecutar audit completo con `improve`.
2. Categorizar hallazgos como:
   - **BUG/SEGURIDAD** - Prioridad maxima.
   - **MEJORA** - Sin riesgo de ruptura.
   - **REFACTOR** - Con riesgo potencial, requiere validacion.
   - **DEUDA** - Documentar pero no tocar sin aprobacion.
3. Generar planes solo para hallazgos aprobados por el humano.

### Fase 3 - Ejecucion con modelo barato
1. Cambiar a modelo economico (ver matriz en skill de proyectos nuevos).
2. Ejecutar cada plan respetando:
   - No cambiar estructura de carpetas.
   - No renombrar funciones/servicios existentes.
   - No migrar dependencias sin justificacion.
   - No modificar configuracion de despliegue.
3. Verificar que las pruebas existentes siguen pasando.

### Fase 4 - Validacion
1. El modelo caro revisa el diff final.
2. Confirmar que no hay regresiones.
3. Verificar tests existentes.
4. Documentar cambios en memoria del proyecto.

## Reglas para proyectos existentes
1. No sugerir cambios de framework/stack.
2. No reestructurar sin autorizacion explicita.
3. Toda mejora debe ser reversible o tener rollback documentado.
4. Pruebas existentes deben seguir pasando (si no hay, es hallazgo #1).
5. Preferir cambios pequenos y frecuentes sobre cambios masivos.

## Referencias
- `skills/improve/SKILL.md`
- `skills/conservacion-estructura-actual.md`
- `skills/refactorizacion-controlada.md`
