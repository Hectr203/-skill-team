# Flujo de Revision y Cierre

## Checklist
- Requerimiento entendido.
- Arquitectura existente respetada.
- Cambios limitados al alcance.
- Dependencias nuevas justificadas o evitadas.
- CI pipeline ejecutado y verde.
- Seguridad revisada si aplica.
- Pruebas ejecutadas o motivo documentado si no se ejecutaron.
- Riesgos residuales declarados.
- Pendientes claramente separados del trabajo terminado.
- Si hubo Azure: se conserva evidencia del análisis previo, aprobación, comandos `az`, estado de recursos, validaciones y rollback.
- La guía final fue escrita después del despliegue y no presenta propuestas o comandos no ejecutados como hechos.

## Informe de cierre
Debe incluir:
- Resumen del cambio.
- Archivos afectados.
- Decisiones tecnicas.
- Validaciones realizadas.
- Validaciones pendientes.
- Riesgos.
- Siguientes pasos recomendados.

## Registro de iteraciones
Incluir en el informe de cierre el historial completo de iteraciones:

| Iteracion | Objetivo | Agentes | Pruebas | Errores | Correcciones | Criterios OK | Criterios pendientes | Estado |
|-----------|----------|---------|---------|---------|--------------|-------------|---------------------|--------|
| 1 | | | | | | | | |

## Evaluacion final de criterios de aceptacion

| ID Criterio | Estado | Evidencia | Observaciones |
|-------------|--------|-----------|---------------|
| CA-001 | Cumplido/Incumplido/Parcial/Bloqueado/N/A | Link o referencia | Detalle |

## Bloqueos documentados (si aplica)
- Que impidio continuar:
- Acciones intentadas:
- Evidencias obtenidas:
- Intervencion humana necesaria:

## Condiciones de finalizacion verificadas
- [ ] Todos los CA obligatorios cumplidos.
- [ ] Pruebas criticas aprobadas.
- [ ] Sin errores bloqueantes.
- [ ] Evidencias recopiladas para cada criterio.
- [ ] Documentacion actualizada.
- [ ] Iteraciones registradas.
