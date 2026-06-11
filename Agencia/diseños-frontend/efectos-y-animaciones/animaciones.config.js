// tailwind-config/animaciones.config.js
// Keyframes y animaciones custom del proyecto.
// Fusionar dentro de theme.extend en tailwind.config.js
// (Con Tailwind v4, declarar como @keyframes en el CSS global — ver bloque al final)

module.exports = {
  theme: {
    extend: {
      keyframes: {
        // Entrada estándar de vistas y cards (fade + slide up)
        viewIn: {
          '0%':   { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        // Fade simple
        fadeIn: {
          '0%':   { opacity: '0' },
          '100%': { opacity: '1' },
        },
        // Salida del loader de pantalla completa
        fadeOut: {
          '0%':   { opacity: '1', visibility: 'visible' },
          '100%': { opacity: '0', visibility: 'hidden' },
        },
        // Logo "respirando" en la pantalla de carga
        breathe: {
          '0%, 100%': { transform: 'scale(1)',    opacity: '1' },
          '50%':      { transform: 'scale(1.08)', opacity: '0.85' },
        },
        // Barra de progreso indeterminada del loader
        loaderBar: {
          '0%':   { transform: 'translateX(-120%)' },
          '100%': { transform: 'translateX(420%)' },
        },
        // Shimmer para skeletons
        shimmer: {
          '0%':   { backgroundPosition: '200% 0' },
          '100%': { backgroundPosition: '-200% 0' },
        },
        // Flotación suave de blobs del fondo del login
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%':      { transform: 'translateY(-18px)' },
        },
      },
      animation: {
        'view-in':    'viewIn 0.45s cubic-bezier(0.22, 1, 0.36, 1) forwards',
        'fade-in':    'fadeIn 0.4s ease-in forwards',
        'fade-out':   'fadeOut 0.5s ease-out forwards',
        'breathe':    'breathe 1.6s ease-in-out infinite',
        'loader-bar': 'loaderBar 1.2s ease-in-out infinite',
        'shimmer':    'shimmer 1.8s linear infinite',
        'float-slow': 'float 7s ease-in-out infinite',
        'float-mid':  'float 5s ease-in-out infinite',
      },
      transitionTimingFunction: {
        'out-quint': 'cubic-bezier(0.22, 1, 0.36, 1)',
      },
    },
  },
};

/* ============================================================
   TAILWIND v4 — equivalente en CSS global (app.css):

   @theme {
     --ease-out-quint: cubic-bezier(0.22, 1, 0.36, 1);
   }

   @keyframes viewIn    { from { opacity:0; transform:translateY(20px) } to { opacity:1; transform:translateY(0) } }
   @keyframes fadeIn    { from { opacity:0 } to { opacity:1 } }
   @keyframes fadeOut   { from { opacity:1 } to { opacity:0; visibility:hidden } }
   @keyframes breathe   { 0%,100% { transform:scale(1) } 50% { transform:scale(1.08); opacity:.85 } }
   @keyframes loaderBar { from { transform:translateX(-120%) } to { transform:translateX(420%) } }
   @keyframes shimmer   { from { background-position:200% 0 } to { background-position:-200% 0 } }
   @keyframes float     { 0%,100% { transform:translateY(0) } 50% { transform:translateY(-18px) } }

   Accesibilidad (obligatorio):
   @media (prefers-reduced-motion: reduce) {
     *, *::before, *::after {
       animation-duration: 0.01ms !important;
       animation-iteration-count: 1 !important;
       transition-duration: 0.01ms !important;
     }
   }
   ============================================================ */
