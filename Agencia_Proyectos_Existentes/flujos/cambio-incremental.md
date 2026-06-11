# Flujo de Cambio Incremental

## Objetivo
Reducir riesgo en proyectos existentes mediante cambios pequenos y verificables.

## Pasos
1. Delimitar comportamiento esperado.
2. Identificar archivos minimos.
3. Leer patrones equivalentes.
4. Aplicar un cambio pequeno.
5. Verificar localmente.
6. Ajustar si hay regresiones.
7. Documentar.

## Reglas
- No mezclar refactorizaciones no solicitadas con funcionalidades.
- No cambiar formato masivo de archivos no relacionados.
- No mover carpetas si el cambio puede resolverse dentro de la estructura actual.
- No ocultar pruebas fallidas.
