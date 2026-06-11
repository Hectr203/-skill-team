# Guia de Contextos

## Que es un contexto
Un contexto es informacion estable que ayuda a los agentes a trabajar sin releer todo el proyecto en cada tarea. Puede incluir arquitectura, convenciones, decisiones, reglas de negocio, flujos criticos, comandos y riesgos.

## Cuando actualizar contexto
- Al descubrir una regla de negocio importante.
- Al confirmar una decision tecnica.
- Al cambiar arquitectura, base de datos, seguridad o integraciones.
- Al cerrar una tarea compleja con aprendizajes reutilizables.
- Al detectar una convencion local que debe respetarse.
- Al crear o copiar un proyecto nuevo dentro de `proyectos/`.

## Memoria por proyecto
Cada proyecto debe tener contexto y memoria independientes en `proyectos/<nombre>/.memoria/`.

Antes de trabajar sobre un proyecto:

```bash
python3 scripts/memoria_proyecto.py --proyecto proyectos/<nombre> start
```

Despues de cambios importantes:

```bash
python3 scripts/memoria_proyecto.py --proyecto proyectos/<nombre> close \
  --tareas "Cambios realizados" \
  --pendientes "Pendientes" \
  --decisiones "Decisiones tecnicas" \
  --riesgos "Riesgos" \
  --cloud-resumen "Resumen operativo" \
  --archivos "archivo.md"
```

Si el proyecto fue copiado desde la plantilla, `start` inicializa la memoria si falta. Tambien puede ejecutarse `init` de forma explicita.

## Que no debe guardarse
- Secretos, tokens, claves, contrasenas o credenciales.
- Datos personales innecesarios.
- Informacion sensible sin autorizacion.
- Suposiciones no verificadas como si fueran hechos.

## Formato recomendado
Cada entrada de contexto debe indicar:
- Fecha.
- Fuente.
- Area afectada.
- Hecho confirmado.
- Implicacion para futuros cambios.
