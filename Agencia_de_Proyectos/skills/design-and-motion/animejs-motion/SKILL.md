---
name: animejs-motion
description: Motor de animaciones de alta precisión con Anime.js. Timelines secuenciales, morphing de SVG, trazado de rutas vectoriales, efectos stagger para cuadrículas, interpolación de métricas y físicas de movimiento elástico sin sobrecarga.
---

# Anime.js Motion Engineering

Guía y recetas de producción para integrar **Anime.js** en proyectos web. Proporciona control milimétrico sobre animaciones complejas de SVG, orquestación secuencial mediante líneas de tiempo (*timelines*), efectos escalonados (*stagger*) e interpolación de números para dashboards y métricas de alto rendimiento.

---

## 1. Repositorio Oficial y Documentación
* **Repositorio GitHub**: [github.com/juliangarnier/anime](https://github.com/juliangarnier/anime)
* **Sitio Oficial y Demos**: [animejs.com](https://animejs.com/)
* **Instalación en proyectos**:
  ```bash
  # Instalación en el frontend
  npm install animejs
  npm install -D @types/animejs
  ```
  O mediante CDN para prototipos rápidos:
  ```html
  <script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>
  ```

---

## 2. Principios de Integración y Rendimiento

1. **Propiedades Aceleradas por Hardware**: Animar exclusivamente `transform` (`translateX`, `translateY`, `scale`, `rotate`) y `opacity`. Evitar animar `width`, `height`, `top` o `left` directamente para prevenir *layout thrashing* o reflujos del navegador.
2. **Ciclo de Vida Limpio en React**: Toda animación en componentes React debe almacenar la instancia en un `ref` y pausar o cancelar la ejecución al desmontar el componente (`animeInstance.pause()`).
3. **Respeto a Preferencias del Usuario**: Detectar siempre `prefers-reduced-motion`:
   ```javascript
   const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
   if (prefersReducedMotion) {
     // Desactivar animaciones o fijar duraciones a 0
   }
   ```

---

## 3. Recetas de Producción Listas para Usar

### Receta 1: Hook Personalizado en React (`useAnime`) Interrumpible

Este hook garantiza que las animaciones se limpien adecuadamente y no acumulen fugas de memoria ni colisiones entre renders:

```typescript
import { useEffect, useRef } from 'react';
import anime from 'animejs';

export function useAnime(
  targetRef: React.RefObject<HTMLElement | SVGElement | null>,
  params: anime.AnimeParams,
  dependencies: any[] = []
) {
  const animationRef = useRef<anime.AnimeInstance | null>(null);

  useEffect(() => {
    if (!targetRef.current) return;

    // Si el usuario prefiere movimiento reducido, saltar animación
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) {
      return;
    }

    // Cancelar animación anterior si estaba corriendo
    if (animationRef.current) {
      animationRef.current.pause();
    }

    // Iniciar animación con el target referenciado
    animationRef.current = anime({
      targets: targetRef.current,
      ...params,
    });

    return () => {
      if (animationRef.current) {
        animationRef.current.pause();
      }
    };
  }, dependencies);

  return animationRef;
}
```

---

### Receta 2: Efecto Escalonado para Cuadrículas y Listas (*Stagger*)

Ideal para revelar tarjetas de productos, elementos de catálogo o filas de una tabla con fluidez:

```typescript
import anime from 'animejs';

export function animateStaggeredGrid(containerSelector: string) {
  return anime({
    targets: `${containerSelector} .grid-card`,
    opacity: [0, 1],
    translateY: [24, 0],
    scale: [0.96, 1],
    delay: anime.stagger(45, { from: 'first', start: 100 }), // 45ms entre cada elemento
    duration: 380,
    easing: 'cubicBezier(0.16, 1, 0.3, 1)', // Curva suave Apple-style
  });
}
```

---

### Receta 3: Línea de Tiempo Secuencial (*Timeline Orchestration*)

Permite encadenar secuencias sincronizadas sin anidar callbacks complejos (`callback hell`):

```typescript
import anime from 'animejs';

export function playHeroSequence(elements: {
  badge: HTMLElement;
  title: HTMLElement;
  cta: HTMLElement;
  illustration: SVGElement;
}) {
  const timeline = anime.timeline({
    easing: 'cubicBezier(0.16, 1, 0.3, 1)',
    duration: 400,
  });

  timeline
    .add({
      targets: elements.badge,
      opacity: [0, 1],
      translateY: [-10, 0],
      duration: 300,
    })
    .add({
      targets: elements.title,
      opacity: [0, 1],
      translateY: [20, 0],
    }, '-=150') // Se solapa 150ms con el anterior para máxima fluidez
    .add({
      targets: elements.cta,
      opacity: [0, 1],
      scale: [0.94, 1],
      duration: 350,
    }, '-=200')
    .add({
      targets: elements.illustration.querySelectorAll('path'),
      strokeDashoffset: [anime.setDashoffset, 0],
      easing: 'easeInOutSine',
      duration: 700,
      delay: anime.stagger(60),
    }, '-=250');

  return timeline;
}
```

---

### Receta 4: Dibujo de Rutas SVG y Morphing Vectorial

#### A. Dibujo progresivo de trazos vectoriales (*Line Drawing*):
```typescript
anime({
  targets: '.svg-path-illustration path',
  strokeDashoffset: [anime.setDashoffset, 0],
  easing: 'easeInOutCubic',
  duration: 900,
  delay: anime.stagger(80),
  direction: 'alternate',
  loop: false,
});
```

#### B. Morphing entre formas SVG compatibles (mismo número de puntos):
```typescript
anime({
  targets: '#morphing-icon-path',
  d: [
    { value: 'M12 2L2 22h20L12 2z' }, // Triángulo
    { value: 'M4 4h16v16H4z' }         // Cuadrado
  ],
  easing: 'easeInOutQuad',
  duration: 500,
  loop: false,
});
```

---

### Receta 5: Interpolación de Números y Métricas para Dashboards

Para contadores en vivo que transmiten dinamismo en dashboards de analítica o páginas de estadísticas:

```typescript
import anime from 'animejs';

export function animateCounter(
  element: HTMLElement,
  targetValue: number,
  formatPrefix: string = '$',
  decimals: number = 0
) {
  const counterObj = { value: 0 };

  anime({
    targets: counterObj,
    value: targetValue,
    round: decimals === 0 ? 1 : 100, // Redondeo entero o decimal
    easing: 'easeOutExpo',
    duration: 1200,
    update: () => {
      const formatted = decimals > 0 
        ? counterObj.value.toFixed(decimals)
        : Math.round(counterObj.value).toLocaleString();
      element.innerText = `${formatPrefix}${formatted}`;
    },
  });
}
```

---

### Receta 6: Simulación de Físicas de Resorte (*Spring Physics*) en Anime.js

Anime.js soporta resortes directamente a través del parámetro de easing `spring(mass, stiffness, damping, velocity)`:

```typescript
// Resorte tipo Apple / Emil Kowalski para modales o tarjetas
anime({
  targets: '.modal-content',
  scale: [0.92, 1],
  opacity: [0, 1],
  easing: 'spring(1, 180, 24, 0)', // masa: 1, rigidez: 180, amortiguación: 24
});

// Microinteracción táctil en botón
anime({
  targets: '.btn-tactile',
  scale: [0.96, 1],
  easing: 'spring(1, 400, 30, 0)', // retorno ultrarrápido y nítido
});
```

---

## 4. Coordinación con las Skills Hermanas
* **Directivas de Taste y Latencia**: Ver [`../emil-design-eng/SKILL.md`](../emil-design-eng/SKILL.md).
* **Parámetros Cuantitativos de Físicas**: Ver [`../animation-vocabulary/SKILL.md`](../animation-vocabulary/SKILL.md).
* **Reglas de Interrupción en Tiempo Real**: Ver [`../interruptible-animation/SKILL.md`](../interruptible-animation/SKILL.md).
* **Componentes React preconstruidos**: Ver [`../react-bits/SKILL.md`](../react-bits/SKILL.md).
