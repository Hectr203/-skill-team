# Ejecución exclusiva con Azure CLI

## Límite de herramientas

Toda interacción con Azure debe ser un comando directo cuyo ejecutable sea `az`. No usar:

- Portal;
- `azd`;
- Bicep, ARM templates o Terraform;
- SWA CLI;
- scripts `.sh`, `.ps1`, `.bat` o lenguajes auxiliares;
- bucles, funciones, pipes, redirecciones o comandos encadenados;
- sustitución `$(...)` o asignaciones de variables de shell;
- herramientas externas para ocultar aprovisionamiento.

Los builds y migraciones propios del proyecto no son administración de Azure. Presentarlos aparte, solo si son indispensables, ya existen en el proyecto y están autorizados. Nunca hacer que invoquen Azure a espaldas del procedimiento.

## Formato obligatorio de cada paso

Para cada comando indicar:

- **Propósito**
- **Comando**
- **Sustituir**: cada `<PLACEHOLDER>`
- **Resultado esperado**
- **Verificar con**: otro comando directo `az`, cuando exista
- **Rollback o recuperación**: si el cambio lo requiere

No colocar valores reales sensibles. Usar placeholders descriptivos como `<KEY_VAULT_SECRET_FILE>`.

## Preflight

Realizar de forma secuencial:

1. consultar versión de Azure CLI;
2. comprobar autenticación y cuenta activa;
3. seleccionar explícitamente suscripción si no coincide;
4. comprobar tenant y permisos relevantes;
5. comprobar proveedor y extensión requeridos;
6. comprobar ubicación, SKU, cuotas y nombres;
7. mostrar recursos existentes para evitar colisiones;
8. consultar `--help` de comandos variables o no conocidos.

`az login` cambia estado de autenticación y puede requerir interacción; no ejecutarlo durante el análisis de solo lectura sin necesidad y autorización.

## Orden de cambios

Ejecutar un comando y verificarlo antes del siguiente:

1. grupo de recursos;
2. identidades y Key Vault;
3. red, DNS y endpoints privados;
4. datos, backups y almacenamiento;
5. registro de contenedores si aplica;
6. cómputo;
7. observabilidad;
8. configuración y referencias a secretos;
9. artefacto o imagen;
10. enlaces, CORS, dominios y certificados;
11. migraciones aprobadas;
12. validación.

Consultar primero y crear o actualizar solo si es necesario. No convertir “command succeeded” en prueba de que la aplicación funciona.

## Secretos

- Preferir identidad administrada.
- Crear Key Vault y permisos antes de configurar consumidores.
- No incluir secretos literales en comandos, documentación, logs o historial.
- Si Azure CLI necesita cargar un valor, usar un archivo protegido o un mecanismo seguro aprobado y mostrar únicamente su placeholder.
- No recuperar valores de secretos para “verificarlos”. Verificar metadatos, versión, referencia y acceso del consumidor.
- Rotar fuera del flujo cualquier credencial que ya estuvo en Git; simplemente copiarla a Key Vault no corrige la exposición.

## Despliegue por tipo

Confirmar el comando real con `--help` antes de usarlo.

- App Service: evaluar `az webapp deploy` y su tipo de artefacto; comprobar build remoto, startup y app settings.
- Function App: evaluar el subgrupo de deployment soportado para el plan y runtime.
- Container Apps/App Service container: promover una imagen inmutable y configurar por digest o tag controlado.
- Storage static website: habilitar sitio y cargar el directorio compilado con comandos `az storage`; comprobar index y error document.
- Static Web Apps: crear/configurar con `az` no implica que `az` pueda publicar el contenido. No usar SWA CLI como excepción.

No generar ZIP, imagen o bundle con scripts improvisados. Usar el artefacto reproducible producido por el proyecto o declarar el prerrequisito pendiente.

## Configuración

- Conservar configuración existente no relacionada.
- Distinguir valores de build y runtime.
- Evitar comandos que reemplacen colecciones completas si solo debe cambiarse una entrada.
- Verificar configuración efectiva sin revelar secretos.
- Usar referencias de Key Vault e identidad en lugar de cadenas de conexión cuando el servicio y SDK lo soporten.
- Configurar CORS en una sola capa y verificar la otra capa antes de cambiarla.

## Datos y red

- Preferir conectividad privada cuando el requisito lo justifique.
- No abrir acceso global por conveniencia.
- Antes de cambios de firewall, identificar origen, destino, puerto, duración y alternativa privada.
- Antes de migrar, confirmar backup/PITR, compatibilidad, dry-run, ventana y rollback.
- Separar creación del servidor, base, permisos, esquema y datos; son estados distintos.

## Verificación

### Plano de administración

Usar comandos `az ... show`, `list` o equivalentes para comprobar:

- provisioning state;
- SKU, región y endpoints;
- identidad y roles;
- red y acceso público;
- app settings redactados;
- revisiones/deployments;
- health de plataforma y logs disponibles;
- backups y política de retención.

### Plano de aplicación

Usar capacidades de Azure CLI del servicio para consultar logs, revisiones, réplicas, deployment status y métricas. Evitar imprimir entornos completos si contienen secretos.

`az rest` puede ser útil solo si la versión instalada admite la URL, autenticación y cabeceras requeridas. Consultar su ayuda. No asumir que prueba CORS del navegador o un flujo de usuario.

### Comprobación externa

Reconocer el límite: Azure CLI administra Azure, pero no siempre simula un navegador, WebSocket o cliente del negocio. Si no existe una comprobación válida con `az`, registrar la prueba externa como pendiente con URL, origen, método, resultado esperado y responsable. No introducir `curl` u otra CLI dentro del procedimiento exclusivo.

## Fallos y rollback

- Detenerse al primer resultado inesperado que pueda afectar pasos posteriores.
- Capturar error redactado, estado observado y último comando.
- No reintentar cambios no idempotentes a ciegas.
- Aplicar rollback explícito y verificado cuando esté definido.
- Si el rollback de datos no es seguro, escalar y conservar evidencia.
