# 07 — Bicep: Configuración y Uso

Este documento detalla la estructura y el uso del archivo **`infraestructura/main.bicep`** que define toda la infraestructura de Azure como código (IaC) para el proyecto **VTP Transporte**.

---

## 1. Estructura de los Archivos de Bicep

El proyecto organiza la infraestructura de la siguiente manera:
```text
vtptransportes/
└── infraestructura/
    ├── main.bicep          ← Archivo principal de IaC (código fuente)
    └── main.json           ← Plantilla ARM compilada automáticamente por Bicep
```

---

## 2. Recursos Creados en Azure

El archivo `main.bicep` aprovisiona los siguientes servicios integrados dentro del mismo grupo de recursos:

1. **Azure App Service Plan (`Microsoft.Web/serverfarms`):** Plan de cómputo en Linux con la SKU **B1** (Capa Básica 1) que aloja la aplicación backend.
2. **Azure App Service Web App (`Microsoft.Web/sites`):** Sitio web de backend que ejecuta Node.js v22.
3. **Azure Static Web App (`Microsoft.Web/staticSites`):** Servicio optimizado para hospedar la aplicación frontend de Vue.js compilada estáticamente.
4. **Azure Database for MySQL Flexible Server (`Microsoft.DBforMySQL/flexibleServers`):** Servidor de base de datos MySQL administrado en su versión flexible.
5. **Azure Database for MySQL Firewall Rules (`Microsoft.DBforMySQL/flexibleServers/firewallRules`):** Reglas para permitir el acceso de IPs de servicios de Azure.
6. **Azure Storage Account (`Microsoft.Storage/storageAccounts`):** Cuenta de almacenamiento con contenedores Blob privados para almacenar archivos cargados por el backend.
7. **Application Insights (`Microsoft.Insights/components`):** Servicio de monitoreo de rendimiento de la aplicación (APM).
8. **Log Analytics Workspace (`Microsoft.OperationalInsights/workspaces`):** Repositorio central para almacenar logs de la infraestructura.

---

## 3. Parámetros de Entrada y Variables Internas

### Parámetros Principales (`main.bicep`):
Para proteger las credenciales, los parámetros sensibles están decorados con `@secure()`, lo que impide que sus valores aparezcan en logs y salidas de consola.

| Parámetro | Tipo | Decorador | Valor por Defecto | Descripción |
|---|---|---|---|---|
| `environmentName` | `string` | Ninguno | `'vtptransportes'` | Nombre base para crear recursos únicos. |
| `location` | `string` | Ninguno | `resourceGroup().location` | Región geográfica donde se crearán los recursos. |
| `webAppName` | `string` | Ninguno | `'smt-transportes-api'` | Nombre de la App Service en Azure. |
| `staticWebAppName` | `string` | Ninguno | `'smt-transportes-web'` | Nombre de la Static Web App. |
| `dbUser` | `string` | Ninguno | `'smtadmin'` | Usuario administrador de MySQL. |
| `dbPassword` | `string` | `@secure()` | *(Ninguno, obligatorio)* | Contraseña del administrador de MySQL. |
| `jwtSecret` | `string` | `@secure()` | *(Ninguno, obligatorio)* | Clave secreta para firmar los tokens JWT del backend. |
| `frontendUrls` | `array` | Ninguno | `['https://blue-bush...net']` | Lista de orígenes autorizados para CORS del backend. |

### Variables Internas:
Las variables internas calculan nombres únicos para los recursos globales, evitando colisiones en Azure:
- `appServicePlanName`: Nombre del plan de hosting (`smt-transportes-plan`).
- `mysqlServerName`: Nombre generado para la base de datos (ej. `mysql-smt-transportes`).
- `storageAccountName`: Nombre de la cuenta de storage sin caracteres especiales.
- `primaryFrontendUrl`: Primer elemento del arreglo `frontendUrls` utilizado para configurar la variable de entorno `FRONTEND_URL` del backend.

---

## 4. Dependencias y Orden de Aprovisionamiento

Bicep calcula automáticamente el orden de creación mediante referencias explícitas o implícitas entre recursos:
1. **Workspace de Log Analytics e Insights** se crean primero.
2. **Storage Account** y **App Service Plan** se configuran a la par.
3. **App Service Web App** depende del Plan, Storage Account e Insights para inyectar sus valores de conexión en las variables de entorno (`appSettings`).
4. **MySQL Flexible Server** se crea y de inmediato se inyecta su regla de firewall (`firewallRule`) para permitir conexiones de Azure.

---

## 5. Comandos de Operación

### Compilación local (de Bicep a JSON ARM):
Este comando valida la sintaxis y genera el archivo `main.json`:
```bash
az bicep build --file infraestructura/main.bicep
```

### Previsualización de Cambios (What-If):
Compara lo que hay en Azure contra tu código Bicep y detalla qué recursos serán modificados, creados o destruidos sin aplicar nada:
```bash
azd provision --preview
```

### Aplicar Cambios de Infraestructura (Aprovisionamiento):
Compila y despliega la infraestructura en Azure utilizando Azure Developer CLI:
```bash
azd provision
```
*(Nota: Este comando te solicitará las credenciales seguras de `dbPassword` y `jwtSecret` en la terminal la primera vez que se configure el ambiente).*
