# Arquitectura API propuesta

## Resumen

La solucion debe partir de dos capacidades centrales: API de unidades y API de identidad/acceso. Ambas deben respetar la propuesta unificada de SMT: Node.js 22 LTS, Express.js, TypeScript, PostgreSQL, Prisma, Clean Architecture, dominio limpio y arquitectura hexagonal.

Esta API forma parte de una solucion fullstack. El frontend visual administrativo se documenta en `07-propuesta-fullstack-administrativa.md` y debe consumir estos contratos como fuente unica de datos operativos.

## Principios

- La API central de unidades es la fuente unica de verdad para vehiculos de SMT.
- Las aplicaciones consumidoras no administran inventarios propios una vez integrada la API.
- La API no se expone sin autenticacion.
- Cada respuesta debe limitar datos segun roles y permisos.
- Prisma solo vive en infraestructura y repositorios.
- Los casos de uso contienen reglas de negocio y no dependen de Express ni Prisma.

## Modulos backend iniciales

### Autenticacion

Responsable de inicio de sesion, cierre de sesion, emision y validacion de tokens.

Endpoints base:

- `POST /api/autenticacion/iniciar-sesion`.
- `POST /api/autenticacion/cerrar-sesion`.
- `GET /api/autenticacion/validar-token`.

### Usuarios y roles

Responsable de administracion de usuarios, roles y permisos.

Endpoints base:

- `GET /api/usuarios`.
- `POST /api/usuarios`.
- `PATCH /api/usuarios/:id`.
- `GET /api/roles`.
- `POST /api/roles`.
- `PATCH /api/roles/:id`.

### Unidades

Responsable del inventario global y estado operativo.

Endpoints base:

- `GET /api/unidades`.
- `POST /api/unidades`.
- `PATCH /api/unidades/:id`.
- `GET /api/unidades/disponibles`.
- `PATCH /api/unidades/:id/estado`.
- `POST /api/unidades/:id/reasignaciones`.

### Mantenimientos

Responsable de servicios, taller, reparaciones, historial y alertas.

Endpoints base:

- `GET /api/mantenimientos/proximos`.
- `POST /api/mantenimientos`.
- `PATCH /api/mantenimientos/:id/finalizar`.

## Contratos de API iniciales

### Iniciar sesion

```http
POST /api/autenticacion/iniciar-sesion
```

Entrada:

```json
{
  "correo": "usuario@smt.local",
  "contrasena": "valor_seguro"
}
```

Salida:

```json
{
  "token": "jwt",
  "usuario": {
    "id": "uuid",
    "nombre": "Nombre del usuario",
    "roles": ["turismo"],
    "permisos": ["unidades.consultar"]
  }
}
```

### Validar token

```http
GET /api/autenticacion/validar-token
Authorization: Bearer <token>
```

Salida:

```json
{
  "valido": true,
  "usuario": {
    "id": "uuid",
    "roles": ["turismo"],
    "permisos": ["unidades.consultar"]
  }
}
```

### Consultar unidades

```http
GET /api/unidades?categoria=turismo&estado=disponible
Authorization: Bearer <token>
```

Reglas:

- Requiere `unidades.consultar`.
- Respeta filtros permitidos por rol.
- No devuelve campos sensibles si el rol no los requiere.

### Crear unidad

```http
POST /api/unidades
Authorization: Bearer <token>
```

Reglas:

- Requiere `unidades.crear`.
- Solo disponible para administrador global hasta nueva validacion.
- Rechaza `numeroEconomico` duplicado.

### Cambiar estado

```http
PATCH /api/unidades/:id/estado
Authorization: Bearer <token>
```

Entrada:

```json
{
  "estado": "en_taller",
  "motivo": "Servicio correctivo",
  "observaciones": "Unidad ingresada por falla mecanica"
}
```

Reglas:

- Requiere `unidades.cambiar_estado`.
- El cambio queda auditado.
- Si el estado no es `disponible`, la unidad se excluye de disponibilidad.

### Mantenimientos proximos

```http
GET /api/mantenimientos/proximos
Authorization: Bearer <token>
```

Reglas:

- Requiere `mantenimientos.consultar`.
- Devuelve unidades con mantenimiento proximo.
- Prioriza 3 dias o menos como alta prioridad.

## Flujo de integracion con aplicaciones existentes

1. El usuario inicia sesion en la API central.
2. La API valida credenciales y devuelve token.
3. La aplicacion consumidora guarda el token de forma segura.
4. Cada backend consumidor valida el token contra la API central o mediante verificacion local de JWT si se define llave compartida.
5. La aplicacion consulta unidades, roles o permisos permitidos.
6. Si el token vence o se invalida, la aplicacion bloquea operaciones y solicita nuevo inicio de sesion.

## Integracion con frontend administrativo

El frontend administrativo debe consumir la API mediante servicios Axios centralizados. Ningun componente visual debe llamar directamente a `fetch` o `axios`.

Flujo base:

1. `frontend/src/modules/autenticacion` llama `POST /api/autenticacion/iniciar-sesion`.
2. `frontend/src/stores/sesion.store.ts` conserva usuario, roles, permisos y token.
3. `frontend/src/services/cliente-http.ts` adjunta el token en peticiones privadas.
4. Las rutas visuales validan permisos para mostrar u ocultar vistas y acciones.
5. La API valida permisos nuevamente en cada endpoint.
6. Los errores de negocio se devuelven en espanol y se muestran con Sonner.

## Seguridad

- Toda ruta privada requiere `Authorization: Bearer <token>`.
- Las contrasenas se almacenan con hash.
- El token debe incluir expiracion.
- La API debe validar permisos por endpoint.
- Los errores no deben exponer detalles internos.
- Los datos sensibles se devuelven solo a roles autorizados.

## Estructura backend recomendada

```txt
backend/
└── src/
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
    │   └── validaciones/
    └── servidor.ts
```

Cada modulo debe separar:

- `dominio`.
- `aplicacion`.
- `infraestructura`.
- `interfaces/http`.

## Errores base

- `401`: token ausente, invalido o vencido.
- `403`: usuario autenticado sin permiso suficiente.
- `404`: recurso no encontrado.
- `409`: conflicto, por ejemplo numero economico duplicado.
- `422`: datos invalidos o regla de negocio incumplida.
- `500`: error interno controlado.

## Pendientes tecnicos

- Confirmar estrategia JWT exacta: revocacion por sesiones, lista negra o expiracion corta.
- Confirmar si cada aplicacion reemplazara su login local o convivira temporalmente con token central.
- Confirmar campos expuestos por rol.
- Confirmar si se requiere API gateway o si las aplicaciones consumiran directamente el servicio central.
- Confirmar si el frontend administrativo sera la interfaz principal para altas, importacion y supervision.
