# Memoria Independiente por Proyecto

## Objetivo
Cada proyecto existente debe tener memoria propia, separada de la agencia y de otros proyectos. La memoria acompana al proyecto copiado y conserva solo el contexto de ese proyecto.

## Estructura

```txt
proyectos/<nombre-proyecto>/
├── .memoria/
│   ├── mem_palace.key
│   ├── mem_palace.enc
│   ├── cloudmem.jsonl
│   └── manifiesto_memoria.md
├── context/
│   └── manifiesto-proyecto.md
├── agentes/
├── skills/
└── plantillas/
```

## Herramienta
La agencia incluye:

```txt
scripts/memoria_proyecto.py
```

## Inicializacion
Cuando se cree o copie un proyecto:

```bash
python3 scripts/memoria_proyecto.py --proyecto proyectos/<nombre-proyecto> init
```

El comando crea `.memoria/` si no existe y genera archivos independientes para ese proyecto.

## Inicio de sesion
Antes de modificar un proyecto:

```bash
python3 scripts/memoria_proyecto.py --proyecto proyectos/<nombre-proyecto> start
```

## Cierre de sesion
Despues de modificar un proyecto:

```bash
python3 scripts/memoria_proyecto.py --proyecto proyectos/<nombre-proyecto> close \
  --tareas "Resumen del trabajo" \
  --pendientes "Pendientes" \
  --decisiones "Decisiones" \
  --riesgos "Riesgos" \
  --cloud-resumen "Resumen operativo" \
  --archivos "ruta/archivo.md" \
  --tipo "documental"
```

## Reglas
1. No usar una memoria global para todos los proyectos.
2. No compartir `.memoria/` entre proyectos.
3. No copiar `mem_palace.key`, `mem_palace.enc` ni `cloudmem.jsonl` desde otro proyecto salvo migracion autorizada.
4. Si se copia la plantilla, ejecutar `init` antes de iniciar trabajo.
5. Si existe duda sobre sensibilidad, registrar en Mem Palace del proyecto y no en CloudMem.
