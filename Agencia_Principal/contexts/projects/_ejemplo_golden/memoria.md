# Memoria del piloto de referencia

- Decisión: utilizar IDs explícitos, por ejemplo `cliente-uno-web` y `cliente-dos-web`.
- Almacén: `contexts/projects/<id>/`; nunca deducir un cliente a partir del último segmento de una ruta externa.
- Continuidad: manifiesto, memoria y eventos JSONL se recuperan mediante CLI y MCP.
- Validación: las pruebas crean agencias temporales independientes; no borran proyectos reales.
- Riesgos pendientes: la prueba local no verifica servicios remotos ni demuestra aislamiento de procesos por usuario.
- Próximo paso: ejecutar el piloto y registrar su resultado en la evidencia de la sesión.
