# 04 — Proceso de Implementación

Este documento describe paso a paso cómo se aplicaron los cambios en el backend, la infraestructura y la configuración de Azure para implementar la solución seleccionada, detallando los archivos afectados y los comandos ejecutados.

---

## 1. Archivos Modificados

Los siguientes archivos del proyecto sufrieron modificaciones:

### Backend:
- **`vtp-transporte-backend-main/src/app.js` ([app.js](file:///mnt/nvme/api%20de%20autos/vtptransportes/vtp-transporte-backend-main/src/app.js)):**
  Se añadió la lógica manual para inyectar cabeceras y responder a la solicitud preflight `OPTIONS` con código `204`.

### Infraestructura:
- **`infraestructura/main.bicep` ([main.bicep](file:///mnt/nvme/api%20de%20autos/vtptransportes/infraestructura/main.bicep)):**
  Se eliminó el bloque `cors` en `siteConfig` dentro del recurso `Microsoft.Web/sites`.

---

## 2. Implementación en Código (Backend)

En `vtp-transporte-backend-main/src/app.js`, se restauró el middleware CORS ubicándolo inmediatamente después de la creación de la instancia de la aplicación (`const app = express();`):

```javascript
// ... código previo de dependencias
const app = express();

app.set("trust proxy", 1);

// Definir Set de orígenes permitidos desde las variables de configuración
const allowedOrigins = new Set(env.corsAllowedOrigins);

app.use((req, res, next) => {
  const origin = (req.headers.origin || "").trim().replace(/\/+$/, "");

  if (origin && allowedOrigins.has(origin)) {
    res.setHeader("Access-Control-Allow-Origin", origin);
    res.setHeader("Vary", "Origin");
    res.setHeader("Access-Control-Allow-Methods", "GET,POST,PUT,PATCH,DELETE,OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization, X-API-Key");
    res.setHeader("Access-Control-Max-Age", "86400"); // Caché del preflight por 24 horas
  }

  // Responder de forma inmediata a la petición preflight del navegador
  if (req.method === "OPTIONS") {
    return res.status(204).end();
  }

  return next();
});

app.use(express.json());
// ... código posterior
```

---

## 3. Modificaciones en la Infraestructura (Bicep)

En el archivo `infraestructura/main.bicep`, se localizó el recurso del App Service (`webApp`) y se removió la propiedad `cors` de su configuración:

```bicep
// Configuración anterior:
// siteConfig: {
//   linuxFxVersion: 'NODE|22-lts'
//   cors: {
//     allowedOrigins: frontendUrls
//     supportCredentials: false
//   }
//   appSettings: [ ... ]
// }

// Configuración actual:
siteConfig: {
  linuxFxVersion: 'NODE|22-lts'
  appSettings: [
    { name: 'CORS_ALLOWED_ORIGINS', value: join(frontendUrls, ',') }
    // ... resto de variables ...
  ]
}
```

---

## 4. Comandos de Configuración Ejecutados en Azure

Para asegurar la aplicación de los cambios de forma inmediata y desactivar las políticas antiguas de la plataforma de Azure, se ejecutaron los siguientes comandos usando Azure CLI:

### Paso 1: Eliminar orígenes permitidos en la App Service
Este comando limpia la lista blanca de la plataforma en Azure, eliminando el dominio del frontend de la capa del proxy:
```bash
az webapp cors remove \
  --name smt-transportes-api \
  --resource-group SMT-TRASPORTE-PRODUCCION \
  --allowed-origins 'https://blue-bush-0d9760810.7.azurestaticapps.net'
```

### Paso 2: Desactivar credenciales de CORS en la App Service
Este comando asegura que la propiedad `supportCredentials` se establezca en `false` para evitar conflictos con la nueva inyección manual de Express:
```bash
az resource update \
  --ids /subscriptions/22ec4e8e-d285-43a0-8096-2f95a8d16527/resourceGroups/SMT-TRASPORTE-PRODUCCION/providers/Microsoft.Web/sites/smt-transportes-api/config/web \
  --set properties.cors.supportCredentials=false
```

---

## 5. Despliegue de Código

Finalmente, para subir el código con el middleware inyectado al recurso existente en Azure App Service, se ejecutó:

```bash
azd deploy backend --no-prompt
```

Este comando empaquetó recursivamente el código fuente del backend (`vtp-transporte-backend-main`), lo compiló en el entorno de Azure mediante build automation (`SCM_DO_BUILD_DURING_DEPLOYMENT=true`), y lo puso en marcha en el contenedor productivo.
