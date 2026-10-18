# Plantilla para una skill independiente

El archivo final se llama `SKILL.md` y comienza con frontmatter válido:

```yaml
---
name: nombre-en-minusculas
description: Resultado y condiciones concretas para usar la habilidad; incluir exclusiones relevantes.
---
```

## Objetivo y alcance
[Capacidad reutilizable, sin cliente, modelo de IA o implementación particular como supuesto. Si es específica de un ecosistema, indicarlo como condición de uso.]

## Cuándo usar / cuándo no usar
[Activadores por intención y resultado, exclusiones y alternativa cuando falta una entrada.]

## Entradas y requisitos
[Datos, herramientas y permisos necesarios. No presumir conexión o autorización.]

## Procedimiento
[Pasos claros, recursos relativos y comprobaciones. Separar preparación de efectos externos.]

## Entrega y validación
[Resultados verificables, controles reales y límites. No declarar pruebas no ejecutadas.]

## Recursos, procedencia y mantenimiento
[Scripts/referencias empaquetados, autor/procedencia y condiciones de uso. Resolver rutas desde la fuente. Evitar duplicar reglas de un proyecto o copiar una arquitectura particular.]

Esta plantilla no instala ni registra una skill. Incorporar su fuente y generar el catálogo según [selección](../reglas/seleccion-skills.md); el contenido se revisa en una tarea específica de autoría, separada de la auditoría general.
