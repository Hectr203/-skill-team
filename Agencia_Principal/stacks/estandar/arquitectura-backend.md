# Arquitectura backend: módulos de dominio y puertos/adaptadores

## Alcance y decisiones
Conservar la organización plana por módulo descrita en la sección 1. Clean Architecture define la dependencia hacia reglas y casos de uso; arquitectura hexagonal explicita puertos y adaptadores. Se aplican como límites compatibles, sin duplicar capas o imponer un contenedor de inyección. Una estructura existente por carpetas de capa puede mantenerse si respeta estos límites; una tarea puntual no autoriza migrarla.

El dominio y los casos de uso no dependen de HTTP, ORM o servicios externos. Los adaptadores implementan contratos requeridos por el caso de uso. La composición instancia adaptadores y los inyecta. Un puerto puede documentarse con JSDoc y una factoría en JavaScript: no requiere una clase abstracta o un archivo vacío.

## Simplicidad obligatoria (Ponytail)
Todo trabajo backend aplica la skill Ponytail en nivel `full` según la [política de simplicidad](../../reglas/simplicidad-ponytail.md). Ponytail actúa dentro de esta arquitectura: conserva sus límites de dependencia, validación, seguridad, errores, transacciones y autorización, pero prohíbe capas vacías, interfaces con una sola implementación, archivos sin lógica y estructuras para necesidades hipotéticas. Si un caso se resuelve con una ruta, un controlador, un caso de uso y una operación de repositorio existentes, no se añaden más capas. Cuando este documento y una solución más simple parezcan chocar, prevalecen los límites de seguridad e integridad de este documento y, dentro de ellos, la solución con menos código, archivos y dependencias.

## 1. Organización de archivos

Mantén los módulos pequeños con archivos planos y crea solamente los archivos que tengan contenido real. El árbol muestra el máximo habitual, no una lista obligatoria:

```text
backend/
├── prisma/
│   ├── schema.prisma
│   └── migrations/
└── src/
    ├── app.js
    ├── server.js
    ├── config/
    │   ├── env.js
    │   └── prisma.js
    ├── shared/
    │   ├── errors/
    │   ├── middlewares/
    │   ├── responses/
    │   ├── validators/
    │   ├── repositories/
    │   └── utils/
    └── modules/
        └── almacen/
            ├── index.js
            ├── almacen.routes.js
            ├── almacen.controller.js
            ├── almacen.service.js
            ├── almacen.repository.js
            ├── almacen.schema.js
            ├── almacen.dto.js
            └── almacen.types.js
```

- `app.js`: configura Express, compone módulos y registra middlewares. No abre el puerto.
- `server.js`: inicia el servidor y coordina el cierre ordenado.
- `config/env.js`: carga y valida variables de entorno; falla al iniciar si falta una configuración obligatoria.
- `config/prisma.js`: crea y administra una instancia compartida del cliente por proceso y contexto de ejecución.
- `modules/<modulo>/index.js`: compone las dependencias y expone la entrada pública del módulo.
- `shared/repositories/`: repositorios técnicos realmente compartidos, incluido el coordinador transaccional si hace falta.

`*.types.js`, `*.dto.js` y `shared/*` son opcionales: se crean cuando hay contratos, proyecciones o código realmente compartido. `*.types.js` contiene contratos JSDoc, no interfaces TypeScript. No crees archivos vacíos para reproducir el ejemplo.

Organiza módulos por capacidades reales del dominio; los nombres del árbol son ejemplos, no requisitos sectoriales. No uses `administracion` como contenedor genérico de toda la lógica.

Si la propuesta del proyecto establece áreas como `administracion/almacen`, respeta ese agrupamiento. Mantén los archivos del módulo final planos hasta que una subdivisión por casos de uso tenga una necesidad concreta.

## 2. Flujo de petición y dependencias

Una petición de negocio sigue este recorrido:

