# Flujo de Desarrollo Incremental

## Objetivo
Añadir valor al proyecto nuevo mediante características (features) desarrolladas de manera iterativa, asegurando calidad y cohesión con la arquitectura base previamente definida.

## Pasos
1. **Delimitar Alcance**: Entender claramente la funcionalidad a implementar en esta iteración.
2. **Diseño Técnico**: Identificar dónde encaja la nueva funcionalidad dentro de la arquitectura base y, si existe un perfil Azure, comprobar si cambia variables, red, almacenamiento, jobs, escalado u observabilidad.
3. **Desarrollo (TDD/BDD si aplica)**:
   - Crear la estructura de archivos necesaria.
   - Escribir pruebas unitarias/integración (opcional, recomendado).
   - Implementar la funcionalidad.
4. **Verificación Local**: Ejecutar el proyecto para validar que la funcionalidad cumple con lo requerido y no rompe la base existente.
5. **Revisión de Calidad**:
   - Comprobar que se siguen las convenciones de código.
   - Refactorizar si la solución inicial no es limpia.
6. **Documentación**: Actualizar los documentos del contexto (memoria) si la nueva característica añade dependencias clave, variables de entorno, cambia la arquitectura o modifica el perfil de despliegue.

## Integracion con CI/CD
Cada iteracion de desarrollo debe pasar por el pipeline CI antes de considerar la tarea completa:

1. `git push` a rama de trabajo.
2. CI ejecuta lint, typecheck, pruebas y build (`.github/workflows/ci.yml`).
3. Si CI falla, corregir antes de continuar.
4. Crear PR contra `develop` o `main`.
5. CI se ejecuta de nuevo en el PR.
6. Aprobacion de code review.
7. Merge a `main` activa CD (`.github/workflows/deploy.yml`).

## Reglas
- **Cohesión**: Toda característica nueva debe respetar la arquitectura decidida en la fase de inicialización.
- **Sin sobre-ingeniería**: Construir solo lo necesario para el requerimiento actual. Aplica `ponytail`.
- **Verificable**: Cada iteración debe terminar en un estado funcional con CI verde.
- **Pruebas**: Toda funcionalidad nueva incluye pruebas unitarias o de integracion con Playwright.
- **Preparación cloud**: No introducir dependencias de `localhost`, filesystem efímero, puertos fijos o secretos compilados que contradigan el perfil Azure aprobado.

## Ciclo iterativo de correccion
Si al verificar localmente (paso 4) o en CI (paso 2 de CI/CD) se detectan errores:

1. Registrar el error en el registro de iteraciones.
2. Clasificar la gravedad: bloqueante, alto, medio, bajo.
3. Aplicar la correccion especifica.
4. No repetir una correccion identica que ya haya fallado.
5. Volver a ejecutar verificacion local.
6. Si el error persiste tras 3 intentos, documentar bloqueo y escalar al humano.
7. Actualizar el registro de iteraciones con el resultado.

Cada iteracion de desarrollo debe quedar registrada con:
- Numero de iteracion.
- Errores detectados.
- Correcciones aplicadas.
- Pruebas ejecutadas y resultado.
- Estado de los criterios de aceptacion afectados.

## Flujo completo
Para el ciclo completo desde especificacion hasta despliegue, usar `flujos/dev-flow-completo.md`.
