# Propuesta fullstack administrativa

## Resumen

El sistema de inventario de unidades SMT debe desarrollarse como una solucion fullstack, no solo como una API. La API central sera la fuente de datos, reglas de negocio, seguridad y trazabilidad; el frontend visual administrativo sera la herramienta operativa para administrar, supervisar y analizar unidades, documentos, mantenimientos, usuarios, roles y permisos.

Esta propuesta aplica los lineamientos de `Agentes_Unificados/asistente-principal.md` y de `Agentes_Unificados/context/propuesta_unificada.md`.

La direccion visual de referencia se complementa en `08-lineamientos-visuales-administrativos.md`.

## Lineamientos aplicables

### Clasificacion de la tarea

- Tipo: mixta, critica y fullstack.
- Memoria: Mem Palace, porque involucra inventario, base de datos, seguridad, reglas de negocio y arquitectura.
- Metodologia: Scrum por defecto.
- Validacion humana requerida: requerimientos, base de datos, permisos, dependencias relevantes y entregables finales.

### Stack obligatorio

Backend:

- Node.js 22 LTS.
- Express.js.
- TypeScript.
- PostgreSQL.
- Prisma.
- Clean Architecture, dominio limpio y arquitectura hexagonal.

Frontend:

- React.
- TypeScript.
- Tailwind CSS.
- Lucide React.
- Sonner.
- Zustand.
- Axios.
- React Router DOM.
- Atomic Design con `atomos`, `moleculas`, `organismos` y `templates`.
- Arquitectura modular en `modules`.

### Coordinacion por agentes

El asistente principal debe orquestar el flujo y asignar responsabilidades minimas:

- Agente de requerimientos: consolida requerimientos funcionales, no funcionales y criterios de aceptacion.
- Agente de desarrollo backend: implementa modulos, endpoints, casos de uso y contratos.
- Agente de desarrollo frontend: construye layout, vistas, formularios y consumo de API.
- Agente de diseno: define sistema visual, componentes base y coherencia con referencias.
- Agente de base de datos: aterriza modelo, migraciones, restricciones y semillas.
- Agente de testeo: valida reglas de negocio, interfaz y flujo de integracion.
- Agente de documentacion: registra cambios, decisiones, pruebas y pendientes.

## Componentes principales

### API backend

Responsabilidades:

- Centralizar autenticacion, usuarios, roles y permisos.
- Administrar unidades, estados, documentos, seguros, mantenimientos, odometro y reasignaciones.
- Aplicar reglas de negocio y validaciones criticas.
- Exponer contratos HTTP consumibles por el frontend administrativo y por aplicaciones externas.
- Proteger toda informacion privada mediante tokens y permisos por rol.

Modulos iniciales:

- `autenticacion`.
- `usuarios`.
- `roles`.
- `unidades`.
- `documentos`.
- `mantenimientos`.
- `reportes`.
- `auditoria`.

### Frontend visual administrativo

Responsabilidades:

- Permitir inicio de sesion y manejo visual de la sesion.
- Mostrar tablero operativo para supervision general.
- Administrar unidades desde formularios controlados.
- Consultar disponibilidad, estados, documentos, mantenimientos y alertas.
- Administrar usuarios, roles y permisos si el usuario tiene autorizacion.
- Visualizar informacion relevante por filtros, estados, categorias y permisos.
- Consumir la API mediante servicios Axios centralizados.
- Mostrar errores y confirmaciones con Sonner.
- Aplicar la direccion visual administrativa definida en las capturas de referencia.

Vistas iniciales:

- `InicioSesion`: acceso centralizado con token.
- `TableroAdministrativo`: resumen de unidades por estado, alertas de mantenimiento, documentos proximos a vencer y unidades no disponibles.
- `UnidadesListado`: tabla filtrable por tipo, categoria, estado, placas, numero de unidad y disponibilidad.
- `UnidadDetalle`: ficha integral con datos tecnicos, documentos, seguro, odometro, mantenimientos y trazabilidad.
- `UnidadFormulario`: alta y edicion de unidad con campos base y complementarios.
- `Mantenimientos`: listado de mantenimientos proximos, en proceso y finalizados.
- `DocumentosUnidad`: gestion de factura, tarjeta de circulacion, poliza, verificacion, contaminantes y fisico-mecanica.
- `UsuariosRoles`: administracion de usuarios, roles y permisos.
- `Reportes`: consultas filtradas por area, categoria, disponibilidad y vencimientos.

