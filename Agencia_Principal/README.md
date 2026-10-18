# Agencia Principal

Sistema local de trabajo con IA: fichas de agentes, habilidades, contextos por proyecto, CLI y servidor MCP. La documentación orienta al modelo; las pruebas verifican controles concretos. La agencia no sustituye al runtime de agentes del IDE ni certifica servicios externos por estar configurados.

## Inicio

Ejecutar desde esta carpeta:

```bash
python3 scripts/agencia.py doctor
python3 scripts/agencia.py validar
python3 -m unittest discover -s tests -v
python3 scripts/agencia.py verificar
python3 scripts/agencia.py comprobar
python3 scripts/agencia.py nuevo cliente-web --cliente "Cliente"
python3 scripts/agencia.py arranque cliente-web --prime
python3 scripts/agencia.py cierre cliente-web --tareas "Avance verificado" --pendientes "Siguiente paso"
```

Para otro stack registrado, añadir `--stack laravel-livewire-alpine`. El CLI crea contexto y memoria; no genera automáticamente una aplicación ni un despliegue. Los perfiles inexistentes se preparan y aprueban antes de crear el proyecto.

## Organización

- [Precedencia de reglas](reglas/precedencia.md): resolver stack, convenciones y autorizaciones.
- [Asistente principal](asistente-principal.md) y [agentes](agentes/contrato-agente.md): selección de roles y entregables.
- [Inicio de proyectos](GUIA-INICIO-PROYECTO.md): desarrollo fuera de la carpeta de la agencia.
- [Stacks](stacks/README.md): estándar JavaScript y perfiles alternativos.
- `contexts/projects/<id>/`: manifiesto, memoria, ADRs y evidencias por ID explícito.
- `.agencia/catalogo-skills.json`: selección única de fuentes de habilidades.
- `.agencia/skills-activos/`: entradas ligeras generadas que remiten a sus recursos originales.
- [HITL](reglas/human-in-the-loop.md): operaciones sensibles y aprobación comprobable.
- [Operación comercial](contexts/agency/acuerdos.md): datos a completar antes de cotizar.

Las fuentes importadas se conservan. Para actualizar las entradas después de editar una fuente:

```bash
python3 scripts/catalogo_skills.py --generar
python3 scripts/catalogo_skills.py
```

No cargar recursivamente todas las variantes de `skills/` junto con las entradas activas. El catálogo detecta duplicados nuevos que requieren una selección explícita. Cada IDE puede añadir habilidades globales: comprobar sus colisiones en ese entorno.

## MCP y credenciales

OpenCode carga el MCP local `agencia` y las entradas activas. Stitch está desactivado hasta configurar una credencial nueva y comprobar la conexión. Su configuración utiliza `{env:STITCH_API_KEY}` según la [documentación de OpenCode](https://opencode.ai/docs/es/config/).

Los archivos `mcp_config.json` y `mcp/mcp_config.json` contienen solo el servidor local. Sus rutas corresponden a este equipo; al mover la agencia hay que apuntar al nuevo `scripts/agencia_mcp.py`. No asumir que otro cliente expande la sintaxis de variables de OpenCode.

Retirar una credencial de los archivos no la revoca en el proveedor. Rotar la anterior en la cuenta correspondiente y actualizar el entorno; no pegar claves en chats, Markdown ni JSON versionable.

El CLI y el MCP comunican fallos mediante código de salida e `isError`. `doctor` comprueba integridad local e inicialización MCP, sin realizar solicitudes a servicios externos.

La [verificación local](reglas/verificacion-local.md) ejecuta pruebas y validador, y conserva evidencia vinculada al contenido. `comprobar` rechaza informes ausentes, fallidos o desactualizados. No requiere instalar herramientas adicionales; el alcance es este checkout de la agencia.

## Piloto y comprobaciones

El [piloto de referencia](contexts/projects/_ejemplo_golden/manifiesto.md) documenta criterios verificables. `tests/test_flujo_piloto.py` ejecuta creación, arranque, cierre y recuperación con dos clientes en una agencia temporal, sin alterar proyectos reales.

Las pruebas de controles cubren rutas externas, enlaces simbólicos, validación de argumentos, propagación de errores y autorización pendiente. Una solicitud pendiente devuelve 2; solo una aprobación interactiva registrada devuelve 0.

Los archivos Markdown y JSONL de memoria son legibles. No registrar secretos; el cifrado de compatibilidad no protege esas copias. El aislamiento por ID evita alias accidentales, pero no constituye aislamiento de sistema operativo entre usuarios.

La rentabilidad, capacidad comercial y calidad de una aplicación se evalúan con datos y evidencias de cada proyecto, no con el número de agentes o habilidades.

## Skills y ampliación de roles

La selección se rige por [el contrato de skills](reglas/seleccion-skills.md). Buscar candidatos y resolver su fuente antes de leer y aplicar sus instrucciones:

```bash
python3 scripts/agencia.py skills --consulta frontend
python3 scripts/agencia.py skills --nombre frontend-modular
python3 scripts/agencia.py registrar-agente nombre-del-agente
```

El último comando registra una ficha existente creada con [la plantilla de agente](plantillas/nuevo-agente.md). No inicia procesos ni asigna skills obligatorias. Para generar configuración MCP en otra ubicación, usar `scripts/configurar_mcp.py --help`; nunca sobrescribe una configuración existente.

[Auditoría integral](contexts/agency/auditoria-integral.md): alcance, correcciones y registro por archivo. Las skills conservan sus fuentes independientes; esta auditoría verifica su integración, no sus procedimientos internos.

## Control de entregas y métricas

El [control de calidad](reglas/calidad-entregas.md) añade un registro independiente de tecnología y proveedor. `scripts/control_entregas.py` comprueba criterios y huellas de evidencias sin ejecutar instrucciones del informe. Calcula duración mediana, retrabajo y costos por moneda a partir de registros explícitos; no atribuye resultados comerciales a escenarios de prueba.

Los [escenarios operativos](contexts/agency/evaluacion-operativa.md) definen cómo comprobar coordinación, cambios de stack, contenido externo e indisponibilidad de herramientas. Están preparados para ejecución; no se contabilizan como resultados reales sin evidencia.

## Coordinación persistente

El [plan operativo](reglas/operacion-tareas.md) registra responsables, archivos y dependencias sin iniciar agentes. CLI `tareas` administra transiciones y revisiones; MCP `agencia_plan` consulta el mismo almacén. Un cierre pierde vigencia si cambian sus artefactos, su informe, su evidencia o un antecesor. Las fases anteriores se archivan y las escrituras son transaccionales.
