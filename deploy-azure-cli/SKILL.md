---
name: deploy-azure-cli
description: Analizar repositorios, detectar su arquitectura y requisitos, evaluar y justificar servicios de Azure, prevenir fallos de configuración y ejecutar despliegues mediante comandos directos de Azure CLI. Usar al planear, preparar, desplegar, migrar, verificar o diagnosticar aplicaciones de cualquier lenguaje o arquitectura en Azure, especialmente cuando se exige no usar Portal, azd, Bicep, Terraform, scripts ni decisiones rígidas de App Service o Static Web Apps.
---

# Desplegar proyectos adaptativamente con Azure CLI

## Reglas obligatorias

- Basar toda decisión en evidencia del repositorio y en requisitos confirmados. No asumir lenguaje, framework, base de datos, topología ni servicio de Azure.
- Mantener la primera fase estrictamente de solo lectura: no modificar archivos, instalar dependencias, compilar, autenticarse, crear recursos ni cambiar Azure.
- Presentar el diagnóstico, las incertidumbres, los bloqueos y la propuesta antes de modificar código o Azure. Obtener confirmación explícita antes de mutaciones cloud, cambios de red, migraciones o acciones con costo.
- Ejecutar toda consulta, creación, configuración, despliegue y administración de Azure con comandos directos `az`.
- No usar Azure Portal, `azd`, Bicep, ARM templates, Terraform, SWA CLI, scripts Bash/PowerShell, archivos por lotes, bucles, pipelines ni comandos que oculten varios pasos.
- Emitir un comando `az` por paso. No usar asignaciones de shell, sustitución de comandos ni encadenamientos.
- Verificar la sintaxis disponible con `az <grupo> <comando> --help` cuando una opción, extensión o capacidad pueda variar. No inventar comandos.
- No mostrar, registrar ni incorporar secretos. Tratar todo secreto encontrado como incidente potencial y recomendar rotación si estuvo versionado.
- No ejecutar eliminaciones, aperturas de firewall, migraciones destructivas, cambios de SKU o despliegues a producción sin autorización específica.
- Separar comandos locales indispensables de los comandos Azure. Los comandos locales deben proceder de scripts ya definidos por el proyecto y nunca sustituir ni envolver operaciones de Azure.

## Flujo

### 1. Delimitar el trabajo

Determinar repositorio o monorepo, componentes, entorno objetivo, suscripción, región, restricciones de costo, disponibilidad, cumplimiento, datos y ventana de cambio. Marcar como `desconocido` lo que no tenga evidencia; no rellenarlo por intuición.

### 2. Analizar sin modificar

Leer [references/repository-analysis.md](references/repository-analysis.md). Inspeccionar el árbol completo, manifiestos, locks, configuración, contenedores, CI/CD, infraestructura, documentación y código de arranque. Producir:

- inventario de componentes y relaciones;
- matriz de tecnologías con archivo y evidencia;
- comandos de build, inicio, migración y prueba;
- runtime, puertos, health checks, persistencia y procesos secundarios;
- matriz de variables por componente y momento de uso;
- servicios externos, restricciones de red y datos;
- hallazgos clasificados como bloqueante, alto, medio o informativo.

No leer valores secretos cuando basta con identificar nombres de claves o patrones.

### 3. Validar preparación

Leer [references/predeployment-validation.md](references/predeployment-validation.md). Revisar cada regla aplicable, incluyendo CORS, URL de API, proxies de desarrollo, variables de build, puertos, rutas SPA, almacenamiento efímero, migraciones, salud, credenciales y compatibilidad del artefacto.

No convertir una lección de una tecnología concreta en requisito universal. Expresar cada resultado como evidencia, riesgo, corrección y comprobación.

### 4. Seleccionar servicios

Leer [references/azure-service-selection.md](references/azure-service-selection.md). Comparar al menos dos opciones viables por componente, salvo incompatibilidad objetiva. Evaluar:

- ajuste tecnológico y modelo de ejecución;
- artefacto y mecanismo de despliegue disponible mediante `az`;
- red, identidad, secretos y persistencia;
- escalado, disponibilidad y recuperación;
- operación, observabilidad y mantenimiento;
- costo relativo y principales factores de costo;
- limitaciones y riesgos.

Descartar Azure Static Web Apps si el despliegue requerido no puede completarse exclusivamente con `az` en el entorno actual. No sustituir `az` por SWA CLI.

### 5. Presentar la evaluación y detener mutaciones

Usar [references/report-contract.md](references/report-contract.md). Entregar el estado `LISTO`, `LISTO CON CORRECCIONES` o `BLOQUEADO`, junto con arquitectura propuesta, alternativas, correcciones, valores desconocidos y plan ordenado.

Esperar confirmación antes de modificar el repositorio o Azure. Si la solicitud autorizó explícitamente el despliegue y ya confirmó alcance, entorno, costo y acciones de riesgo, continuar sin repetir preguntas resueltas.

### 6. Corregir y volver a validar

Aplicar únicamente correcciones aprobadas. Ejecutar las pruebas existentes y repetir los controles afectados. No desplegar con bloqueantes abiertos salvo aceptación explícita y documentada del riesgo.

### 7. Preparar y ejecutar Azure CLI

Leer [references/azure-cli-execution.md](references/azure-cli-execution.md). Antes de cada familia de comandos:

1. confirmar cuenta, suscripción y ubicación;
2. comprobar proveedores, extensiones, SKU y disponibilidad regional;
3. consultar estado existente para conservar idempotencia;
4. mostrar propósito, sustituciones, resultado esperado y verificación;
5. ejecutar un solo comando;
6. verificar el resultado antes de continuar.

Aprovisionar en orden de dependencia: grupo de recursos; identidad y secretos; red; datos y almacenamiento; cómputo; observabilidad; configuración; artefactos; conexiones; migraciones.

### 8. Verificar y documentar

Validar desde tres perspectivas:

- plano de administración: recursos, configuración, identidades, red y estado;
- plano de aplicación: arranque, logs, health, migraciones y dependencias;
- experiencia externa: frontend, API, CORS, rutas SPA, tiempo real y flujos críticos.

No afirmar que las consultas del plano de administración prueban la experiencia del navegador. Si Azure CLI no puede realizar una comprobación funcional, declararla pendiente y especificar la evidencia externa necesaria sin introducir otra herramienta como sustituto silencioso.

Registrar recursos, URLs no sensibles, comandos `az` ejecutados, resultados, desviaciones, rollback y pendientes. Redactar secretos.

## Condiciones de parada

Detener el despliegue ante cualquiera de estas condiciones:

- secretos versionados sin plan de revocación y reemplazo;
- build o comando de inicio no reproducible;
- runtime, puerto, artefacto o variables obligatorias desconocidos;
- migración sin respaldo, dry-run o rollback adecuado al riesgo;
- selección de servicio incompatible con el proceso o con la restricción de Azure CLI;
- suscripción, región, permisos o presupuesto sin confirmar;
- conectividad propuesta más abierta de lo requerido;
- cambio destructivo no autorizado;
- verificación crítica fallida.
