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

Si el cambio corrige un bloqueante de despliegue, volver a ejecutar únicamente las validaciones afectadas de `despliegue-azure-proyecto-existente` y actualizar el informe de preparación. La corrección no autoriza por sí sola a crear infraestructura.

## Integracion con CI/CD
1. Hacer commit y push a rama de trabajo.
2. CI ejecuta pruebas existentes + pruebas nuevas.Verificar que no hay regresiones.
3. Si el proyecto no tenia CI, el pipeline `.github/workflows/ci.yml` se adapta al stack detectado.
4. Crear PR solo cuando CI este verde.
5. Merge a main activa CD (si esta configurado).

## Reglas
- No mezclar refactorizaciones no solicitadas con funcionalidades.
- No cambiar formato masivo de archivos no relacionados.
- No mover carpetas si el cambio puede resolverse dentro de la estructura actual.
- No ocultar pruebas fallidas.
- Toda correccion debe pasar por CI antes del merge.

## Ciclo iterativo de correccion
Si al verificar localmente (paso 5) o en CI (paso 2 de CI/CD) se detectan errores:

1. Registrar el error en el registro de iteraciones.
2. Clasificar la gravedad: bloqueante, alto, medio, bajo.
3. Aplicar la correccion especifica.
4. No repetir una correccion identica que ya haya fallado.
5. Volver a ejecutar verificacion local.
6. Si el error persiste tras 3 intentos, documentar bloqueo y escalar al humano.
7. Actualizar el registro de iteraciones con el resultado.

Cada iteracion de cambio debe quedar registrada con:
- Numero de iteracion.
- Errores detectados.
- Correcciones aplicadas.
- Pruebas ejecutadas y resultado.
- Estado de los criterios de aceptacion afectados.
- Regresiones verificadas (pruebas existentes que siguen pasando).

## Flujo completo
Para el ciclo completo desde especificacion hasta despliegue, usar `flujos/dev-flow-completo.md`.
