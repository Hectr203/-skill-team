---
name: mejora-asesor
description: Skill de mejora y auditoria con dos modelos. Usar primero /improve con el modelo mas capaz (caro) para analisis profundo, luego ejecutar los planes con un modelo barato o gratuito. Ideal para audits de codigo, revisiones de arquitectura y deteccion de mejoras.
---

# Mejora Asesor (Improve Advisor)

## Proposito
Aplicar la skill `shadcn/improve` con un flujo de dos modelos: el modelo mas capaz y caro para el analisis y la generacion de planes (fase de inteligencia intensiva), y un modelo barato o gratuito para la ejecucion de esos planes (fase de implementacion).

## Integracion con shadcn/improve
Esta skill es un wrapper que orquesta el uso de `shadcn/improve` (ubicada en `.agents/skills/improve/SKILL.md`). La skill original es estrictamente read-only y produce planes; esta skill anade la capa de ejecucion con el modelo economico.

## Filosofia
El analisis profundo requiere el mejor modelo disponible. La ejecucion de tareas bien especificadas puede hacerla cualquier modelo competente. Esto optimiza calidad por dolar gastado.

## Flujo de dos modelos

### Fase 1 - Analisis con modelo caro (INTELIGENCIA)
1. Activar la skill `improve` con el modelo mas capaz del agente:
   - Claude Opus 4 / Sonnet 4 para Anthropic.
   - GPT-5 / GPT-5.2 para OpenAI.
   - Gemini 2.5 Pro para Gemini.
   - DeepSeek-V4 para DeepSeek.
2. Ejecutar Recon completo: leer README, CLAUDE.md, AGENTS.md, estructura, package.json, tests.
3. Ejecutar Audit completo en las 9 categorias:
   - Correctitud/bugs, seguridad, rendimiento, cobertura de pruebas,
     deuda tecnica/arquitectura, dependencias/migraciones,
     DX/herramientas, documentacion, direccion/futuro.
4. Generar planes priorizados en `plans/` o `advisor-plans/`.
5. Presentar tabla de hallazgos al humano para aprobacion.

### Fase 2 - Ejecucion con modelo barato (IMPLEMENTACION)
1. Esperar confirmacion del humano sobre que planes ejecutar.
2. Cambiar a modelo economico:
   - Claude Haiku / Sonnet 4 (modelo rapido) para Anthropic.
   - GPT-4o mini / GPT-5.3 para OpenAI.
   - Gemini 2.5 Flash / Gemini 2.0 Flash para Gemini.
   - DeepSeek-V3 / DeepSeek-R1 para DeepSeek.
   - Gratuito: Claude Haiku, Gemini Flash, DeepSeek-V3.
3. Cargar el plan correspondiente.
4. Ejecutar paso a paso siguiendo el plan:
   - Leer archivos citados en el plan.
   - Aplicar cambios incrementales.
   - Ejecutar verificaciones del plan.
   - Confirmar criterios de completitud.
5. Si el modelo economico encuentra ambiguedad, escalar al modelo caro.

### Fase 3 - Validacion cruzada
1. El modelo caro revisa el diff generado por el modelo economico.
2. Verificar que no hay cambios fuera de alcance.
3. Confirmar que todas las pruebas pasan.
4. Actualizar `plans/README.md` con el estado.

## Invocacion
- `/improve quick` - Audit rapido con modelo caro, ejecucion inmediata con barato.
- `/improve` - Audit estandar con modelo caro, esperar confirmacion.
- `/improve deep` - Audit profundo con modelo caro.
- `/improve seguridad` - Audit solo de seguridad.
- `/improve execute <plan>` - Ejecutar plan especifico con modelo barato.

## Reglas
1. El analisis (Fase 1) SIEMPRE con el modelo mas caro disponible.
2. La ejecucion (Fase 2) SIEMPRE con el modelo mas barato disponible.
3. Si el modelo barato no puede completar, escalar al caro.
4. No ejecutar planes sin aprobacion humana previa.
5. No modificar codigo directamente desde la Fase 1 (read-only).
6. Documentar que modelo se uso en cada fase.
7. Si no hay modelo barato disponible, ejecutar igual con el mismo modelo pero advertirlo.

## Referencias
- `.agents/skills/improve/SKILL.md` - Documentacion original de shadcn/improve.
- `.agents/skills/improve/references/` - Referencias de audit, plan template, cierre.