Direccion visual:

- Barra lateral oscura como estructura principal de navegacion.
- Encabezado superior claro con breadcrumbs y sesion.
- Area de contenido con fondo gris azulado suave.
- Acentos rojos en tabs, botones primarios y focos de accion.
- Tarjetas con sombra suave para detalle, resumen y vistas de comprobante.

## Integracion entre API y frontend

1. El usuario inicia sesion desde el frontend administrativo.
2. El frontend llama `POST /api/autenticacion/iniciar-sesion` mediante un servicio Axios.
3. La API devuelve token, usuario, roles y permisos.
4. Zustand conserva el estado minimo de sesion necesario para la navegacion.
5. Axios adjunta el token en cada peticion privada.
6. El frontend muestra u oculta rutas, botones y acciones segun permisos.
7. La API vuelve a validar permisos en cada endpoint; el frontend no sustituye las validaciones backend.
8. Los errores de negocio se muestran con mensajes claros en espanol.
9. Las operaciones criticas, como crear unidades, cambiar estados o modificar roles, requieren confirmacion visual.

## Estructura recomendada

### Backend

```txt
backend/
└── src/
    ├── config/
    │   └── prisma.ts
    ├── modulos/
    │   ├── autenticacion/
    │   ├── usuarios/
    │   ├── roles/
    │   ├── unidades/
    │   ├── documentos/
    │   ├── mantenimientos/
    │   ├── reportes/
    │   └── auditoria/
    ├── compartido/
    │   ├── errores/
    │   ├── middlewares/
    │   ├── respuestas/
    │   └── validaciones/
    └── servidor.ts
```

Cada modulo debe separar `dominio`, `aplicacion`, `infraestructura` e `interfaces/http`.

### Frontend

```txt
frontend/
└── src/
    ├── components/
    │   ├── atomos/
    │   ├── moleculas/
    │   ├── organismos/
    │   └── templates/
    ├── modules/
    │   ├── autenticacion/
    │   ├── tablero/
    │   ├── unidades/
    │   ├── documentos/
    │   ├── mantenimientos/
    │   ├── usuarios/
    │   └── reportes/
    ├── services/
    │   ├── cliente-http.ts
    │   └── manejador-errores.ts
    ├── stores/
    │   └── sesion.store.ts
    ├── hooks/
    ├── types/
    ├── routes/
    └── main.tsx
```

Reglas:

- Los componentes no llaman directamente a `fetch` ni a `axios`.
- Los servicios por modulo encapsulan los endpoints de API.
- Los tipos de respuesta viven en `types` o dentro del modulo correspondiente.
- Los componentes globales se crean primero en Atomic Design.
- Los modulos funcionales reutilizan componentes globales y solo agregan componentes locales cuando hay comportamiento especifico.

## Modulos visuales iniciales

### Autenticacion

- Formulario de inicio de sesion.
- Persistencia controlada de token.
- Proteccion de rutas.
- Cierre de sesion.

### Tablero

- Resumen de unidades por estado.
- Unidades en taller o mantenimiento.
- Documentos o polizas proximas a vencer.
- Mantenimientos urgentes.
- Accesos rapidos a alta de unidad, listado y reportes.

### Unidades

- Listado con filtros.
- Alta y edicion.
- Detalle de unidad.
- Cambio de estado.
- Reasignacion controlada.
- Validaciones visuales para campos base: numero de unidad, marca, tipo, serie, motor, placas, factura, T/C, poliza y vigencia.

### Documentos

- Registro de factura, tarjeta de circulacion, poliza, verificacion, contaminantes y fisico-mecanica.
- Estados normalizados: pendiente, no tiene, no aplica, en unidad, vigente, vencido y exento.
- Visualizacion de vigencias y pendientes.

