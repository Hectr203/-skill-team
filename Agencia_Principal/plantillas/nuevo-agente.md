# Nombre del rol

Aplicar el [contrato común](../agentes/contrato-agente.md) y la [precedencia](../reglas/precedencia.md). Al copiar esta plantilla a agentes, ajustar el enlace al contrato como `contrato-agente.md`.

## Objetivo
[Responsabilidad y resultado del rol, sin tecnologías universales.]

## Activación
[Cuándo corresponde usar este rol y cuándo no.]

## Entradas
[Objetivo, alcance, contexto, fuentes, perfil y criterios necesarios.]

## Acciones y límites
[Permisos de lectura/escritura, coordinación con el asistente principal, dueño de artefactos y condiciones de traspaso. No crear procesos por adoptar la ficha.]

## Uso de skills
Aplicar [selección común](../reglas/seleccion-skills.md), descubrir por tarea y leer fuentes compatibles. No incrustar una lista obligatoria de tecnologías o skills.

## Entrega
[Resultado, archivos, criterios, evidencia real, riesgos y próximo responsable.]

## Criterios de aceptación
[Condiciones verificables para completar el alcance y controles pendientes.]

Tras guardar como `agentes/<id>.md`, registrar con `python3 scripts/agencia.py registrar-agente <id>` y ejecutar la verificación local. Registrar la ficha no crea un proceso de agente.
