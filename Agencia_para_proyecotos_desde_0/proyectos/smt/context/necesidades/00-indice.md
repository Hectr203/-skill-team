# Indice de necesidades del inventario de unidades SMT

Fecha de creacion: 2026-06-10

## Proposito

Esta carpeta concentra la documentacion formal de necesidades, requerimientos y decisiones iniciales para el inventario central de unidades y gestion de usuarios de SMT.

El objetivo es convertir las reuniones existentes en una base de trabajo clara para requerimientos, arquitectura, base de datos, API, backlog y validacion humana antes de iniciar el scaffold tecnico.

## Ruta canonica

La ruta oficial para esta documentacion es:

```txt
context/necesidades/
```

La carpeta `context/nececidades/` existe con error ortografico y no debe recibir nueva documentacion.

## Fuentes usadas

- `Agentes_Unificados/asistente-principal.md`
- `Agentes_Unificados/context/propuesta_unificada.md`
- `Agentes_Unificados/proyectos/smt/context/manifiesto-proyecto.md`
- `context/docuentos que manejan/SMT Parque Vehicular.md`
- `context/docuentos que manejan/SMT Parque Vehicular.xlsx`
- `context/reuniones /reunion con el equipo de desarollo sobre el inventario.md`
- `context/reuniones /Revisión de información para el inventario de unidades y gestión de usuarios.md`
- `context/reuniones /reunion cruda de nececidades y Revisión de información para el inventario de unidades y gestión de usuarios.md`

## Documentos generados

| Documento | Objetivo |
| --- | --- |
| `01-necesidades-negocio.md` | Define el problema, las necesidades del negocio y las reglas principales detectadas. |
| `02-requerimientos-funcionales.md` | Convierte las necesidades en requerimientos funcionales y no funcionales. |
| `03-modelo-dominio.md` | Propone entidades, estados, categorias y relaciones iniciales del dominio. |
| `04-arquitectura-api.md` | Define la estrategia de API central, autenticacion, permisos y endpoints base. |
| `05-backlog-scrum.md` | Organiza el primer backlog por epicas, historias y criterios de aceptacion. |
| `06-pendientes-validacion.md` | Lista decisiones que deben confirmarse con el humano y responsables de operacion. |
| `07-propuesta-fullstack-administrativa.md` | Define el inicio conjunto de API backend y frontend visual administrativo. |
| `08-lineamientos-visuales-administrativos.md` | Traduce las referencias visuales en reglas concretas de UI para el frontend administrativo. |

## Decisiones base

- El inventario de unidades sera una fuente unica de verdad para SMT.
- Las unidades no pertenecen a cada sistema individual; pertenecen a una entidad global administrada por la empresa.
- Taller y mantenimiento se modelan como procesos, eventos o estados relacionados con la unidad, no como unidades de negocio propietarias de vehiculos.
- La API central debe protegerse con autenticacion, tokens, roles y permisos.
- El frontend administrativo es parte obligatoria de la solucion y debe consumir la API como fuente unica de datos.
- La direccion visual administrativa debe seguir las referencias proporcionadas: barra lateral oscura, contenido claro, acentos rojos y tarjetas funcionales con jerarquia clara.
- Las altas de unidades quedan inicialmente bajo un rol de administrador global para evitar duplicidad.
- El primer ciclo de trabajo sera documentacion mas backlog, sin scaffold tecnico todavia.

## Estado de validacion

Pendiente de validacion humana. Esta documentacion es la base para revisar alcance, confirmar responsables y desbloquear el primer sprint tecnico.
