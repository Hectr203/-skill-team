# Efectos y Animaciones

Documenta aquí los efectos visuales que quieres aplicar en el proyecto con Tailwind CSS.

## Formato para agregar un efecto

```
### [Nombre del efecto]
- **Elemento**: (botón / card / navbar / input / tabla / etc.)
- **Clases Tailwind**: `hover:scale-105 transition-transform duration-300`
- **Descripción**: Qué hace y cuándo se activa
- **Referencia visual**: (ruta a captura en capturas-inspiracion/ si existe)
```

---

## Efectos del Proyecto

## 1. LOGIN — Efecto 3D Parallax Tilt (PRIORIDAD ALTA)

### Login Card — Tilt 3D que sigue al cursor
- **Elemento**: Card principal del formulario de login
- **Clases Tailwind**: `transition-transform duration-200 ease-out will-change-transform [transform-style:preserve-3d]`
- **Requiere JS**: Sí (listener `mousemove` sobre el contenedor — ver snippet abajo)
- **Descripción**: La card de login rota en 3D siguiendo la posición del cursor (máx. ±10° en X/Y). Al salir el cursor, regresa suavemente a su posición plana. Los elementos internos (logo, botón) tienen `translateZ` para dar profundidad real.
- **Referencia visual**: `capturas-inspiracion/efecto-login-tilt-3d.html` (demo funcional, abrir en navegador)

```js
// Tilt 3D — vanilla JS, funciona con cualquier framework
const card = document.getElementById('login-card');
const wrapper = document.getElementById('login-wrapper');

wrapper.addEventListener('mousemove', (e) => {
  const rect = wrapper.getBoundingClientRect();
  const x = (e.clientX - rect.left) / rect.width - 0.5;   // -0.5 a 0.5
  const y = (e.clientY - rect.top) / rect.height - 0.5;
  card.style.transform = `perspective(1000px) rotateY(${x * 14}deg) rotateX(${-y * 14}deg)`;
});

wrapper.addEventListener('mouseleave', () => {
  card.style.transform = 'perspective(1000px) rotateY(0deg) rotateX(0deg)';
});
```

```html
<!-- Profundidad interna: capas con translateZ -->
<div id="login-card" class="[transform-style:preserve-3d] transition-transform duration-200 ease-out">
  <img class="[transform:translateZ(60px)]" src="logo.svg" />        <!-- flota más -->
  <form class="[transform:translateZ(30px)]"> ... </form>            <!-- nivel medio -->
  <button class="[transform:translateZ(45px)]">Iniciar sesión</button>
</div>
```

### Fondo del Login — Parallax de capas (entorno que "gira")
- **Elemento**: Fondo de la pantalla de login (blobs / formas / partículas decorativas)
- **Clases Tailwind**: `absolute blur-3xl opacity-40 transition-transform duration-500 ease-out will-change-transform`
- **Requiere JS**: Sí (mismo `mousemove`, cada capa se mueve a distinta velocidad)
- **Descripción**: 2–3 capas decorativas de fondo (gradientes blur tipo "blob") se desplazan en dirección **opuesta** al cursor y a velocidades distintas (capa lejana lenta, capa cercana rápida). Combinado con el tilt de la card, da la sensación de que todo el entorno gira alrededor del login.

```js
// Parallax de capas — factor distinto por capa
const layers = document.querySelectorAll('[data-depth]');
wrapper.addEventListener('mousemove', (e) => {
  const x = (e.clientX / window.innerWidth - 0.5);
  const y = (e.clientY / window.innerHeight - 0.5);
  layers.forEach(layer => {
    const depth = parseFloat(layer.dataset.depth); // ej. 10, 25, 40
    layer.style.transform = `translate(${-x * depth}px, ${-y * depth}px)`;
  });
});
```

```html
<div data-depth="15" class="absolute -top-20 -left-20 w-96 h-96 rounded-full bg-indigo-500/30 blur-3xl"></div>
<div data-depth="30" class="absolute bottom-0 right-0 w-80 h-80 rounded-full bg-cyan-400/20 blur-3xl"></div>
<div data-depth="50" class="absolute top-1/2 left-1/3 w-64 h-64 rounded-full bg-fuchsia-500/20 blur-3xl"></div>
```

### Brillo / Glare sobre la card (opcional, refuerza el 3D)
- **Elemento**: Overlay dentro de la card de login
- **Clases Tailwind**: `pointer-events-none absolute inset-0 rounded-[inherit] opacity-0 transition-opacity duration-300`
- **Descripción**: Un gradiente radial blanco semi-transparente sigue al cursor sobre la card, simulando reflejo de luz sobre vidrio. Se activa en hover.

```js
glare.style.background = `radial-gradient(circle at ${px}% ${py}%, rgba(255,255,255,.25), transparent 60%)`;
```

> **Accesibilidad**: envolver todos los efectos de movimiento en `@media (prefers-reduced-motion: no-preference)` o verificar `window.matchMedia('(prefers-reduced-motion: reduce)')` antes de activar los listeners. En móvil (sin cursor) el tilt se desactiva o se reemplaza con giroscopio opcional.

---

## 2. POST-LOGIN — Pantalla de carga y transiciones de vista

