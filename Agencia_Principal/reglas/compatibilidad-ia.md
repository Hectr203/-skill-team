# Compatibilidad de entornos

La agencia es documentación y herramientas locales; no depende de un proveedor de IA ni de un IDE. Su runtime local usa Python y sus aplicaciones usan el perfil que corresponda.

- Entrar por [asistente principal](../asistente-principal.md), objetivo y contexto del proyecto, sin cargar todos los documentos o skills indiscriminadamente.
- Confirmar capacidades disponibles: archivos, terminal, preguntas, navegador o MCP. Un nombre documentado no acredita conexión o ejecución.
- Si falta MCP, usar CLI; si falta ejecución, entregar un resultado revisable y comandos pendientes. No declarar validación.
- Configuraciones de clientes son adaptadores. Generar rutas para el checkout actual y combinar con configuración existente; no suponer expansión de variables universal.
- Las aprobaciones y permisos del entorno prevalecen. Un prompt no instala agentes, hooks, servicios o skills.
