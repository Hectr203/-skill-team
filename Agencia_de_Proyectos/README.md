# Agencia de Proyectos

Agencia unificada para crear software nuevo y evolucionar software existente.
La ruta es `/mnt/nvme/skill-team/Agencia_de_Proyectos`.

## CLI Unificado de la Agencia (`scripts/agencia.py`)

La agencia cuenta con un punto de entrada centralizado para todo el ciclo de vida:

```bash
# 1. Diagnóstico integral preflight del entorno
python3 scripts/agencia.py doctor

# 2. Inicializar un nuevo proyecto (manifiesto, memoria, ADRs, evidencias)
python3 scripts/agencia.py nuevo <nombre-proyecto> --tipo nuevo|existente --cliente "Nombre"

# 3. Context Engine: carga de contexto, memoria, ADRs y FinOps de tokens
python3 scripts/agencia.py arranque <nombre-proyecto>          # Modo visual humano
python3 scripts/agencia.py arranque <nombre-proyecto> --prime  # System Primer para LLMs
python3 scripts/agencia.py arranque <nombre-proyecto> --json   # Modo máquina para subagentes

# 4. Registrar avance y cerrar sesión con alertas de escritorio
python3 scripts/agencia.py cierre <nombre-proyecto> --tareas "Descripción" --agente "Backend" --notificar

# 5. Dashboard resumen de todos los proyectos activos
python3 scripts/agencia.py estado

# 6. Validar integridad de la agencia (estándar 11/10)
python3 scripts/agencia.py validar
```

La persistencia opera de forma nativa en Markdown transparente (`contexts/projects/<id>/memoria.md`), con soporte opcional para `claude-mem` y un proyecto modelo de referencia en `contexts/projects/_ejemplo_golden/`.


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
