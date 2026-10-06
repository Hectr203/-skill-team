# Stack Estándar: Frontend (React 18+ + JavaScript JSX + Tailwind CSS)

Este documento define las especificaciones técnicas obligatorias para el desarrollo de interfaces de usuario bajo el stack oficial predeterminado de la agencia.

---

## 1. Tecnologías y Dependencias Base

- **Biblioteca:** React 18+ (con Vite)
- **Lenguaje:** JavaScript moderno (ES Modules + JSX `.jsx`)
- **Estilos:** Tailwind CSS 3.x / 4.x
- **Iconografía:** Lucide React
- **Notificaciones UI:** Sonner
- **Gestión de Estado:** Zustand
- **Cliente HTTP:** Axios
- **Enrutamiento:** React Router DOM 6.x

Dependencias recomendadas en `package.json`:
```json
{
  "name": "frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "axios": "^1.7.0",
    "clsx": "^2.1.1",
    "lucide-react": "^0.450.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.26.0",
    "sonner": "^1.5.0",
    "tailwind-merge": "^2.5.2",
    "zustand": "^4.5.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.1",
    "autoprefixer": "^10.4.20",
    "postcss": "^8.4.47",
    "tailwindcss": "^3.4.13",
    "vite": "^5.4.0"
  }
}
```

---

## 2. Estructura de Directorios (Atomic Design en JavaScript)

```txt
frontend/
├── src/
│   ├── app/                           # Enrutamiento principal y proveedores globales
│   ├── componentes/                   # Sistema de diseño Atomic Design
│   │   ├── atomos/                    # Botones, inputs, badges, tipografía básica (.jsx)
│   │   ├── moleculas/                 # Campos de formulario con etiqueta, tarjetas simples (.jsx)
│   │   ├── organismos/                # Tablas de datos, formularios complejos, cabeceras (.jsx)
│   │   └── plantillas/                # Layouts de página y estructuras maestras (.jsx)
│   ├── modulos/                       # Pantallas y vistas agrupadas por dominio
│   │   └── <nombre_modulo>/
│   │       ├── paginas/               # Componentes de página consumidos por el router (.jsx)
│   │       ├── hooks/                 # Custom hooks específicos del módulo (.js)
│   │       └── servicios/             # Llamadas HTTP con Axios hacia la API (.js)
│   ├── estados/                       # Tiendas globales Zustand (.js)
│   ├── utilidades/                    # Formateadores de fechas, moneda y helpers UI (.js)
│   ├── main.jsx                       # Punto de entrada de la aplicación
│   ├── App.jsx                        # Componente raíz
│   └── index.css                      # Directivas de Tailwind y estilos globales
├── index.html
├── package.json
├── tailwind.config.js
├── postcss.config.js
└── vite.config.js
```

---

## 3. Reglas de Código Obligatorias
1. **Nombres en Español**: Componentes (`BotonPrimario.jsx`, `TablaClientes.jsx`), hooks (`usarAutenticacion.js`), servicios (`servicioClientes.js`) y variables deben estar estrictamente en español neutro.
2. **Atomic Design Estricto**: Todo elemento reutilizable debe catalogarse adecuadamente en su nivel atómico.
3. **Manejo de Estados con Zustand**: No sobrecargar con prop-drilling; estados globales van en tiendas organizadas en `estados/`.
4. **Agilidad y Simplicidad (Cero TypeScript)**: Se utiliza JavaScript con JSX directo (`.jsx`), evitando interfaces o decoradores innecesarios para agilizar el desarrollo y facilitar el mantenimiento.
