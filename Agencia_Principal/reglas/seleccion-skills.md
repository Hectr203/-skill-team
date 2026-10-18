# Descubrimiento y uso de skills

## Contrato de integración
Una skill es una capacidad reutilizable con su propia descripción, entradas, procedimiento, recursos y límites. El rol define responsabilidad; el perfil define arquitectura y tecnología; la tarea define objetivo y permiso. Una skill especializada puede requerir una herramienta o tecnología, pero eso no obliga a utilizarla en otro perfil. La compatibilidad se decide antes de aplicarla.

## Selección por tarea
1. Precisar resultado, entradas y restricciones del proyecto activo.
2. Consultar `python3 scripts/agencia.py skills` o MCP `agencia_skills`. El filtro `--consulta` es textual y solo reduce candidatos; puede omitir sinónimos, así que consultar el catálogo completo si hace falta. No activa nada por palabras aisladas.
3. Resolver nombre exacto con `python3 scripts/agencia.py skills --nombre <nombre>` o `agencia_skill`. La salida identifica fuente y directorio de recursos, sin ejecutar su procedimiento.
4. Leer la fuente seleccionada, incluidas exclusiones y recursos necesarios. Resolver rutas relativas desde esa fuente, no desde el wrapper generado.
5. Aplicar únicamente lo pertinente al resultado autorizado. Si hay conflicto con perfil, instrucciones o permisos, elegir otra skill o adaptar ejemplos sin falsear su aplicación. Si la capacidad depende de una tecnología incompatible, no utilizarla.
6. Verificar herramientas y entradas reales antes de operar. Una integración ausente admite alternativa local o resultado parcial explícito. No declarar invocaciones, aprobación o controles que no ocurrieron.
7. Registrar en la entrega solo skills aplicadas, propósito y límites; no copiar su contenido a roles, stacks o memoria.

## Incorporar skills independientes
Para una skill propia usar [plantilla](../plantillas/nueva-skill.md). Para terceros preservar procedencia y recursos, revisar su contrato antes del uso y conservar sus condiciones/licencia. El catálogo selecciona una fuente por nombre; un duplicado necesita decisión explícita, no prioridad accidental por orden de directorios.

`python3 scripts/catalogo_skills.py --generar` actualiza entradas y catálogo; después ejecutar validación local. Este paso lee metadatos y comprueba resolución, no certifica la redacción o seguridad del procedimiento interno. El contenido y las pruebas propias de skills quedan fuera de la auditoría general de la agencia salvo encargo específico.

No instalar, conectar o ejecutar servicios externos por regenerar el catálogo. Cada cliente puede cargar skills globales adicionales: comprobar colisiones en ese entorno. Los wrappers son adaptadores generados; las fuentes bajo `skills/` permanecen independientes.
