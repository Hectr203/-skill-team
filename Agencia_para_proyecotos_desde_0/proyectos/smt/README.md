# Proyecto SMT

Esta carpeta concentra el contexto especifico de **SMT**.

## Que debe vivir aqui

- agentes que mencionen reglas, supuestos o decisiones propias de SMT
- skills de transporte, flotilla, rutas, choferes, combustible o telemetria
- contexto de negocio y reglas operativas del proyecto
- plantillas y documentos propios del dominio SMT

## Subcarpetas

- `agentes/`
- `skills/dominio/`
- `skills/operacion/`
- `skills/integraciones/`
- `context/`
- `plantillas/`
- `.memoria/`

## Memoria del proyecto

SMT usa memoria independiente en `.memoria/`.

Consultar antes de cambios:

```bash
python3 ../../skills/ahorro-contexto/scripts/arranque.py --proyecto proyectos/smt
```

Registrar cierre:

```bash
python3 ../../skills/ahorro-contexto/scripts/cierre.py --proyecto proyectos/smt \
  --tareas "Cambios realizados" \
  --pendientes "Pendientes" \
  --decisiones "Decisiones tecnicas" \
  --riesgos "Riesgos" \
  --cloud-resumen "Resumen operativo" \
  --archivos "archivo.md"
```
