# Mejoras operativas de la agencia

## Objetivo y aceptación

Como operador, quiero que memoria, permisos y diagnósticos correspondan a resultados comprobados, y que los agentes apliquen reglas coherentes para cada proyecto.

- Una ruta externa no puede convertirse en un alias de memoria ni redirigirse mediante enlaces simbólicos.
- Una autorización pendiente, rechazada o sin auditoría no permite continuar como si estuviera aprobada.
- El MCP valida entradas y comunica fallos; admite el mismo selector de stack que el CLI.
- La memoria cifrada previa se conserva; no se inventa una clave para reemplazar un historial inaccesible.
- El catálogo activo selecciona una fuente por nombre y OpenCode puede descubrir sus entradas.
- El piloto crea dos proyectos aislados, registra un cierre y recupera el contexto por CLI y MCP.
- La documentación distingue el estándar de perfiles alternativos y las capacidades comprobadas de las pendientes.

## Decisiones

Se mantienen los IDs existentes. Nuevos proyectos usan IDs explícitos preferiblemente asociados al cliente. No se migraron historiales existentes ni se modificó la aplicación del directorio `proyecto/`.

Las variantes de habilidades se conservan; las entradas activas remiten a una fuente por nombre y reutilizan sus recursos. Se actualizó la habilidad de memoria para usar el motor central.

Se retiraron las credenciales literales de las configuraciones MCP. Stitch queda desactivado hasta disponer de una credencial nueva y comprobarla. La sintaxis de entorno de OpenCode se verificó en su [documentación](https://opencode.ai/docs/es/config/); no se presupone compatible con otros clientes.

## Verificación

La suite de la agencia contiene 30 pruebas de controles y operación, incluido el piloto y la vigencia de evidencia vinculada al contenido. Las pruebas de suites importadas no forman parte de esta certificación local.

OpenCode instalado: 1.18.31. Su diagnóstico descubrió 110 entradas activas con 110 nombres únicos. La salida completa se obtuvo mediante archivo temporal porque su salida por tubería se cortaba antes de terminar; no se guardaron instrucciones globales en la agencia.

La evidencia reproducible se guarda en `contexts/projects/_ejemplo_golden/evidencias/validacion-local.json`. Incluye los códigos y resultados reales de pruebas, validador, catálogo y diagnóstico. Es evidencia de ejecución local, no un recibo de revisión.

## Pendientes y límites

- Rotar o revocar la credencial anterior en el proveedor. Retirarla localmente no la invalida ni elimina copias históricas.
- Comprobar conexiones y permisos externos antes de utilizarlos; no se realizaron despliegues.
- Completar precios, disponibilidad y resultados comerciales con datos reales en los acuerdos de la agencia.
- El control vigente es `python3 scripts/agencia.py verificar` y `python3 scripts/agencia.py comprobar`; no requiere herramientas externas de revisión. Documentar por separado la revisión humana necesaria para cambios sensibles. No se realizaron commits, pushes o publicaciones.
- El aislamiento por rutas e IDs protege de colisiones accidentales; no separa usuarios del sistema operativo que tengan acceso al mismo almacén.
- La memoria Markdown y JSONL sigue siendo legible. No registrar secretos aunque exista una copia cifrada.

## Actualización de roles y selección de skills

Se actualizaron las 17 fichas de roles y las dos guías compartidas. El auditor de seguridad ya no duplica al frontend. El frontend estándar usa FSD con slices, segmentos, APIs públicas e imports descendentes; la documentación no acredita una migración del código de clientes.

El registro `reglas/rutas-agentes.json` conecta roles con habilidades canónicas; el validador detecta roles sin registro, rutas inexistentes, duplicados y desacuerdos con las fichas. Se revisaron metadatos y resolución del catálogo y las instrucciones de activación de las habilidades candidatas. El catálogo contiene 111 nombres únicos, incluida frontend-fsd. Se incorporó precedencia y límites de autorización en las fuentes candidatas; los recursos auxiliares conservan sus funciones específicas.

La comunicación separa hechos, supuestos y pendientes, evita inferencias por estereotipos y asigna un dueño por entregable. Adoptar un rol no crea un proceso autónomo; la delegación y los efectos externos necesitan autorización aplicable. Estos controles reducen errores y sesgos; no certifican una ausencia absoluta de ellos ni el funcionamiento de todas las integraciones externas.

## Arquitecturas centralizadas en stacks

Las fichas de frontend, backend y datos coordinan trabajo y resuelven el perfil del manifiesto. Las tecnologías y árboles residen en `stacks/estandar`; los perfiles alternativos no heredan dependencias estándar. La arquitectura frontend FSD se centralizó allí manteniendo el enlace anterior como referencia de compatibilidad. La arquitectura backend conserva módulos planos e incorpora contratos de puertos/adaptadores; la persistencia define archivos, integridad, migraciones y recuperación. El contrato de integración distribuye responsabilidades entre las tres capas.

## Decisión vigente: frontend modular por dominio

La aclaración del usuario reemplaza el objetivo FSD anterior del perfil estándar. Cada módulo reúne components, hooks, services, store y types, con entrada index.jsx. App compone módulos y los recursos genéricos viven fuera de ellos. Se actualizó la fuente de arquitectura, agentes, guías operativas y habilidad canónica frontend-modular. Las menciones FSD en las entradas históricas anteriores describen decisiones sustituidas y no son instrucciones vigentes. No se modificó el código de aplicaciones.

Esta página conserva resultados históricos. Consultar la auditoría integral y ejecutar `verificar` para obtener evidencia del contenido actual.
