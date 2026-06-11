# Configuración Tailwind del Proyecto

Define aquí las extensiones, clases custom y configuraciones especiales de Tailwind que quieres usar en el proyecto.

## Extensiones de tailwind.config.js

Documenta qué quieres agregar al archivo `tailwind.config.js`:

```js
// Ejemplo de extensiones que el agente debe aplicar
theme: {
  extend: {
    colors: {
      // Agrega colores custom aquí
      brand: {
        50:  '#...',
        500: '#...',
        900: '#...',
      }
    },
    fontFamily: {
      // Fuentes personalizadas
      sans: ['Inter', 'sans-serif'],
      display: ['Poppins', 'sans-serif'],
    },
    animation: {
      // Animaciones custom
      'fade-in': 'fadeIn 0.4s ease-in forwards',
    },
    keyframes: {
      fadeIn: {
        '0%': { opacity: '0', transform: 'translateY(8px)' },
        '100%': { opacity: '1', transform: 'translateY(0)' },
      }
    },
    borderRadius: {
      // Radios custom si el diseño los requiere
    },
    boxShadow: {
      // Sombras custom
    }
  }
}
```

---

## Clases Utilitarias Frecuentes del Proyecto

<!-- Lista las clases que se repiten mucho para que el agente las use consistentemente -->

| Elemento | Clases a usar siempre |
|---|---|
| Contenedor principal | `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8` |
| Sección con padding | `py-8 md:py-12` |
| Título de página | — |
| Subtítulo | — |
| Texto muted | `text-sm text-gray-500 dark:text-gray-400` |

---

## Plugins de Tailwind instalados

<!-- Documenta si usas plugins como @tailwindcss/forms, @tailwindcss/typography, etc. -->
- [ ] `@tailwindcss/forms` — Estilos base para formularios
- [ ] `@tailwindcss/typography` — Clase `prose` para contenido de texto
- [ ] `tailwindcss-animate` — Animaciones adicionales

---

## Notas especiales
<!-- Cualquier regla de estilo importante para el proyecto -->
