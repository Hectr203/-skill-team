---
name: react-bits
description: Catálogo de componentes interactivos y animaciones de élite para React basado en React Bits. Tarjetas con perspectiva 3D (TiltCard), efectos de foco spotlight, revelación de texto animado (SplitText, BlurText, ShinyText), botones magnéticos y fondos fluidos.
---

# Catálogo de Componentes Motion: React Bits

Guía práctica y recetas de producción basadas en la colección de **React Bits** ([reactbits.dev](https://www.reactbits.dev/) / [github.com/DavidHDev/react-bits](https://github.com/DavidHDev/react-bits)). Proporciona componentes de interacción visual de alto impacto que pueden copiarse e integrarse modularmente en cualquier proyecto React con Tailwind CSS o CSS puro, siguiendo la filosofía de *shadcn/ui* (código abierto, sin dependencias monolíticas innecesarias).

---

## 1. Repositorio Oficial y Fuentes
* **Sitio Web Oficial y Demostraciones**: [reactbits.dev](https://www.reactbits.dev/)
* **Repositorio GitHub**: [github.com/DavidHDev/react-bits](https://github.com/DavidHDev/react-bits)
* **Filosofía**: Componentes autocontenidos que se copian dentro de `frontend/src/shared/components/` o `frontend/src/modules/` adaptando sus colores a los tokens del proyecto.

---

## 2. Categorías Principales

1. **Animaciones de Texto**: Revelación tipográfica de alto impacto (`SplitText`, `BlurText`, `ShinyText`, `TrueFocus`).
2. **Componentes UI Interactivos**: Respuestas táctiles y perspectiva 3D (`TiltCard`, `SpotlightCard`, `MagneticButton`, `AnimatedDock`).
3. **Fondos y Efectos de Ambiente**: Lienzos dinámicos interactivos (`FluidBackground`, `Squares`, `Particles`, `StarBorder`).

---

## 3. Recetas de Componentes Listos para Copiar

### Receta 1: `TiltCard` (Tarjeta 3D con Perspectiva y Brillo Especular)

Efecto de inclinación 3D que responde a la posición del cursor con retorno suave por resorte:

```tsx
import React, { useRef, useState } from 'react';

interface TiltCardProps {
  children: React.ReactNode;
  className?: string;
  maxTilt?: number; // Grados máximos de inclinación (ej. 12)
}

export const TiltCard: React.FC<TiltCardProps> = ({
  children,
  className = '',
  maxTilt = 10,
}) => {
  const cardRef = useRef<HTMLDivElement>(null);
  const [transform, setTransform] = useState('perspective(1000px) rotateX(0deg) rotateY(0deg)');
  const [glarePosition, setGlarePosition] = useState({ x: 50, y: 50, opacity: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotateX = ((y - centerY) / centerY) * -maxTilt;
    const rotateY = ((x - centerX) / centerX) * maxTilt;

    setTransform(`perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) scale3d(1.02, 1.02, 1.02)`);
    setGlarePosition({
      x: (x / rect.width) * 100,
      y: (y / rect.height) * 100,
      opacity: 0.15,
    });
  };

  const handleMouseLeave = () => {
    // Retorno suave por resorte
    setTransform('perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)');
    setGlarePosition((prev) => ({ ...prev, opacity: 0 }));
  };

  return (
    <div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      className={`relative overflow-hidden rounded-2xl transition-transform duration-200 ease-out will-change-transform ${className}`}
      style={{ transform, transformStyle: 'preserve-3d' }}
    >
      {/* Capa de brillo especular dinámico */}
      <div
        className="pointer-events-none absolute inset-0 transition-opacity duration-300"
        style={{
          background: `radial-gradient(circle at ${glarePosition.x}% ${glarePosition.y}%, rgba(255,255,255,${glarePosition.opacity}), transparent 60%)`,
        }}
      />
      {children}
    </div>
  );
};
```

---

### Receta 2: `SpotlightCard` (Tarjeta con Luz Radial Dinámica para Modo Oscuro)

Ideal para interfaces oscuras sofisticadas (estilo Linear / Apple):

```tsx
import React, { useRef, useState } from 'react';

interface SpotlightCardProps {
  children: React.ReactNode;
  className?: string;
  spotlightColor?: string; // Por defecto blanco translúcido
}

export const SpotlightCard: React.FC<SpotlightCardProps> = ({
  children,
  className = '',
  spotlightColor = 'rgba(255, 255, 255, 0.08)',
}) => {
  const divRef = useRef<HTMLDivElement>(null);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [opacity, setOpacity] = useState(0);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!divRef.current) return;
    const rect = divRef.current.getBoundingClientRect();
    setPosition({ x: e.clientX - rect.left, y: e.clientY - rect.top });
  };

  return (
    <div
      ref={divRef}
      onMouseMove={handleMouseMove}
      onMouseEnter={() => setOpacity(1)}
      onMouseLeave={() => setOpacity(0)}
      className={`relative overflow-hidden rounded-xl border border-white/10 bg-zinc-900/80 p-6 text-white backdrop-blur-md transition-all ${className}`}
    >
      <div
        className="pointer-events-none absolute -inset-px transition-opacity duration-300"
        style={{
          opacity,
          background: `radial-gradient(600px circle at ${position.x}px ${position.y}px, ${spotlightColor}, transparent 40%)`,
        }}
      />
      <div className="relative z-10">{children}</div>
    </div>
  );
};
```

---

### Receta 3: `ShinyText` (Texto Metálico Brillante Apple-Style)

Efecto de resplandor continuo que viaja sobre el texto para destacar titulares o badges de producto:

```tsx
import React from 'react';

interface ShinyTextProps {
  text: string;
  className?: string;
  shimmerWidth?: number; // En píxeles
}

export const ShinyText: React.FC<ShinyTextProps> = ({
  text,
  className = '',
}) => {
  return (
    <span
      className={`inline-block bg-gradient-to-r from-neutral-400 via-white to-neutral-400 bg-clip-text font-semibold text-transparent [background-size:200%_100%] animate-shimmer ${className}`}
      style={{
        animation: 'shimmer 2.5s infinite linear',
      }}
    >
      {text}
    </span>
  );
};

// En tu index.css o tailwind.config:
// @keyframes shimmer {
//   0% { background-position: 100% 0; }
//   100% { background-position: -100% 0; }
// }
```

---

### Receta 4: `MagneticButton` (Botón con Atracción Magnética al Cursor)

El botón se desplaza ligeramente hacia el cursor cuando este se encuentra cerca, transmitiendo una sensación física ultra-premium:

```tsx
import React, { useRef, useState } from 'react';

interface MagneticButtonProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
  strength?: number; // Factor de atracción (ej. 0.3)
}

export const MagneticButton: React.FC<MagneticButtonProps> = ({
  children,
  className = '',
  onClick,
  strength = 0.25,
}) => {
  const btnRef = useRef<HTMLButtonElement>(null);
  const [position, setPosition] = useState({ x: 0, y: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLButtonElement>) => {
    if (!btnRef.current) return;
    const { left, top, width, height } = btnRef.current.getBoundingClientRect();
    const centerX = left + width / 2;
    const centerY = top + height / 2;
    const deltaX = (e.clientX - centerX) * strength;
    const deltaY = (e.clientY - centerY) * strength;
    setPosition({ x: deltaX, y: deltaY });
  };

  const handleMouseLeave = () => {
    setPosition({ x: 0, y: 0 });
  };

  return (
    <button
      ref={btnRef}
      onClick={onClick}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      className={`relative transition-transform duration-150 ease-out active:scale-95 ${className}`}
      style={{
        transform: `translate3d(${position.x}px, ${position.y}px, 0)`,
      }}
    >
      {children}
    </button>
  );
};
```

---

### Receta 5: `AnimatedDock` (Barra Estilo macOS con Magnificación de Proximidad)

Emula la icónica barra inferior de macOS calculando el tamaño de cada ícono en función de su distancia euclídea al cursor:

```tsx
import React, { useRef, useState } from 'react';

interface DockItemProps {
  icon: React.ReactNode;
  label: string;
  onClick?: () => void;
}

export const AnimatedDock: React.FC<{ items: DockItemProps[] }> = ({ items }) => {
  const [mouseX, setMouseX] = useState<number | null>(null);

  return (
    <div
      onMouseMove={(e) => setMouseX(e.clientX)}
      onMouseLeave={() => setMouseX(null)}
      className="flex h-16 items-end gap-3 rounded-2xl border border-white/10 bg-neutral-900/70 px-4 pb-3 shadow-2xl backdrop-blur-xl"
    >
      {items.map((item, idx) => (
        <DockIcon key={idx} item={item} mouseX={mouseX} />
      ))}
    </div>
  );
};

const DockIcon: React.FC<{ item: DockItemProps; mouseX: number | null }> = ({
  item,
  mouseX,
}) => {
  const iconRef = useRef<HTMLButtonElement>(null);
  let size = 44; // Tamaño base en px

  if (mouseX !== null && iconRef.current) {
    const rect = iconRef.current.getBoundingClientRect();
    const iconCenter = rect.left + rect.width / 2;
    const distance = Math.abs(mouseX - iconCenter);
    // Fórmula de magnificación gaussiana
    if (distance < 120) {
      size = 44 + (1 - distance / 120) * 26; // Crece hasta 70px
    }
  }

  return (
    <button
      ref={iconRef}
      onClick={item.onClick}
      title={item.label}
      className="flex items-center justify-center rounded-xl bg-neutral-800 text-white transition-all duration-100 ease-out hover:bg-neutral-700"
      style={{ width: `${size}px`, height: `${size}px` }}
    >
      {item.icon}
    </button>
  );
};
```

---

## 4. Estándares de Rendimiento y Accesibilidad
1. **Zero Layout Thrashing**: Todos los efectos se renderizan utilizando transformaciones CSS (`transform: translate3d/scale`) para forzar la aceleración por GPU.
2. **Movimiento Reducido**: Si el usuario tiene `prefers-reduced-motion: reduce`, desactivar las transformaciones dinámicas y mantener los componentes en sus tamaños base estáticos.
3. **Navegación por Teclado**: Todo botón o elemento interactivo debe admitir `:focus-visible` con un anillo nítido de 2px de separación.
