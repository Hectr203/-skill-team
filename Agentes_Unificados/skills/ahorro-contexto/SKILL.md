---
name: ahorro-contexto
description: Use this skill when working in this project to reduce token usage, avoid unnecessary context loading, minimize memory usage, and keep project work concise and efficient.
---

# Ahorro de contexto y tokens

When working in this project:

- Do not read large files unless necessary.
- Do not scan the whole repository unless the task requires it.
- Prefer targeted searches over broad searches.
- Read only the files directly related to the task.
- Summarize findings briefly.
- Avoid repeating file contents unless requested.
- Avoid loading generated folders, dependency folders, build outputs, cache folders, logs, and binary files.
- Before editing, identify the smallest set of files needed.
- Prefer small, focused changes.
- Do not create long explanations after code changes.
- Do not include large diffs in the response unless requested.
- Mention only changed files and the reason for each change.
- Keep answers short and practical.

Avoid reading or indexing these paths unless explicitly requested:

- node_modules/
- vendor/
- dist/
- build/
- coverage/
- .git/
- .cache/
- .next/
- .nuxt/
- out/
- target/
- tmp/
- logs/
- *.log
- *.lock
- package-lock.json
- yarn.lock
- pnpm-lock.yaml
- composer.lock

Default workflow:

1. Understand the request.
2. Search only relevant filenames, symbols, or folders.
3. Open the smallest useful files.
4. Make the minimal necessary change.
5. Respond with a short summary.

## Memoria persistente del proyecto

Antes de cualquier modificacion importante dentro de `Agentes_Unificados`, ejecutar desde la raiz de la agencia:

```bash
python3 skills/ahorro-contexto/scripts/arranque.py
```

El arranque recupera Mem Palace y las entradas recientes de CloudMem local.

Despues de modificar documentos, agentes, skills, reglas, arquitectura o configuracion, registrar el cierre:

```bash
python3 skills/ahorro-contexto/scripts/cierre.py \
  --tareas "Resumen de tareas completadas" \
  --pendientes "Pendientes" \
  --decisiones "Decisiones tecnicas" \
  --riesgos "Riesgos" \
  --cloud-resumen "Resumen operativo no sensible" \
  --archivos "archivo1.md,archivo2.md" \
  --tipo "documental"
```

Usar Mem Palace para decisiones estables, arquitectura, backend, base de datos, seguridad y reglas criticas. Usar CloudMem local para historial operativo no sensible, avances recientes y archivos modificados.

## Memoria independiente por proyecto

Para cualquier tarea dentro de `proyectos/<nombre>/`, usar siempre memoria del proyecto:

```bash
python3 skills/ahorro-contexto/scripts/arranque.py --proyecto proyectos/<nombre>
```

Al cerrar:

```bash
python3 skills/ahorro-contexto/scripts/cierre.py \
  --proyecto proyectos/<nombre> \
  --tareas "Resumen de tareas completadas" \
  --pendientes "Pendientes" \
  --decisiones "Decisiones tecnicas" \
  --riesgos "Riesgos" \
  --cloud-resumen "Resumen operativo no sensible" \
  --archivos "archivo1.md,archivo2.md"
```

Para inicializar un proyecto copiado desde plantilla:

```bash
python3 skills/ahorro-contexto/scripts/memoria_proyecto.py --proyecto proyectos/<nombre> init
```
