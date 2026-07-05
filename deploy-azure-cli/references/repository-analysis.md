# Análisis del repositorio

## Objetivo

Construir un modelo verificable del sistema antes de proponer Azure. Inspeccionar en modo de solo lectura y asociar cada conclusión a una ruta, clave de configuración o fragmento relevante.

## Inventario mínimo

Recorrer el repositorio completo, incluidos archivos ocultos no sensibles, sin limitarse al primer `package.json` o proyecto encontrado.

| Área | Evidencia frecuente |
|---|---|
| Componentes | workspaces, soluciones, módulos, subdirectorios, documentación |
| JavaScript/TypeScript | `package.json`, locks, workspaces, Vite/Next/Nuxt configs |
| .NET | `.sln`, `.csproj`, `global.json`, `appsettings*.json` |
| Java/JVM | `pom.xml`, `build.gradle*`, wrappers, manifests |
| Python | `pyproject.toml`, locks, `requirements*.txt`, ASGI/WSGI config |
| Go/Rust/PHP/Ruby | `go.mod`, `Cargo.toml`, `composer.json`, `Gemfile` |
| Contenedores | `Dockerfile*`, Compose, devcontainer, entrypoints |
| Datos | migraciones, schemas, ORM config, seeders, connection factories |
| Entrega | workflows, pipelines, Docker build contexts, deployment manifests |
| Infraestructura | Bicep, ARM, Terraform, Helm, Kubernetes, `azure.yaml` |
| Configuración | `.env.example`, config modules, feature flags, proxy and CORS config |
| Operación | health endpoints, logging, telemetry, schedulers, workers |

Usar los ejemplos solo como pistas. Continuar buscando tecnologías no listadas.

## Modelo por componente

Registrar para cada componente:

1. nombre, ruta y responsabilidad;
2. lenguaje, framework y versiones con evidencia;
3. gestor de paquetes y lockfile autoritativo;
4. build, salida generada e inclusión/exclusión de archivos;
5. comando de inicio y directorio de trabajo;
6. runtime y arquitectura de CPU requeridos;
7. puertos de escucha y si respetan el puerto inyectado por la plataforma;
8. endpoint de salud y tiempo esperado de arranque;
9. estado persistente, temporal y compartido;
10. dependencias síncronas, asíncronas y externas;
11. trabajos programados, consumidores, colas y conexiones persistentes;
12. necesidades de escalado, afinidad de sesión o singleton;
13. exposición pública o privada y protocolos;
14. estrategia de migración, seed y rollback.

## Detección tecnológica

No inferir una tecnología por el nombre de una carpeta. Confirmarla con dependencia, configuración y uso.

Distinguir:

- frontend estático, SSR, ISR y servidor web dinámico;
- API HTTP, gRPC, WebSocket, worker, job y función;
- base relacional, documental, clave-valor, caché y búsqueda;
- ORM de la base real que usa;
- almacenamiento local temporal de almacenamiento duradero;
- proxy solo de desarrollo de proxy necesario en producción;
- proceso de build de configuración de runtime.

Cuando haya señales contradictorias, documentarlas. Un lockfile obsoleto o un Dockerfile no usado no debe gobernar la arquitectura sin corroboración.

## Variables y secretos

Crear una matriz sin copiar valores:

| Variable | Componente | Obligatoria | Secreta | Build/runtime | Origen de evidencia | Valor por entorno conocido |
|---|---|---:|---:|---|---|---|

Buscar acceso a variables en código y compararlo contra ejemplos, CI y configuración. Detectar:

- claves usadas pero no documentadas;
- claves documentadas pero no usadas;
- variables públicas que contienen secretos;
- valores de producción incorporados al bundle;
- cadenas de conexión, tokens, contraseñas, certificados y claves privadas;
- secretos en IaC, historial o archivos versionados.

No imprimir el valor encontrado. Registrar archivo y clase de secreto. Si parece real o estuvo versionado, clasificar como bloqueante y recomendar revocación/rotación; moverlo a Key Vault no invalida una credencial ya expuesta.

## Requisitos de despliegue

Derivar y registrar:

- artefacto desplegable: archivos estáticos, ZIP, paquete, imagen o función;
- build local o remoto y dependencias nativas;
- archivos necesarios en runtime;
- comando de inicio exacto;
- escritura requerida y vida útil de datos;
- orden de arranque y tolerancia a dependencias no disponibles;
- esquema de red y DNS;
- certificados y dominios;
- concurrencia, memoria, CPU y tiempos máximos conocidos;
- backups, RPO, RTO y residencia de datos;
- observabilidad y alertas;
- ambientes y promoción de artefactos.

## Calidad de evidencia

Etiquetar cada dato:

- `CONFIRMADO`: evidencia directa y consistente;
- `INFERIDO`: evidencia indirecta, indicar razonamiento;
- `DESCONOCIDO`: falta información;
- `CONFLICTIVO`: fuentes no coinciden.

No seleccionar infraestructura definitiva mientras un desconocido afecte compatibilidad, seguridad, datos o costo.
