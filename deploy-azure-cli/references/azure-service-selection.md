# Selección de servicios de Azure

## Método

Seleccionar por requisito, no por familiaridad. Para cada componente:

1. eliminar opciones incompatibles;
2. comparar al menos dos opciones restantes;
3. validar disponibilidad regional, SKU, límites y comando de despliegue en la versión instalada de Azure CLI;
4. justificar elección y descarte;
5. registrar costo relativo y factores, sin inventar precios.

## Cómputo y frontend

| Necesidad observada | Opciones a evaluar | Factores decisivos |
|---|---|---|
| Archivos estáticos/SPA | Static Web Apps; Storage static website con Front Door/CDN; App Service | despliegue directo con `az`, auth integrada, rutas, headers, CDN, costo |
| Servidor web convencional | App Service; Container Apps | runtime soportado, control de imagen, escalado a cero, procesos, red |
| Contenedor HTTP o microservicio | Container Apps; App Service custom container; AKS | revisión operativa, sidecars, Dapr, Kubernetes real, escalado |
| Evento o ejecución breve | Functions; Container Apps Jobs | triggers, duración, runtime, cold start, reintentos |
| Worker continuo | Container Apps; App Service/WebJob si compatible; AKS | cola, escalado, ciclo de vida y observabilidad |
| SSR/híbrido | App Service; Container Apps; Functions solo si el framework encaja | servidor persistente, build, caché y rutas |
| Kubernetes requerido | AKS | solo con requisitos que justifiquen su complejidad |

### Restricción de Azure CLI

Comprobar si el servicio permite cargar el artefacto exclusivamente mediante `az`, no solo crear el recurso. Si Static Web Apps requiere en ese entorno una acción, workflow o SWA CLI para publicar contenido, descartarlo bajo esta skill o dejar el despliegue bloqueado. Para un frontend estático, Storage static website con `az storage blob upload-batch` puede ser una alternativa, pero evaluar rutas SPA, headers, CDN y seguridad.

No usar un servicio dinámico para archivos estáticos sin explicar el costo operativo adicional.

## Datos y estado

| Requisito | Opciones |
|---|---|
| PostgreSQL | Azure Database for PostgreSQL Flexible Server |
| MySQL | Azure Database for MySQL Flexible Server |
| SQL Server/T-SQL | Azure SQL Database o Managed Instance según compatibilidad |
| Documento/distribución global | Cosmos DB, solo tras validar modelo y consistencia |
| MongoDB compatible | Cosmos DB for MongoDB o servicio compatible evaluado explícitamente |
| Caché | Azure Managed Redis o alternativa actualmente soportada; verificar oferta vigente |
| Objetos/archivos | Blob Storage, Data Lake según semántica |
| Archivos SMB/NFS | Azure Files según protocolo y rendimiento |
| Mensajería | Service Bus para colas/topics empresariales; Storage Queues para casos simples |
| Eventos | Event Grid; Event Hubs para streaming/telemetría |

No seleccionar una base administrada solo por nombre del ORM. Confirmar motor, versión, extensiones, transacciones, conexiones, backup, HA, región, red y estrategia de migración.

## Identidad, secretos, red y observabilidad

Evaluar por defecto:

- Managed Identity para acceso servicio-a-servicio;
- Key Vault para secretos, certificados y rotación;
- VNet integration, private endpoints y private DNS cuando los requisitos lo pidan;
- Front Door, Application Gateway o API Management solo si sus capacidades justifican costo y complejidad;
- Log Analytics y Application Insights/OpenTelemetry según runtime y necesidades;
- alertas accionables, retención y control de costo de logs.

No agregar todos estos servicios mecánicamente. Cada recurso debe mapearse a un requisito.

## Matriz de decisión

Puntuar cualitativamente `favorable`, `neutral`, `desfavorable` o `incompatible`:

| Criterio | Opción A | Opción B | Evidencia |
|---|---|---|---|
| Compatibilidad runtime/artefacto | | | |
| Despliegue exclusivo con `az` | | | |
| Procesos y protocolos | | | |
| Red privada e identidad | | | |
| Persistencia | | | |
| Escalado/disponibilidad | | | |
| Operación y observabilidad | | | |
| Seguridad/compliance | | | |
| Costo relativo | | | |
| Riesgos y límites | | | |

## Validaciones con Azure CLI antes de decidir

Usar comandos directos y de solo lectura apropiados al servicio:

- comprobar versión y extensiones;
- consultar ubicaciones y SKU;
- consultar proveedores y tipos de recurso;
- mostrar estado y configuración de recursos existentes;
- consultar cuotas cuando el grupo de comandos lo permita;
- abrir `--help` del comando de creación, configuración y despliegue.

No asumir que una SKU, runtime o extensión mencionada en documentación histórica sigue disponible.

## Costos

No prometer importes sin región, moneda, uso y fecha. Comparar:

- cómputo mínimo y escalado a cero;
- instancias mínimas, HA y zonas;
- almacenamiento, IOPS, backups y transferencia;
- ejecuciones, solicitudes y mensajes;
- ingestión/retención de logs;
- endpoints privados, gateways y egress;
- ambientes duplicados.

Indicar qué valores faltan para una estimación defendible.
