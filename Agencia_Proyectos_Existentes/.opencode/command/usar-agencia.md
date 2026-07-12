---
description: Usar la Agencia Universal para Proyectos Existentes como orquestador principal.
---

Actua usando esta agencia de proyectos existentes como herramienta principal.

Contrato operativo obligatorio:
- Lee y aplica `asistente-principal.md` como instruccion principal de orquestacion.
- Trabaja desde la carpeta actual de la agencia cuando ejecutes scripts o referencias internas.
- Usa sus agentes, skills, flujos, guias, plantillas, contexto y scripts cuando correspondan.
- Para pedir validacion humana, ejecuta `python3 scripts/solicitar_validacion.py --preguntas "<preguntas>"`.
- Para pedir permiso antes de acceder a una ruta o recurso sensible, ejecuta `python3 scripts/solicitar_autorizacion.py --recurso "<ruta o permiso>"`.
- Antes de responder con el cierre final de una tarea completada, ejecuta `python3 scripts/notificar_tarea.py --auto-completado --tarea "<resumen>"`.
- Nunca anadas `--sin-interfaz`, `--sin-navegador` ni `--sin-sonido` a los comandos de aviso; deben abrir navegador y reproducir audio exactamente 2 veces.

Solicitud del humano:

$ARGUMENTS
