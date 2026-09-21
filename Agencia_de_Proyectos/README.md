# Agencia de Proyectos

Agencia unificada para crear software nuevo y evolucionar software existente.
La ruta es `/mnt/nvme/skill-team/Agencia_de_Proyectos`.

## Inicio rapido

1. Lee `AGENTS.md` y `asistente-principal.md`.
2. Copia `plantillas/manifiesto-proyecto.md` al contexto aislado del proyecto.
3. Identifica tipo, objetivo, stack, cliente y aprobaciones necesarias.
4. Usa el flujo correspondiente en `flujos/`.
5. Consulta memoria y Graphify antes de explorar o responder sobre estructura.
6. Ejecuta `python3 scripts/validar_agencia.py` para validar esta agencia.

La agencia no instala ni conecta MCP externos automaticamente. `mcp/registro-mcp.md`
separa capacidades documentadas, configuraciones de ejemplo y estado real.

## Principios

- Monorepo dividido para proyectos nuevos: `frontend/` y `backend/` separados.
- Brownfield primero: conservar arquitectura existente y migrar solo con plan.
- Ponytail: la menor solucion correcta, sin recortar seguridad, accesibilidad,
  validacion, pruebas ni manejo de errores.
- Contexto aislado por proyecto, cliente, marca y campaña.
- Human-in-the-loop para toda accion externa o irreversible.

## Origen y trazabilidad

La matriz completa esta en `inventario/matriz-integracion.md` y el manifiesto
en `inventario/manifiesto-migracion.md`. Las fuentes originales permanecen
intactas y solo se usaron como referencia:

- `../Agencia_para_proyectos_desde_0/`: descubrimiento, arquitectura greenfield,
  loops, SDD, Ponytail, memoria local y CI.
- `../Agencia_Proyectos_Existentes/`: preservacion brownfield, memoria por
  proyecto, cambios incrementales, regresion y auditoria adaptativa.

## Estado de integraciones

Graphify, claude-mem, Headroom, Stitch, NotebookLM y Playwright tienen fichas
de integracion. En esta construccion no se instalaron, conectaron ni ejecutaron.
La compatibilidad operativa debe verificarse en el entorno del usuario.

## Validación de esta entrega

La auditoría estática cubrió 652 archivos de las dos fuentes (395 hashes
únicos); los duplicados exactos se agruparon y los estados privados se
excluyeron. El validador local comprueba la estructura de esta carpeta y termina
en `VALIDACION OK`. La ausencia de una tercera agencia independiente queda
registrada en `inventario/matriz-integracion.md`.
