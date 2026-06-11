---
name: memoria
description: Instrucción de memoria para agentes que trabajan dentro de un proyecto específico de la agencia.
---

# Memoria del Proyecto

Estás trabajando dentro de un proyecto específico de la Agencia Universal para Proyectos Existentes.

Este proyecto tiene su propia memoria independiente en `.memoria/`.  
**No uses, leas ni escribas en la memoria de otros proyectos.**

---

## Inicio de sesión

Antes de comenzar cualquier tarea, consulta la memoria de este proyecto desde la raíz de la agencia:

```bash
python3 scripts/arranque.py --proyecto proyectos/<nombre-de-este-proyecto>
```

Si no conoces el nombre exacto del proyecto, revisa en qué carpeta dentro de `proyectos/` estás trabajando.

---

## Cierre de sesión

Después de cada cambio importante en este proyecto:

```bash
python3 scripts/cierre.py --proyecto proyectos/<nombre-de-este-proyecto> \
  --tareas "Resumen de lo realizado" \
  --pendientes "Qué falta" \
  --decisiones "Decisiones técnicas" \
  --riesgos "Riesgos identificados" \
  --cloud-resumen "Resumen operativo no sensible" \
  --archivos "archivo1.ext,archivo2.ext"
```

---

## Reglas

1. La memoria de este proyecto está aislada en `.memoria/`. No la compartas con otros proyectos.
2. Toda sesión importante debe iniciar con `arranque.py` y cerrar con `cierre.py`.
3. Las decisiones técnicas, de arquitectura, seguridad o reglas de negocio van al Mem Palace (cifrado).
4. El historial operativo no sensible (avances, archivos modificados) va a CloudMem.
5. Si la memoria no está inicializada, ejecuta desde la raíz de la agencia:

```bash
python3 scripts/memoria_proyecto.py --proyecto proyectos/<nombre> init
```

---

## Contexto del proyecto

El manifiesto de este proyecto está en:

```txt
context/manifiesto-proyecto.md
```

Léelo antes de iniciar cualquier tarea si la memoria no tiene contexto suficiente.
