# Proyectos Existentes

Cada subcarpeta dentro de `proyectos/` representa un proyecto independiente.

## Regla principal
Cada proyecto debe tener su propia memoria en:

```txt
proyectos/<nombre-proyecto>/.memoria/
```

Esa carpeta contiene:
- `mem_palace.enc`: memoria cifrada para decisiones estables.
- `mem_palace.key`: clave local del proyecto.
- `cloudmem.jsonl`: historial operativo no sensible.
- `manifiesto_memoria.md`: descripcion de la memoria del proyecto.

No se debe usar una memoria global compartida entre proyectos.

## Crear un nuevo proyecto (método recomendado)

```bash
python3 scripts/nuevo_proyecto.py <nombre-proyecto>
```

El script copia la plantilla, inicializa la memoria independiente y muestra los siguientes pasos.

## Crear un nuevo proyecto (método manual)

```bash
cp -R proyectos/_plantilla_proyecto proyectos/mi-proyecto
python3 scripts/memoria_proyecto.py --proyecto proyectos/mi-proyecto init
```

El comando `init` crea o valida la memoria independiente del proyecto copiado.

## Consultar memoria

```bash
python3 scripts/memoria_proyecto.py --proyecto proyectos/mi-proyecto start
```

## Registrar cierre

```bash
python3 scripts/memoria_proyecto.py --proyecto proyectos/mi-proyecto close \
  --tareas "Cambios realizados" \
  --pendientes "Pendientes" \
  --decisiones "Decisiones tecnicas" \
  --riesgos "Riesgos" \
  --cloud-resumen "Resumen operativo no sensible" \
  --archivos "archivo1.md,archivo2.md" \
  --tipo "operativo"
```