1. Middlewares generales: identificación de petición, límites y lectura del cuerpo cuando corresponde.
2. Ruta y middlewares del endpoint: autenticación, permisos generales y validación Zod según su contrato.
3. Controlador: extrae los datos validados y el contexto de identidad confiable.
4. Servicio: ejecuta el caso de uso y sus reglas de negocio.
5. Repositorio: consulta o modifica datos mediante Prisma y PostgreSQL cuando el caso requiere persistencia.
6. DTO y respuesta HTTP: proyectan los campos permitidos al contrato externo.

Los endpoints públicos no requieren autenticación por defecto. Los casos sin persistencia no necesitan pasar artificialmente por un repositorio. Los errores de cualquier etapa llegan al manejador centralizado.

El flujo de ejecución no debe confundirse con las importaciones:

- Rutas y controladores pertenecen a la adaptación HTTP.
- Servicios reciben dependencias por parámetros o factorías; no importan Express, Prisma ni implementaciones concretas de repositorios.
- Repositorios implementan operaciones de persistencia y no importan servicios o controladores.
- `index.js` conecta las implementaciones reales. No necesitas un contenedor de inyección de dependencias.
- Los módulos colaboran por entradas públicas o contratos, evitando importaciones de archivos internos y dependencias circulares.

## 3. Responsabilidades por archivo

| Archivo | Responsabilidad | Límite |
| --- | --- | --- |
| `*.routes.js` | Registrar endpoints y sus middlewares | Sin negocio ni consultas |
| `*.schema.js` | Describir entradas y transformaciones explícitas con Zod | Sin consultas ni reglas dependientes de la base de datos |
| `*.controller.js` | Adaptar datos validados, invocar el servicio y responder | Sin negocio ni Prisma |
| `*.service.js` | Ejecutar casos de uso, reglas y autorización sobre recursos | Sin objetos HTTP ni Prisma |
| `*.repository.js` | Implementar consultas, escrituras y mecanismos de persistencia | Sin objetos HTTP ni decisiones de negocio |
| `*.dto.js` | Mapear entradas cuando sea necesario y proyectar respuestas | Sin consultas, autenticación ni decisiones de permisos |
| `*.types.js` | Documentar contratos internos con JSDoc | Opcional; sin validación en ejecución |
| `index.js` | Componer dependencias y publicar el módulo | Sin lógica del caso de uso |

Los servicios coordinan operaciones y pueden tener efectos a través de sus dependencias. La **lógica de dominio** debe permanecer libre de dependencias de infraestructura; eso no convierte a todo el servicio en una función pura.

Los servicios devuelven resultados internos controlados. El controlador aplica la proyección DTO de salida. Un repositorio debe seleccionar los campos necesarios y evitar devolver estructuras Prisma sin control a las capas superiores.

## 4. Validación y contratos

Cada endpoint debe declarar su contrato de entrada y validar con Zod todos los datos del cliente que utilice: `body`, `params`, `query` y, cuando corresponda, cabeceras, cookies o metadatos de archivos específicos.

- Define campos permitidos, obligatoriedad, longitudes, formatos, límites y valores admitidos.
- Rechaza propiedades desconocidas en objetos de entrada de negocio, salvo que el contrato permita explícitamente un objeto extensible.
- Define conversiones deliberadas para valores recibidos como texto; evita coerciones ambiguas de booleanos, fechas o números.
- El middleware guarda el resultado parseado en una propiedad propia, por ejemplo `req.validado`.
- El controlador consume ese resultado y no vuelve a leer el cuerpo original para ejecutar el caso de uso.
- Mensajes de validación en español, con identificación de los campos relevantes y sin reproducir secretos.

Zod comprueba el contrato de entrada. El servicio comprueba reglas que dependen del estado del negocio: disponibilidad, transiciones permitidas, pertenencia a una empresa o autorización sobre un recurso. PostgreSQL garantiza restricciones persistentes como unicidad e integridad referencial.

Los DTOs utilizan selección explícita de campos. No hagas un spread indiscriminado de modelos Prisma ni devuelvas hashes, secretos o relaciones no autorizadas.

Acuerda con frontend la representación de fechas, identificadores, valores decimales, campos opcionales, paginación y errores. Conserva contratos existentes hasta coordinar su cambio; no cambies `data` por otra clave solo por preferencia de idioma.

