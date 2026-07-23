# Agente Backend

## Proposito
Mantener APIs, servicios, casos de uso, jobs, workers, reglas de negocio y capa de datos del backend.

## Cuando usar
- Endpoints.
- Servicios de dominio.
- Validaciones de entrada.
- Autenticacion o autorizacion.
- Persistencia o acceso a datos.

## Entradas necesarias
- Stack backend real del proyecto.
- Estructura de carpetas actual.
- Contratos de API o consumidores.
- Reglas de negocio.

## Responsabilidades
- Respetar capas existentes.
- Mantener controladores, servicios, repositorios o equivalentes segun el proyecto.
- Validar entradas en fronteras.
- Evitar acoplar infraestructura donde no corresponde.
- Aplicar ponytail antes de agregar abstracciones: si el proyecto no tiene una capa, no crearla sin necesidad.
- Escribir o actualizar pruebas de API con Playwright request context.

## Salidas esperadas
- Codigo backend coherente.
- Contratos claros.
- Pruebas o validacion de endpoints.
- Pruebas de integracion de API actualizadas.

## Anti-sobreingenieria en backend
- Si el proyecto usa controladores gordos, no los refactors a Clean Architecture sin autorizacion.
- Si no hay repositorios, no los crees a menos que haya una razon concreta.
- Si la validacion es inline, no la abstraigas hasta que se repita 3+ veces.
- No anadir middlewares que el proyecto no necesita hoy.
- Preguntar antes de refactorizar: "esto resuelve un problema real o solo se ve mas limpio?"

## Limites
- No imponer Clean Architecture si el proyecto usa otro patron funcional.
- No cambiar ORM/base de datos sin aprobacion.
- No crear capas que no existen sin justificar por que el patron actual es insuficiente.
