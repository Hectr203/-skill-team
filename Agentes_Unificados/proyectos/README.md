# Proyectos de la Agencia

Esta carpeta agrupa los contextos especificos de cada proyecto.

## Regla principal

Si un agente, skill o documento depende del negocio, lenguaje operativo o reglas de un proyecto concreto, debe vivir aqui y no en `base_reutilizable/`.

## Estructura esperada

Cada proyecto debe tener:

- `agentes/`
- `skills/`
- `context/`
- `plantillas/`
- `.memoria/`

Ademas, cada proyecto debe contar con un manifiesto propio para que la agencia pueda saber que contexto cargar.

## Memoria independiente por proyecto

Cada proyecto debe tener su propia memoria en:

```txt
proyectos/<nombre-proyecto>/.memoria/
```

El contenido de `.memoria/` pertenece solo a ese proyecto:

- `mem_palace.enc`: decisiones y contexto estable cifrado.
- `mem_palace.key`: clave local del proyecto.
- `cloudmem.jsonl`: historial operativo no sensible.
- `manifiesto_memoria.md`: descripcion de la memoria del proyecto.

## Crear un nuevo proyecto

```bash
cp -R proyectos/_plantilla_proyecto proyectos/mi-proyecto
python3 skills/ahorro-contexto/scripts/memoria_proyecto.py --proyecto proyectos/mi-proyecto init
```

## Consultar memoria del proyecto

```bash
python3 skills/ahorro-contexto/scripts/arranque.py --proyecto proyectos/mi-proyecto
```

## Registrar cierre del proyecto

```bash
python3 skills/ahorro-contexto/scripts/cierre.py \
  --proyecto proyectos/mi-proyecto \
  --tareas "Cambios realizados" \
  --pendientes "Pendientes" \
  --decisiones "Decisiones tecnicas" \
  --riesgos "Riesgos" \
  --cloud-resumen "Resumen operativo no sensible" \
  --archivos "archivo1.md,archivo2.md"
```

La memoria raiz de `Agentes_Unificados` queda solo para continuidad general de la agencia. El contexto de cada proyecto debe registrarse con `--proyecto`.
