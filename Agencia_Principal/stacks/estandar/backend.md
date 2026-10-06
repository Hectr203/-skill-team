# Stack Estándar: Backend (Node.js 22 LTS + Express + JavaScript ES Modules)

Este documento define las especificaciones técnicas obligatorias para el desarrollo de backend bajo el stack oficial predeterminado de la agencia.

---

## 1. Tecnologías y Dependencias Base

- **Runtime:** Node.js 22 LTS
- **Framework:** Express.js 4.x / 5.x
- **Lenguaje:** JavaScript moderno (ECMAScript 2024+ con ES Modules `"type": "module"`)
- **ORM:** Prisma ORM 6.x / 7.x
- **Base de Datos:** PostgreSQL 16+
- **Seguridad:** JWT (`jsonwebtoken`), hash de contraseñas (`bcryptjs`), sanitización y CORS.
- **Herramientas de Ejecución y Pruebas:** `node --watch` (nativo en Node 22) o `nodemon`, Jest o runner nativo `node --test`.

Dependencias recomendadas en `package.json`:
```json
{
  "name": "backend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "node --watch src/server.js",
    "start": "node src/server.js",
    "test": "node --test tests/**/*.test.js",
    "prisma:migrar": "prisma migrate dev",
    "prisma:generar": "prisma generate",
    "prisma:semilla": "node prisma/seed.js"
  },
  "dependencies": {
    "@prisma/client": "^6.0.0",
    "bcryptjs": "^2.4.3",
    "cors": "^2.8.5",
    "dotenv": "^16.4.5",
    "express": "^4.21.0",
    "jsonwebtoken": "^9.0.2"
  },
  "devDependencies": {
    "prisma": "^6.0.0"
  }
}
```

---

## 2. Estructura de Directorios (Clean Architecture en JavaScript)

```txt
backend/
├── src/
│   ├── app.js                         # Configuración de Express, middlewares y rutas
│   ├── server.js                      # Arranque del servidor y conexión a base de datos
│   ├── configuracion/                 # Variables de entorno y configuración general
│   ├── middlewares/                   # Autenticación, manejo global de errores y validación
│   ├── modulos/                       # Módulos organizados por dominio de negocio
│   │   └── <nombre_modulo>/
│   │       ├── dominio/               # Entidades y reglas de negocio puras
│   │       ├── aplicacion/            # Casos de uso y lógica de aplicación
│   │       ├── infraestructura/       # Repositorio con Prisma y llamadas externas
│   │       └── interfaces/            # Controladores HTTP y rutas Express
│   └── utilidades/                    # Respuestas JSON estándar y helpers puros
├── prisma/
│   ├── schema.prisma                  # Esquema declarativo de base de datos
│   └── seed.js                        # Datos iniciales para desarrollo y pruebas
├── tests/                             # Pruebas unitarias y de integración
├── .env.example
└── package.json
```

---

## 3. Reglas de Código Obligatorias
1. **Nombres en Español**: Controladores (`controladorUsuarios.js`), casos de uso (`crearUsuarioCasoUso.js`), repositorios (`repositorioUsuarios.js`) y variables deben estar estrictamente en español neutro.
2. **Encapsulamiento de Prisma**: Queda terminantemente prohibido importar `@prisma/client` en controladores, rutas o casos de uso. Prisma solo existe dentro de la capa `infraestructura/` del módulo correspondiente.
3. **Manejo Centralizado de Excepciones**: Ningún error debe fugar trazas de stack en producción; todos deben devolver formato `{ "exito": false, "mensaje": "...", "codigo": "..." }`.
4. **Agilidad sin Fatiga de Tipado**: Se utiliza JavaScript moderno y claro. Las validaciones de entrada se realizan en la capa de interfaz/controlador mediante validación semántica simple, aplicando la filosofía Ponytail & YAGNI.
