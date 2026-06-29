param location string = resourceGroup().location
param webAppName string = 'smt-transportes-api'
param staticWebAppName string = 'smt-transportes-web'
param appServicePlanName string = 'smt-transportes-plan'
param skuName string = 'B1' // Capa Básica 1 para Linux Web App

// Contraseñas y secretos se reciben como parámetros seguros (sin defaults hardcodeados)
@secure()
param dbPassword string
param dbUser string = 'smtadmin'

@secure()
param jwtSecret string
param frontendUrls array = [
  'https://blue-bush-0d9760810.7.azurestaticapps.net'
]

// Sufijo único para los nombres de recursos globales (empieza con smt)
var uniqueSuffix = 'smt${uniqueString(resourceGroup().id)}'
var dbServerName = '${uniqueSuffix}-db'
var storageAccountName = take('${uniqueSuffix}st', 24) // Storage account name (letras minúsculas y números, max 24)
var appInsightsName = '${uniqueSuffix}-ai'
var logAnalyticsName = '${uniqueSuffix}-law'
var primaryFrontendUrl = frontendUrls[0]

// === 1. Log Analytics & Application Insights ===
resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logAnalyticsName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalyticsWorkspace.id
  }
}

// === 2. Storage Account ===
resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    supportsHttpsTrafficOnly: true
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2022-09-01' = {
  parent: storageAccount
  name: 'default'
}

resource blobContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2022-09-01' = {
  parent: blobService
  name: 'vtptransporte-archivos'
  properties: {
    publicAccess: 'None'
  }
}

// === 3. MySQL Flexible Server ===
resource mysqlServer 'Microsoft.DBforMySQL/flexibleServers@2023-06-30' = {
  name: dbServerName
  location: location
  sku: {
    name: 'Standard_B1s' // SKU más económica para dev/test (Burstable)
    tier: 'Burstable'
  }
  properties: {
    administratorLogin: dbUser
    administratorLoginPassword: dbPassword
    highAvailability: {
      mode: 'Disabled'
    }
    storage: {
      storageSizeGB: 20
      iops: 360
      autoGrow: 'Enabled'
    }
  }
}

resource mysqlFirewall 'Microsoft.DBforMySQL/flexibleServers/firewallRules@2023-06-30' = {
  parent: mysqlServer
  name: 'AllowAllAzureIPs'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0' // Permite el acceso desde otros servicios de Azure (incluyendo la Web App)
  }
}

resource mysqlDatabase 'Microsoft.DBforMySQL/flexibleServers/databases@2023-06-30' = {
  parent: mysqlServer
  name: 'vtptransporte'
  properties: {}
}

// === 4. App Service Plan ===
resource appServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: skuName
  }
  properties: {
    reserved: true // Requerido para App Service en Linux
  }
}

// === 5. Web App (Node.js) ===
resource webApp 'Microsoft.Web/sites@2022-09-01' = {
  name: webAppName
  location: location
  tags: {
    'azd-service-name': 'backend'
  }
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'NODE|22-lts'
      appSettings: [
        { name: 'NODE_ENV', value: 'production' }
        { name: 'PORT', value: '8080' }
        { name: 'SCM_DO_BUILD_DURING_DEPLOYMENT', value: 'true' }
        { name: 'FRONTEND_URL', value: primaryFrontendUrl }
        { name: 'CORS_ALLOWED_ORIGINS', value: join(frontendUrls, ',') }
        { name: 'JWT_SECRET', value: jwtSecret }
        { name: 'JWT_EXPIRES_IN', value: '8h' }
        { name: 'API_BASE_URL', value: 'https://${webAppName}.azurewebsites.net' }
        
        // Base de Datos
        { name: 'DB_HOST', value: mysqlServer.properties.fullyQualifiedDomainName }
        { name: 'DB_PORT', value: '3306' }
        { name: 'DB_NAME', value: 'vtptransporte' }
        { name: 'DB_USER', value: dbUser }
        { name: 'DB_PASSWORD', value: dbPassword }
        { name: 'DB_SSL', value: 'true' }
        { name: 'DB_CONNECT_TIMEOUT_MS', value: '10000' }

        // Storage Account
        { name: 'AZURE_STORAGE_ACCOUNT_NAME', value: storageAccount.name }
        { name: 'AZURE_STORAGE_CONNECTION_STRING', value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};EndpointSuffix=${environment().suffixes.storage}' }
        { name: 'AZURE_STORAGE_CONTAINER_NAME', value: 'vtptransporte-archivos' }

        // Application Insights
        { name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value: appInsights.properties.ConnectionString }
        { name: 'APPINSIGHTS_INSTRUMENTATIONKEY', value: appInsights.properties.InstrumentationKey }

        // Facturama
        { name: 'FACTURAMA_BASE_URL', value: 'https://apisandbox.facturama.mx/' }
        { name: 'FACTURAMA_USERNAME', value: 'YaelAhuatzi' }
        { name: 'FACTURAMA_PASSWORD', value: '100203yaalsmorc!' }
        { name: 'FACTURAMA_API_MODE', value: 'multiemisor' }
        { name: 'FACTURAMA_TIMEOUT_MS', value: '90000' }

        // SMTP
        { name: 'SMTP_HOST', value: 'smtp.gmail.com' }
        { name: 'SMTP_PORT', value: '587' }
        { name: 'SMTP_USER', value: 'creativasoftia@gmail.com' }
        { name: 'SMTP_PASSWORD', value: 'tgco eobn ysqc shdx' }
        { name: 'SMTP_SECURE', value: 'false' }
        { name: 'SMTP_FROM_EMAIL', value: 'creativasoftia@gmail.com' }
      ]
    }
    httpsOnly: true
  }
}

// === 6. Static Web App (Frontend) ===
resource staticWebApp 'Microsoft.Web/staticSites@2022-09-01' = {
  name: staticWebAppName
  location: 'centralus'
  tags: {
    'azd-service-name': 'frontend'
  }
  sku: {
    name: 'Free'
    tier: 'Free'
  }
  properties: {}
}

// Outputs para uso en scripts o validaciones posteriores
output webAppDefaultHostName string = webApp.properties.defaultHostName
output storageAccountName string = storageAccount.name
output dbHostName string = mysqlServer.properties.fullyQualifiedDomainName