## 5. Persistencia, transacciones y concurrencia

Los repositorios son la única capa de aplicación que consulta o modifica la base de datos mediante Prisma. Ninguna ruta, middleware, controlador o servicio importa el cliente.

`config/prisma.js` puede construir el cliente y administrar su ciclo de vida. `server.js` puede invocar una función de cierre expuesta para ese fin, sin recibir el cliente ni ejecutar consultas. Scripts de migración o semillas autorizados son herramientas operativas separadas de las capas de petición.

### Transacciones

El servicio decide **qué operaciones deben ser atómicas**; la implementación técnica de la transacción permanece en la capa de repositorios.

- Para una operación compuesta de un repositorio, encapsula la transacción allí.
- Para un caso que coordina varios repositorios, incorpora solo si hace falta `shared/repositories/transacciones.repository.js`.
- Ese coordinador abre la transacción y entrega al callback repositorios vinculados al mismo contexto transaccional.
- El servicio recibe una función como `ejecutarEnTransaccion` y opera con esos repositorios. No recibe `PrismaClient`, `tx` ni promesas Prisma.
- No mezcles, dentro de una operación atómica, repositorios del cliente global y repositorios transaccionales.

En versiones del cliente que utilizan `$transaction`, selecciona escrituras anidadas, transacciones por lote o interactivas según las dependencias del caso. No impongas transacciones interactivas a toda operación de varias tablas. Mantén las transacciones breves y evita llamadas HTTP externas dentro de ellas.

La atomicidad no resuelve por sí sola todos los conflictos de concurrencia. Para stock, saldos, consecutivos o estados sensibles, coordina restricciones, actualizaciones condicionales, aislamiento o reintentos acotados según el caso. No uses una consulta previa de existencia como única garantía de unicidad.

No prometas que una transacción de PostgreSQL revierte un correo o una operación de API externa. Si el flujo mezcla efectos externos y persistencia, define con el asistente principal el comportamiento ante fallos y reintentos.

### Consultas y borrado

- Usa filtros explícitos, selección de campos, ordenamiento estable y paginación con límites.
- Propaga el alcance de empresa o área desde un contexto autorizado cuando corresponda; un identificador enviado por el cliente no prueba pertenencia.
- Evita consultas repetidas innecesarias y carga indiscriminada de relaciones.
- Aplica borrado lógico con `eliminadoEn` solo cuando el dominio lo requiera y define su efecto en consultas, restauración, unicidad e historial.
- No conviertas errores de persistencia en mensajes de negocio engañosos. Traduce los casos conocidos y propaga los inesperados al manejador central.

## 6. Respuestas y errores

Mantén el contrato vigente. Para endpoints nuevos sin contrato previo, utiliza una estructura uniforme como:

```json
{
  "ok": true,
  "mensaje": "Operación realizada correctamente",
  "data": {}
}
```

```json
{
  "ok": false,
  "mensaje": "No se encontró el recurso solicitado",
  "error": "RECURSO_NO_ENCONTRADO"
}
```

Para listas, acuerda metadatos como página, límite y total, o un cursor cuando corresponda. No cambies la estrategia sin coordinarla con frontend.

Usa códigos HTTP según el resultado real: creación, consulta, entrada inválida, falta de autenticación, permiso insuficiente, recurso ausente o conflicto. Una respuesta `204` no lleva cuerpo. No devuelvas `200` para todos los errores.

Centraliza el manejo HTTP en `shared/middlewares/error-handler.middleware.js`. Las clases de error de aplicación viven en `shared/errors/` y no dependen de Express. Registra el manejador después de las rutas y utiliza la propagación de errores asíncronos compatible con la versión instalada de Express.

Los errores internos se registran con contexto y un identificador de petición, sin contraseñas, tokens o datos sensibles innecesarios. El cliente no recibe stack traces, consultas SQL ni mensajes brutos del motor.

## 7. Seguridad

