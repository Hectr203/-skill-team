# Skill: Notificacion de Finalizacion

## Proposito

Avisar al humano cuando el agente haya terminado una ejecucion relevante o este por entregar la respuesta final, usando una notificacion visual y audible sin depender de servicios externos.

## Cuando usar

- Antes de responder al final de una tarea completada.
- Despues de una verificacion importante.
- Cuando el agente determine que ya termino una fase o ejecucion y va a informar el resultado.
- Al integrarse con automatizadores locales mediante comandos encadenados.

## Script ejecutable

Ruta:

```bash
Agencia_Proyectos_Existentes/scripts/notificar_tarea.py
```

HTML reutilizable:

```bash
Agencia_Proyectos_Existentes/scripts/notificacion_tarea.html
```

El script sobrescribe y reutiliza el mismo HTML para evitar crear multiples archivos temporales.

## Uso recomendado por agentes

Antes de la respuesta final, ejecutar desde la raiz de `Agencia_Proyectos_Existentes`:

```bash
python3 scripts/notificar_tarea.py --tarea "Tarea completada" --estado completada --mensaje "La ejecucion termino y el agente esta por responder."
```

Si se necesita evitar abrir navegador durante pruebas:

```bash
python3 scripts/notificar_tarea.py --tarea "Prueba" --sin-navegador --sin-sonido --sin-escritorio
```

## Opciones utiles

- `--tarea`: nombre visible de la tarea.
- `--estado`: estado mostrado, por ejemplo `completada` o `verificada`.
- `--mensaje`: texto del aviso.
- `--repeticiones`: cantidad de sonidos.
- `--sin-navegador`: no abre pestana.
- `--sin-sonido`: no emite sonido.
- `--sin-escritorio`: no intenta notificacion de escritorio.

## Integracion

Puede encadenarse con cualquier automatizador:

```bash
comando_largo && python3 /mnt/nvme/cotizacionsmt1/Agencia_Proyectos_Existentes/scripts/notificar_tarea.py --tarea "comando_largo"
```

## Restricciones

- No requiere credenciales ni informacion sensible.
- No envia datos a servicios externos.
- Usa Python 3 y bibliotecas estandar.
- El sonido del navegador puede depender de politicas de autoplay; por eso el script tambien intenta sonido del sistema y campana de terminal.
