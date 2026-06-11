# Flujo para Analizar y Continuar un Proyecto Existente

1. Confirmar objetivo del humano.
2. Identificar repositorio, modulo y alcance.
3. Consultar o inicializar la memoria independiente del proyecto con `scripts/memoria_proyecto.py --proyecto <ruta> start`.
4. Leer documentacion y archivos de configuracion solo cuando la memoria no tenga contexto suficiente.
5. Mapear arquitectura, tecnologias, capas y convenciones.
6. Localizar codigo relacionado con la tarea.
7. Revisar pruebas existentes y comandos de validacion.
8. Definir estrategia: conservar, adaptar, extender o refactorizar.
9. Implementar cambios incrementales.
10. Ejecutar pruebas o verificaciones pertinentes.
11. Registrar cierre en `.memoria/` con tareas, archivos, decisiones, riesgos y pendientes.

## Criterio de cierre
La tarea solo se considera cerrada cuando el resultado cumple el requerimiento, respeta el sistema existente y se declaran las validaciones realizadas.