### Pantalla de carga inicial (después de autenticar)
- **Elemento**: Overlay de pantalla completa al entrar al dashboard
- **Clases Tailwind**: `fixed inset-0 z-50 flex items-center justify-center bg-[var(--fondo)] animate-[fadeOut_0.5s_ease-out_1.2s_forwards]`
- **Descripción**: Logo centrado con animación de pulso/respiración + barra de progreso fina. La pantalla completa hace fade-out cuando la vista está lista. Duración objetivo: 0.8–1.5 s máximo (que nunca se sienta lenta).

```html
<div id="loader" class="fixed inset-0 z-50 flex flex-col items-center justify-center gap-6 bg-slate-950">
  <img src="logo.svg" class="w-16 h-16 animate-[breathe_1.6s_ease-in-out_infinite]" />
  <div class="w-40 h-1 rounded-full bg-white/10 overflow-hidden">
    <div class="h-full w-1/3 rounded-full bg-indigo-500 animate-[loaderBar_1.2s_ease-in-out_infinite]"></div>
  </div>
</div>
```

### Transición entre vistas — Fade + Slide Up con stagger
- **Elemento**: Contenedor principal de cada vista + sus cards hijas
- **Clases Tailwind**: contenedor `animate-[viewIn_0.45s_cubic-bezier(0.22,1,0.36,1)_forwards]`; hijos con `opacity-0` + delays escalonados `[animation-delay:80ms]`, `[animation-delay:160ms]`, `[animation-delay:240ms]`
- **Descripción**: Al cambiar de vista, el contenido nuevo entra con fade + desplazamiento de 16–24 px hacia arriba. Las cards internas aparecen en cascada (stagger de 80 ms entre cada una). Es el efecto que más impacto visual da con menos costo.

```html
<section class="animate-[viewIn_0.45s_cubic-bezier(0.22,1,0.36,1)_forwards] opacity-0">
  <div class="card opacity-0 animate-[viewIn_0.4s_ease-out_forwards] [animation-delay:80ms]">KPI 1</div>
  <div class="card opacity-0 animate-[viewIn_0.4s_ease-out_forwards] [animation-delay:160ms]">KPI 2</div>
  <div class="card opacity-0 animate-[viewIn_0.4s_ease-out_forwards] [animation-delay:240ms]">KPI 3</div>
</section>
```

### Skeleton loaders (carga de datos dentro de la vista)
- **Elemento**: Cards, tablas y gráficas mientras llegan los datos
- **Clases Tailwind**: `animate-pulse rounded-lg bg-slate-200 dark:bg-slate-800` o shimmer custom `animate-[shimmer_1.8s_infinite] bg-gradient-to-r from-slate-200 via-slate-100 to-slate-200 bg-[length:200%_100%]`
- **Descripción**: En lugar de spinners, cada componente muestra su silueta gris animada con efecto shimmer (barrido de luz). El layout nunca "salta" cuando llegan los datos.

### Números que cuentan (KPIs animados)
- **Elemento**: Métricas / contadores del dashboard
- **Requiere JS**: Sí (count-up de 0 al valor final en ~0.8 s con easing)
- **Descripción**: Al entrar la vista, los números de KPIs suben animados desde 0. Combinado con el stagger de cards, da el "impacto visual único" en el primer vistazo del dashboard.

### Hover lift en cards interactivas
- **Elemento**: Cards clicables del dashboard
- **Clases Tailwind**: `transition-all duration-300 hover:-translate-y-1.5 hover:shadow-xl hover:shadow-indigo-500/10 hover:ring-1 hover:ring-indigo-500/40`
- **Descripción**: La card se eleva con sombra de color al pasar el cursor.

### Sidebar / Navbar — indicador deslizante
- **Elemento**: Item activo del menú lateral
- **Clases Tailwind**: indicador `absolute transition-all duration-300 ease-[cubic-bezier(0.22,1,0.36,1)]`
- **Descripción**: Una barra/píldora de color se desliza físicamente del item anterior al nuevo al navegar (no aparece/desaparece, viaja).

---

## Efectos base preexistentes

### Botón con efecto lift
- **Elemento**: Botones primarios (acciones principales)
- **Clases Tailwind**: `hover:-translate-y-1 hover:shadow-lg transition-all duration-200 active:scale-95`
- **Descripción**: El botón sube ligeramente al pasar el cursor y se presiona al hacer clic.

### Card con borde glow
- **Elemento**: Cards de información o métricas
- **Clases Tailwind**: `hover:ring-2 hover:ring-indigo-500 hover:ring-offset-2 transition-all duration-300`
- **Descripción**: Al pasar el cursor, aparece un anillo de color alrededor de la card.

### Fade in en carga de página
- **Elemento**: Contenedor principal de vistas
- **Clases Tailwind**: `opacity-0 animate-[fadeIn_0.4s_ease-in_forwards]`
- **Descripción**: Las vistas aparecen suavemente al cargar.

---

## Reglas generales de motion del proyecto

1. **Duraciones**: micro-interacciones 150–250 ms · transiciones de vista 400–500 ms · loaders 1.2–1.8 s por ciclo.
2. **Easing estándar**: `cubic-bezier(0.22, 1, 0.36, 1)` (ease-out-quint) para entradas; `ease-out` para hovers.
3. **Una sola pieza protagonista por pantalla**: en login el tilt 3D, en dashboard el stagger + count-up. No saturar.
4. **Respetar `prefers-reduced-motion`** en todos los efectos (obligatorio).
5. Los keyframes custom (`viewIn`, `shimmer`, `breathe`, `loaderBar`, `fadeOut`) viven en `tailwind-config/animaciones.config.js`.
