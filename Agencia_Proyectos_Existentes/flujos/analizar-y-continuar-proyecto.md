# Flujo para Analizar y Continuar un Proyecto Existente

1. Confirmar objetivo del humano.
2. Identificar repositorio, modulo y alcance.
3. Consultar o inicializar la memoria independiente del proyecto con `scripts/memoria_proyecto.py --proyecto <ruta> start`.
4. Leer documentacion y archivos de configuracion solo cuando la memoria no tenga contexto suficiente.
5. Mapear arquitectura, tecnologias, capas y convenciones.
6. Localizar codigo relacionado con la tarea.
7. Revisar pruebas existentes, comandos de validacion y si existe CI/CD.
8. Si el proyecto no tiene CI/CD, configurar `.github/workflows/ci.yml` adaptado al stack detectado.
9. Definir estrategia: conservar, adaptar, extender o refactorizar.
10. Implementar cambios incrementales.
11. Ejecutar CI pipeline (push a rama).
12. Crear PR, code review, merge.
13. Registrar cierre en `.memoria/` con tareas, archivos, decisiones, riesgos y pendientes.

## Rama obligatoria para despliegues Azure

Si la solicitud incluye preparación cloud, infraestructura o despliegue, sustituir los pasos 8 a 11 por el flujo [desplegar-en-azure.md](desplegar-en-azure.md). El orden es obligatorio:

1. terminar el análisis de solo lectura;
2. presentar y aprobar la propuesta;
3. corregir bloqueantes;
4. crear infraestructura y desplegar;
5. validar;
6. documentar el estado real.

No generar infraestructura durante el mapeo ni adelantar la documentación final.

## Criterio de cierre
La tarea solo se considera cerrada cuando el resultado cumple el requerimiento, respeta el sistema existente y se declaran las validaciones realizadas.

## Integracion con el ciclo de iteraciones

Cada cambio en un proyecto existente debe seguir el ciclo controlado:

### Fase de analisis
1. Interpretar la solicitud y el estado real del proyecto.
2. Identificar requerimientos, restricciones y dependencias.
3. Detectar informacion faltante o ambiguedades.
4. Mapear la arquitectura existente sin modificarla.

### Fase de especificacion
5. Definir alcance respetando la arquitectura actual.
6. Establecer criterios de aceptacion verificables.
7. Definir casos de prueba incluyendo verificacion de regresiones.
8. Establecer condiciones de finalizacion.

### Fase de implementacion y validacion
9. Implementar cambios incrementales.
10. Ejecutar pruebas existentes para descartar regresiones.
11. Validar contra criterios de aceptacion.
12. Si hay fallos, corregir y re-validar.
13. Repetir hasta cumplir o escalar bloqueos.

### Control del ciclo
14. Registrar cada iteracion en la memoria del proyecto.
15. Maximo 5 iteraciones. Si un error persiste tras 3 intentos, escalar al humano.
16. No cerrar la tarea sin evidencias de cumplimiento.
