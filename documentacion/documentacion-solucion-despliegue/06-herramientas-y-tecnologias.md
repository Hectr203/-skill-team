# 06 — Herramientas y Tecnologías

Este documento enumera los lenguajes de programación, frameworks, librerías del sistema, bases de datos y herramientas de infraestructura y despliegue que componen el proyecto **VTP Transporte**.

---

## 1. Tecnologías del Servidor (Backend)

- **Node.js:** Versión recomendada/ejecutada: **v22.x LTS** (LTS actual para el contenedor de Linux de Azure App Service).
- **Express.js:** Versión **^5.2.1** (gestionada en `package.json`). Framework web minimalista para Node.js, utilizado para estructurar las rutas y middlewares.
- **MySQL Driver (`mysql2`):** Versión **^3.11.5**. Conector nativo de Node.js para interactuar con la base de datos MySQL mediante promesas y pools de conexiones.
- **Facturama SDK/HTTP Integration:** Integración REST API directa para la facturación electrónica mexicana mediante peticiones Axios.
- **Nodemailer:** Versión **^6.9.16**. Biblioteca para el envío de correos electrónicos desde Node.js (conectado a Hostinger SMTP en desarrollo y a Gmail SMTP en producción).

---

## 2. Tecnologías del Cliente (Frontend)

- **Vue.js:** Versión **3.x**. Framework progresivo de Javascript para crear interfaces de usuario SPA (Single Page Application).
- **Vite:** Herramienta de compilación rápida para frontend, encargada de empaquetar los assets y levantar el servidor de desarrollo con proxy inverso dinámico.
- **CSS Vanilla:** Utilizado para el diseño visual, garantizando la compatibilidad estándar de navegadores sin frameworks adicionales de CSS como Tailwind CSS.

---

## 3. Infraestructura y Despliegue (Azure DevOps / IaC)

- **Azure Developer CLI (`azd`):** Herramienta unificada de línea de comandos para empaquetar, aprovisionar y desplegar aplicaciones en Azure de forma declarativa mediante `azure.yaml`.
- **Azure CLI (`az`):** CLI nativa de Azure utilizada para comandos administrativos individuales (por ejemplo, gestión de recursos de base de datos, firewall y CORS de plataforma).
- **Bicep:** Lenguaje de sintaxis declarativa para definir la infraestructura de Azure como código (IaC), compilando automáticamente a plantillas ARM en formato JSON (`main.json`).

---

## 4. Base de Datos

- **MySQL Database Server:** Versión **8.0** flexible server.
- **Sistema de Migraciones SQL:** Script personalizado en JS (`migrate-safe.js`) localizado en la carpeta del backend, que se encarga de ejecutar sentencias SQL nativas de forma incremental y registrar los cambios en la tabla interna `_migrations_log`.

---

## 5. Control de Versiones

- **Git:** Utilizado para el control del código fuente. El flujo de trabajo del despliegue productivo está enlazado directamente con la rama de pruebas (`pruebas-cors` o la rama activa de desarrollo) y sincronizado con repositorios de GitHub.