- Almacena hashes de contraseñas con bcryptjs; nunca contraseñas en texto plano ni mediante cifrado reversible. Usa un costo acordado y compatible con la capacidad del servidor.
- Verifica la firma y las restricciones del JWT; decodificarlo no equivale a autenticar. Respeta expiración y los parámetros aprobados del flujo de autenticación.
- Establece la identidad desde credenciales verificadas. No confíes en roles, permisos o identidades enviados en el cuerpo de una petición.
- El middleware controla permisos generales; el servicio comprueba acceso al recurso concreto y su alcance organizacional.
- Si la autenticación necesita consultar usuarios, el middleware llama a un servicio de autenticación que usa su repositorio; no importa Prisma.
- Limita tamaños de entrada y solicitudes sensibles según la configuración de la agencia. Configura CORS y cabeceras de seguridad para los clientes autorizados.
- Mantén secretos en variables de entorno y no los incluyas en código, respuestas o logs.
- No rediseñes almacenamiento de tokens, renovación, revocación o cookies sin coordinar el flujo con frontend y el asistente principal.

## 8. Migraciones y operaciones de datos

Coordina con el Agente de Base de Datos modelos, relaciones, índices, restricciones, migraciones, semillas e integridad referencial.

Antes de ejecutar una operación, identifica el entorno y su efecto. Revisa el cambio de esquema y sus consecuencias sobre los datos existentes; no apliques una migración destructiva incidentalmente para completar un endpoint.

Comandos destructivos como `migrate reset`, eliminación de datos o recreación de una base requieren confirmación humana explícita para la operación y el entorno concretos, salvo que esa autorización ya conste de forma inequívoca en la sesión. Respeta además las salvaguardas de las herramientas utilizadas.

Usa el procedimiento de migración correspondiente a la versión y entorno reales. No sustituyas migraciones revisables por sincronizaciones de esquema que eludan el historial aprobado.


## Puertos, adaptadores y composición

- Puerto de entrada: operación del caso de uso con entradas y resultados independientes del transporte.
- Adaptador de entrada: rutas/controladores HTTP que validan forma y convierten el contexto al contrato del caso de uso.
- Puerto de salida: operaciones de persistencia o integración requeridas por el caso de uso; no devuelve objetos de framework o cliente ORM.
- Adaptador de salida: repositorio y clientes externos, responsables de consultas, mapeo y errores técnicos.
- Composition root: `modules/<dominio>/index.js`, conectado desde `app.js`. `config/prisma.js` administra el recurso técnico; el caso de uso no lo importa.

El archivo `*.service.js` contiene casos de uso. Extraer reglas puras a `*.domain.js` o a una subdivisión de dominio solo cuando se reutilizan en más de un caso de uso o el servicio deja de ser legible. `*.types.js` documenta contratos cuando hace falta. No exigir todos los archivos para una operación sencilla.

Ejemplo conceptual de inyección (sin base real):

```js
export const crearRegistro = ({ repositorio }) => async (entrada, contexto) => {
  // Validar reglas y autorización del caso de uso con el contexto confiable.
  return repositorio.crear(entrada, contexto);
};
```

Un controlador llama al caso de uso; este usa el puerto inyectado; el repositorio adapta el puerto al ORM. Los DTOs de salida permiten solo campos públicos y los errores técnicos se traducen sin filtrar secretos. No enlazar módulos por sus repositorios internos ni crear ciclos.

## Coordinación y verificación
Backend define contrato API y casos de uso; datos revisa esquema, índices, transacciones y migraciones; frontend verifica consumo y estados. Mantener un dueño por artefacto y acordar cambios incompatibles antes de integrarlos. Las pruebas son proporcionales al riesgo: toda lógica no trivial (condiciones, cálculos monetarios, permisos, reglas de negocio) deja al menos una comprobación ejecutable que falle si se rompe; usar puertos sustituidos, persistencia aislada o recorridos con contratos reales solo donde cubran ese riesgo, sin suites redundantes. Los comandos se obtienen del proyecto, no de esta documentación.

Fuentes: [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html), [arquitectura hexagonal de Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture).
