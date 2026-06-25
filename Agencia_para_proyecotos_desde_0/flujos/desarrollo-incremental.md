# Flujo de Desarrollo Incremental

## Objetivo
Añadir valor al proyecto nuevo mediante características (features) desarrolladas de manera iterativa, asegurando calidad y cohesión con la arquitectura base previamente definida.

## Pasos
1. **Delimitar Alcance**: Entender claramente la funcionalidad a implementar en esta iteración.
2. **Diseño Técnico**: Identificar dónde encaja la nueva funcionalidad dentro de la arquitectura base del proyecto.
3. **Desarrollo (TDD/BDD si aplica)**:
   - Crear la estructura de archivos necesaria.
   - Escribir pruebas unitarias/integración (opcional, recomendado).
   - Implementar la funcionalidad.
4. **Verificación Local**: Ejecutar el proyecto para validar que la funcionalidad cumple con lo requerido y no rompe la base existente.
5. **Revisión de Calidad**:
   - Comprobar que se siguen las convenciones de código.
   - Refactorizar si la solución inicial no es limpia.
6. **Documentación**: Actualizar los documentos del contexto (memoria) si la nueva característica añade dependencias clave, variables de entorno o cambia la arquitectura.

## Reglas
- **Cohesión**: Toda característica nueva debe respetar la arquitectura decidida en la fase de inicialización.
- **Sin sobre-ingeniería**: Construir solo lo necesario para el requerimiento actual.
- **Verificable**: Cada iteración debe terminar en un estado funcional.
