# Flujo para Crear y Configurar un Proyecto Nuevo

## Objetivo
Establecer bases sólidas para un proyecto nuevo asegurando que su arquitectura, stack tecnológico y contexto inicial estén correctamente definidos desde el primer día.

## Pasos
1. **Entender el Requerimiento**: Comprender el dominio del negocio, el problema a resolver y los objetivos del proyecto. Revisa obligatoriamente los [Lineamientos de desarrollo](../reglas/lineamientos-desarrollo.md) antes de comenzar.
2. **Definir Stack y Arquitectura**: Proponer y acordar con el usuario el stack tecnológico, la estructura de carpetas y los patrones de diseño iniciales.
3. **Inicializar Proyecto**:
   - Crear el repositorio o carpeta principal utilizando plantillas o frameworks base (`npx`, `vite`, etc.).
   - Inicializar el control de versiones (`git init`).
   - (Opcional) Ejecutar el script `scripts/nuevo_proyecto.py` para establecer la memoria del proyecto si se requiere integración nativa con la agencia.
4. **Configurar Entorno**: Añadir linters, formateadores de código (Ej. Prettier/ESLint), y frameworks de pruebas iniciales.
5. **Documentar el Contexto**: Crear o actualizar el `manifiesto-proyecto.md` detallando las decisiones tomadas y la arquitectura base.
6. **Implementar el Núcleo (Core)**: Construir la base de la aplicación (ej. enrutamiento, configuración de BD, layout principal).
7. **Registrar Cierre Inicial**: Generar un informe de cierre de la fase de inicialización documentando tareas, dependencias base y próximos pasos.

## Criterio de cierre
La fase de inicialización se considera terminada cuando el proyecto compila/ejecuta exitosamente en su forma base, cuenta con su documentación arquitectónica en `context/` y está listo para recibir desarrollo incremental de características.