### Mantenimientos

- Mantenimientos proximos.
- Mantenimientos en proceso.
- Finalizacion de mantenimiento.
- Priorizacion visual para 3 dias o menos.

### Usuarios y roles

- Listado de usuarios.
- Alta y edicion de usuarios.
- Asignacion de roles.
- Consulta de permisos.
- Acceso restringido a administradores.

### Reportes

- Reportes por categoria, area, estado y disponibilidad.
- Reportes de vencimientos documentales.
- Reportes de unidades incompletas o pendientes de validacion.

## Contratos compartidos

Backend y frontend deben trabajar con los mismos conceptos:

- `Unidad`.
- `Usuario`.
- `Rol`.
- `Permiso`.
- `DocumentoUnidad`.
- `Mantenimiento`.
- `Seguro`.
- `LecturaOdometro`.
- `ReasignacionUnidad`.

La fuente de verdad del contrato es la API. El frontend puede definir tipos TypeScript equivalentes, pero no debe importar modelos Prisma ni depender de estructuras internas de base de datos.

## Primer ciclo de desarrollo recomendado

### Sprint 0

Objetivo: cerrar decisiones minimas para iniciar API y frontend.

Entregables:

- Validacion de requerimientos fullstack.
- Confirmacion de campos minimos de unidad.
- Confirmacion de roles iniciales.
- Definicion de permisos por vista y accion.
- Definicion de navegacion inicial del frontend.
- Definicion de contratos iniciales de API.
- Definicion de paleta, tipografia, layout y componentes base del frontend administrativo.

### Sprint 1

Objetivo: crear base funcional de API y frontend administrativo.

Backend:

- Scaffold del backend.
- Modulo de autenticacion.
- Modulo de usuarios, roles y permisos.
- Modulo inicial de unidades.
- Middleware de autenticacion y permisos.

Frontend:

- Scaffold del frontend.
- Sistema base de rutas.
- Layout administrativo.
- Inicio de sesion.
- Store de sesion.
- Cliente Axios central.
- Barra lateral administrativa.
- Encabezado superior y breadcrumbs.
- Listado inicial de unidades.
- Formulario inicial de alta de unidad.

Validacion:

- Login visual consume API real.
- El token se adjunta en peticiones.
- Las rutas protegidas bloquean usuarios sin sesion.
- El listado de unidades consume `GET /api/unidades`.
- El alta visual consume `POST /api/unidades`.
- La API mantiene validaciones aunque el frontend oculte acciones.

## Criterios de aceptacion fullstack

- La solucion permite operar desde interfaz visual, no solo desde peticiones HTTP.
- El frontend usa la API como unica fuente de datos.
- Las reglas de negocio se validan en backend y se reflejan visualmente en frontend.
- Los usuarios ven solo rutas, datos y acciones autorizadas.
- El diseno visual es administrativo, claro, denso y enfocado en supervision operativa.
- La interfaz toma como referencia las capturas visuales sin caer en una copia literal ni en un dashboard generico.
- El proyecto mantiene idioma espanol en nombres, textos visuales, errores, documentacion y codigo propio.

## Documentacion y pruebas

Todo avance debe dejar evidencia de:

- Cambios implementados en backend y frontend.
- Decisiones tecnicas y visuales.
- Relacion entre cambios y requerimientos.
- Agentes y skills usados durante el proceso.
- Pruebas funcionales, visuales y de integracion ejecutadas.
- Riesgos, limites y pendientes para el siguiente ciclo.

## Pendientes de validacion

- Definir si el frontend administrativo sera la unica interfaz de alta o si otras aplicaciones podran solicitar altas.
- Confirmar permisos por vista: tablero, unidades, documentos, mantenimientos, usuarios, roles y reportes.
- Confirmar que indicadores debe mostrar el tablero inicial.
- Confirmar si reportes requieren exportacion en una primera version.
- Confirmar si se necesita importacion visual del Excel desde el frontend o si sera una tarea tecnica administrada.
