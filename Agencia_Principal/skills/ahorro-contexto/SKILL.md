---
name: ahorro-contexto
description: Recuperar y cerrar el contexto de un proyecto de esta agencia con memoria por ID explícito y lectura mínima. Aplicar al reanudar sesiones o registrar decisiones; no usar como sustituto de un gestor de secretos.
---

## Integración en Agencia Principal
Aplicar el [contrato de selección y coordinación](../../agentes/contrato-agente.md). Activar esta habilidad solo si su resultado corresponde al alcance autorizado; los ejemplos de stack y herramientas no sustituyen el manifiesto. Recursos relativos se resuelven desde esta fuente. No ampliar permisos, invocar procesos recursivos ni declarar controles no ejecutados.


# Contexto y memoria por proyecto

Usa el CLI central desde la raíz de la agencia. Los scripts duplicados dentro de suites importadas son referencias históricas; no son el motor operativo activo.

1. Identifica el ID único en `contexts/projects/<id>/`. No lo deduzcas a partir de una ruta externa ni mezcles proyectos con el mismo nombre de carpeta.
2. Recupera contexto con `python3 scripts/agencia.py arranque <id> --prime` o `agencia_arranque` con `formato="primer"`.
3. Consulta CodeGraph antes de explorar código. Lee solo las fuentes relacionadas y omite dependencias, compilados y registros extensos salvo necesidad concreta.
4. Registra decisiones, riesgos y pendientes mediante `python3 scripts/agencia.py cierre <id> --tareas "resumen" --decisiones "decisiones" --pendientes "pendientes"`.
5. Conserva convenciones existentes y aplica [precedencia](../../reglas/precedencia.md).

El manifiesto y `memoria.md` son texto legible. El historial JSONL también puede contener datos sensibles: nunca registrar credenciales, datos personales innecesarios ni contenido confidencial de otro cliente. El cifrado de compatibilidad no protege las copias Markdown y JSONL.

No inicializar memoria durante una lectura. Si falta una clave de un archivo cifrado existente, informar la limitación; no generar una clave nueva para intentar recuperarlo.

Las herramientas opcionales de compresión y memoria remota se usan cuando están disponibles. No afirmar que comprimieron o sincronizaron datos sin evidencia de ejecución.
