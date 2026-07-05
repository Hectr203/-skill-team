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
