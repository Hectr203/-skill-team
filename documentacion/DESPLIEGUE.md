# Guía de Despliegue — VTP Transporte (Azure Developer CLI)

Este proyecto usa **Azure Developer CLI (`azd`)** para automatizar todo el ciclo de despliegue. Bicep crea y actualiza la infraestructura en Azure (servidores, base de datos, configuración), y `azd` empaqueta y sube el código automáticamente.

No necesitas scripts personalizados ni acceso directo a Azure Portal para desplegar.

---

## 1. Requisitos previos

Instala las siguientes herramientas antes de tu primer despliegue:

### Azure CLI (`az`)

```bash
# Linux/macOS
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Windows (PowerShell)
winget install -e --id Microsoft.AzureCLI
```

### Azure Developer CLI (`azd`)

```bash
# Linux/macOS
curl -fsSL https://aka.ms/install-azd.sh | bash

# Sin permisos de administrador (sin sudo)
export AZD_INSTALL_LOCATION=~/.local/bin && curl -fsSL https://aka.ms/install-azd.sh | bash

# Windows (PowerShell)
powershell -ex AllSigned -c "Invoke-RestMethod 'https://aka.ms/install-azd.ps1' | Invoke-Expression"
```

### Node.js 22.x

Requerido para compilar el código antes de subirlo. Verifica con:

```bash
node --version  # debe mostrar v22.x.x
```

---

## 2. Autenticación (primera vez)

Abre una terminal en la raíz del proyecto (`vtptransportes`) y ejecuta:

```bash
# Iniciar sesión en Azure
az login

# Iniciar sesión en Azure Developer CLI
azd auth login
```

Ambos comandos abrirán una ventana en tu navegador para que inicies sesión con tu cuenta Microsoft/Azure. Solo necesitas hacerlo una vez por máquina (o cuando expire tu sesión).

---

## 3. Comandos de despliegue

### 🚀 `azd up` — Desplegar todo (infraestructura + código)

```bash
azd up
```

Hace el flujo completo de inicio a fin:

1. Compila el Bicep y crea/actualiza la infraestructura en Azure
2. Instala dependencias y compila el código
3. Sube el backend y el frontend a sus respectivos recursos

> Te pedirá el nombre del entorno (usa `produccion` o `vtptransportes`) y la suscripción de Azure la primera vez.

**¿Cuándo usarlo?** Cuando hay cambios en la infraestructura (`main.bicep`) y también en el código.

---

### ☁️ `azd provision` — Solo infraestructura (Bicep)

```bash
azd provision
```

Aplica únicamente los cambios del archivo `infraestructura/main.bicep` (parámetros de base de datos, reglas de firewall, configuración de la App Service, etc.). No toca el código fuente.

**¿Cuándo usarlo?** Cuando solo modificaste `main.bicep` y el código sigue igual.

Si cambia el dominio del frontend en Azure Static Web Apps, actualiza `frontendUrls` en `infraestructura/main.bicep` y vuelve a ejecutar `azd provision`; esa lista controla el CORS de App Service.

---

### 📦 `azd deploy` — Solo código (sin infraestructura)

```bash
# Backend y frontend
azd deploy

# Solo el backend
azd deploy backend

# Solo el frontend
azd deploy frontend
```

Omite la fase de Bicep. Instala dependencias, compila y sube el código directamente al recurso ya existente en Azure. Es el más rápido.

**¿Cuándo usarlo?** La infraestructura ya está creada y solo cambiaste archivos de Node.js o del frontend.

---

## 4. Tabla de decisión rápida

| ¿Qué cambió?                       | Comando                 |
| ------------------------------------- | ----------------------- |
| Solo código (backend o frontend)     | `azd deploy`          |
| Solo infraestructura (`main.bicep`) | `azd provision`       |
| Infraestructura + código             | `azd up`              |
| Solo el frontend                      | `azd deploy frontend` |

---

## 5. ¿Cómo funciona por dentro?

`azd` lee el archivo **`azure.yaml`** en la raíz del proyecto. Ahí está definido qué carpeta es el backend y cuál el frontend.

1. **`azd provision`** compila `infraestructura/main.bicep` y lo envía a Azure Resource Manager para crear o actualizar los recursos.
2. Los recursos de Azure (Web App, Static Web App) tienen tags especiales `azd-service-name: backend` y `azd-service-name: frontend`.
3. **`azd deploy`** hace `npm install` y empaqueta el código en un `.zip`, luego busca en Azure el recurso con el tag correspondiente y lo despliega directamente.

---

## 6. Flujos típicos

### Mergué un PR con cambios de código al main

```bash
git pull
azd deploy backend   # o "azd deploy" si también hay cambios en el frontend
```

### Cambié parámetros en main.bicep (ej. RAM del servidor)

```bash
azd provision
```

### Soy nuevo en el equipo y quiero crear mi propio ambiente de desarrollo

```bash
# 1. Clona el repositorio
git clone <url-del-repo>
cd vtptransportes

# 2. Autentícate
az login
azd auth login

# 3. Despliega todo (crea infraestructura y sube el código)
azd up
# Cuando pregunte el nombre del entorno, usa algo único como "dev-tunombre"
```

---

## 7. Migraciones de base de datos después del despliegue

El despliegue **sube el código** pero **no aplica las migraciones de base de datos** automáticamente. Después de un `azd deploy` o `azd up`, si había migraciones nuevas debes aplicarlas manualmente:

```bash
cd vtp-transporte-backend-main
npm run db:migrate-safe
```

Consulta el documento [MIGRACIONES.md](./MIGRACIONES.md) para instrucciones detalladas sobre el sistema de migraciones.

---

## 8. Errores comunes

### `ERROR: az: command not found`

Azure CLI no está instalado. Ve a la sección de [Requisitos previos](#1-requisitos-previos).

### `ERROR: You are not logged in`

Tu sesión expiró. Corre `az login` y `azd auth login` de nuevo.

### `ERROR: Subscription not found`

No tienes acceso a la suscripción de Azure. Pídele al administrador que te agregue con el rol correspondiente.

### El despliegue tarda más de lo normal

`azd deploy` puede tardar entre 2 y 5 minutos dependiendo del tamaño del código. Es normal. No canceles el proceso.
