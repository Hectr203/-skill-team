# Compatibilidad con Diferentes IA

## Objetivo
Permitir que esta agencia sea usada por Codex, Claude, Gemini, GitHub Copilot u otras herramientas sin depender de funciones exclusivas de una sola plataforma.

## Reglas
1. Cada agente y skill debe poder leerse como prompt independiente.
2. Las instrucciones deben indicar entradas, salidas, limites y criterios de activacion.
3. No depender de rutas absolutas salvo que el proyecto lo requiera.
4. No asumir herramientas disponibles; si una IA no puede ejecutar comandos, debe entregar pasos verificables.
5. Mantener todo en espanol claro y formal.
6. Separar contexto estable, flujo de trabajo y plantillas.

## Adaptacion por IA
- Codex: usar lectura de archivos, edicion incremental y pruebas locales.
- Claude: usar agentes/skills como instrucciones de sistema o proyecto.
- Gemini: usar documentos como contexto de trabajo y guias de decision.
- GitHub Copilot: usar archivos como convenciones del repositorio y prompts reutilizables.
- Otras IA: cargar primero `README.md`, `asistente-principal.md`, reglas y guias de activacion.
