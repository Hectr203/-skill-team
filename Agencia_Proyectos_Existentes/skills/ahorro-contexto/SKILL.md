---
name: ahorro-contexto
description: Úsala en cualquier sesión dentro de Agencia_Proyectos_Existentes para gestionar la memoria independiente de cada proyecto, reducir carga de contexto y registrar decisiones de forma persistente.
---

# Ahorro de contexto y memoria persistente por proyecto

## Regla fundamental

Cada proyecto en `proyectos/<nombre>/` tiene su propia memoria en `proyectos/<nombre>/.memoria/`.  
**No existe memoria global compartida entre proyectos.**

---

## Inicio de sesión (arranque)

Antes de trabajar en cualquier proyecto, recupera su memoria:

```bash
python3 scripts/arranque.py --proyecto proyectos/<nombre>
```

Si no sabes qué proyectos existen:

```bash
python3 scripts/arranque.py
```

---

## Cierre de sesión

Después de modificar documentos, agentes, skills, reglas, arquitectura o código del proyecto:

```bash
python3 scripts/cierre.py --proyecto proyectos/<nombre> \
  --tareas "Resumen de tareas completadas" \
  --pendientes "Pendientes" \
  --decisiones "Decisiones tecnicas" \
  --riesgos "Riesgos" \
  --cloud-resumen "Resumen operativo no sensible" \
  --archivos "archivo1.md,archivo2.md" \
  --tipo "operativo"
```

Solo `--proyecto` y `--tareas` son obligatorios. El resto es opcional pero recomendado.

---

## Inicializar un proyecto nuevo

Si el proyecto aún no tiene memoria o fue copiado desde la plantilla:

```bash
# Opción 1 — Recomendada: crea la carpeta Y la memoria de una vez
python3 scripts/nuevo_proyecto.py <nombre>

# Opción 2 — Manual: copiar plantilla y luego inicializar
cp -R proyectos/_plantilla_proyecto proyectos/<nombre>
python3 scripts/memoria_proyecto.py --proyecto proyectos/<nombre> init
```

---

## Consultar memoria directamente

```bash
# Ver Mem Palace + CloudMem reciente del proyecto
python3 scripts/memoria_proyecto.py --proyecto proyectos/<nombre> start

# Agregar entrada rápida a CloudMem sin cierre completo
python3 scripts/memoria_proyecto.py --proyecto proyectos/<nombre> add \
  --resumen "Nota operativa" \
  --archivos "ruta/archivo.md" \
  --tipo "operativo"
```

---

## Reglas de uso de memoria

| Tipo de información | Dónde guardar |
|---|---|
| Decisiones de arquitectura, seguridad, reglas de negocio | Mem Palace (cifrado) — usar `--decisiones` |
| Historial operativo, avances, archivos modificados | CloudMem — usar `--cloud-resumen` |
| Información sensible del proyecto | Solo Mem Palace, nunca CloudMem |
| Contexto inicial del proyecto | `context/manifiesto-proyecto.md` |

---

## Lectura eficiente de archivos

- Lee solo los archivos directamente relacionados con la tarea.
- Usa la memoria del proyecto en lugar de releer todos los archivos en cada sesión.
- No escanees el repositorio completo a menos que la tarea lo requiera.
- Evita cargar: `node_modules/`, `dist/`, `build/`, `.git/`, `*.lock`, `*.log`.

---

## Flujo de trabajo por defecto

1. Ejecutar `arranque.py --proyecto proyectos/<nombre>` para leer contexto.
2. Leer solo los archivos mínimos necesarios.
3. Realizar el cambio más pequeño que cumpla el objetivo.
4. Ejecutar `cierre.py` con un resumen claro del trabajo realizado.

---

## Estructura de memoria por proyecto

```txt
proyectos/<nombre>/
└── .memoria/
    ├── mem_palace.enc      ← decisiones cifradas (Mem Palace)
    ├── mem_palace.key      ← clave local del proyecto
    ├── cloudmem.jsonl      ← historial operativo no sensible
    └── manifiesto_memoria.md ← descripción de la memoria
```
