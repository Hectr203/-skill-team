# Human-in-the-loop

## Autónomo

Lecturas, contexto local, auditorías de solo lectura, planificación, edición dentro del alcance autorizado y pruebas locales reversibles.

## Requiere aprobación explícita

Instalar o conectar MCP/skills, usar credenciales o cuentas, publicar contenido,
enviar comunicaciones, contactar leads, desplegar a staging público o
producción, cambiar DNS, migrar o borrar datos productivos, comprar servicios y
rotar credenciales.

Una autorización explícita ya dada en la sesión cubre la operación descrita;
no repetir la pregunta para cada archivo del mismo cambio. No ampliar su alcance
a cuentas externas o producción. Para procesos que usen el script, ejecutar
`python3 scripts/solicitar_autorizacion.py --recurso "acción concreta" --esperar`
y continuar únicamente si devuelve 0. Un código 2 significa pendiente y bloquea
la acción. Los avisos se pueden silenciar en automatización sin eludir la aprobación.

## Registro

Para operaciones externas o sensibles registrar responsable, herramienta, propósito,
datos accesibles, aprobación, resultado, archivos afectados y rollback.
