# Flujo de Memoria Persistente

## Objetivo
Evitar que cada sesion de desarrollo tenga que reconstruir desde cero el historial del proyecto. Todo agente debe consultar memoria antes de cambios importantes y registrar el cierre despues de modificar documentos, agentes, skills, arquitectura, reglas de negocio, base de datos, seguridad o configuracion.

## Herramientas activas

## Memoria independiente por proyecto
Todo proyecto dentro de `Agentes_Unificados/proyectos/<nombre>/` debe tener memoria propia en:

```txt
proyectos/<nombre>/.memoria/
```

La memoria raiz de `Agentes_Unificados` queda como continuidad general de la agencia. Las tareas de un proyecto concreto deben usar siempre `--proyecto`.

Inicializar memoria de un proyecto:

```bash
cd Agentes_Unificados
python3 skills/ahorro-contexto/scripts/memoria_proyecto.py --proyecto proyectos/<nombre> init
```

Consultar memoria de un proyecto:

```bash
cd Agentes_Unificados
python3 skills/ahorro-contexto/scripts/arranque.py --proyecto proyectos/<nombre>
```

Registrar cierre de un proyecto:

```bash
cd Agentes_Unificados
python3 skills/ahorro-contexto/scripts/cierre.py \
  --proyecto proyectos/<nombre> \
  --tareas "Cambios realizados" \
  --pendientes "Pendientes" \
  --decisiones "Decisiones tecnicas" \
  --riesgos "Riesgos" \
  --cloud-resumen "Resumen operativo no sensible" \
  --archivos "archivo1.md,archivo2.md"
```

### Mem Palace
Memoria local cifrada para informacion estable o sensible.

Usar para:
- Decisiones tecnicas importantes.
- Reglas de arquitectura.
- Criterios de implementacion.
- Cambios estructurales.
- Acuerdos del proyecto.
- Riesgos criticos.
- Informacion de backend, base de datos, seguridad o trazabilidad.

Archivo local:

```txt
.memoria_palacio_cifrada
```

Clave local:

```txt
.mem_palace_key
```

### CloudMem local
Historial operativo no sensible guardado como JSONL para continuidad rapida entre sesiones.

Usar para:
- Cambios recientes.
- Archivos modificados.
- Avances documentales.
- Ajustes de frontend no sensibles.
- Pendientes operativos.
- Modificaciones especificas de agentes, skills o guias.

Archivo local:

```txt
.cloudmem.jsonl
```

No guardar en CloudMem local:
- Credenciales.
- Secretos.
- Llaves de API.
- Datos personales sensibles.
- Reglas confidenciales de negocio.
- Detalles internos de seguridad.

## Inicio obligatorio de sesion
Antes de modificar el proyecto:

```bash
cd Agentes_Unificados
python3 skills/ahorro-contexto/scripts/arranque.py
```

El arranque recupera:
- Ultimo contexto cifrado de Mem Palace.
- Entradas recientes de CloudMem local.

## Consulta rapida de CloudMem local

```bash
cd Agentes_Unificados
python3 skills/ahorro-contexto/scripts/cloudmem.py list --limite 10
python3 skills/ahorro-contexto/scripts/cloudmem.py list --filtro "frontend"
```

## Registro operativo en CloudMem local

```bash
cd Agentes_Unificados
python3 skills/ahorro-contexto/scripts/cloudmem.py add \
  --tipo "documental" \
  --resumen "Se actualizo la guia de agentes y habilidades." \
  --archivos "context/guia_agentes_y_habilidades.md"
```

## Cierre obligatorio de sesion
Para registrar Mem Palace y CloudMem local en un solo paso:

```bash
cd Agentes_Unificados
python3 skills/ahorro-contexto/scripts/cierre.py \
  --tareas "Cambios completados" \
  --pendientes "Pendientes conocidos" \
  --decisiones "Decisiones tecnicas tomadas" \
  --riesgos "Riesgos detectados" \
  --cloud-resumen "Resumen operativo no sensible" \
  --archivos "archivo1.md,archivo2.md" \
  --tipo "documental"
```

## Regla de seleccion
- Si la informacion es tecnica estable, critica o sensible: Mem Palace.
- Si la informacion es historial operativo no sensible: CloudMem local.
- Si existe duda sobre sensibilidad: Mem Palace.

## Criterio de cumplimiento
Un cambio importante no queda cerrado hasta que:
1. Se consulto memoria al inicio.
2. Se identificaron decisiones previas relacionadas.
3. Se aplico el cambio respetando el contexto.
4. Se registro el cierre con tareas, archivos, decisiones, riesgos y pendientes.
