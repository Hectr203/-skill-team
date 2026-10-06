---
name: apple-design
description: Directivas de diseño visual de clase mundial inspiradas en los estándares de Apple, Linear y Vercel. Sombras multicapa semitransparentes, jerarquía tipográfica armónica, efectos de vidrio esmerilado (frosted glass), suavizado continuo de esquinas (squircles) y superficies limpias.
---

# Directivas de Diseño Visual: Estándares de Apple, Linear y Vercel

Esta skill condensa las directivas estéticas, matemáticas y visuales para lograr interfaces con acabado de producto de clase mundial, emulando la precisión de **Apple Human Interface Guidelines (HIG)**, el refinamiento de **Linear** y la sobriedad técnica de **Vercel Geist**.

---

## 1. Repositorios y Fuentes Oficiales
* **Apple Human Interface Guidelines**: [developer.apple.com/design/human-interface-guidelines](https://developer.apple.com/design/human-interface-guidelines/)
* **Linear Design System & App**: [linear.app](https://linear.app/)
* **Vercel Geist Design System**: [vercel.com/geist](https://vercel.com/geist)
* **Emil Kowalski Design Engineering**: [github.com/emilkowalski/skills](https://github.com/emilkowalski/skills)

---

## 2. Sistema Canónico de Tokens CSS (Apple-Grade Design System)

Para garantizar consistencia en todo el proyecto, define estos tokens en `src/shared/theme/tokens.css` o `index.css`:

```css
:root {
  /* Paleta Base Light Mode */
  --bg-primary: #FFFFFF;
  --bg-secondary: #F5F5F7;
  --bg-tertiary: #E8E8ED;
  --text-primary: #1D1D1F;
  --text-secondary: #86868B;
  --text-tertiary: #A1A1A6;
  --accent-color: #0071E3; /* Apple Blue */
  --accent-hover: #0077ED;
  
  /* Jerarquía de Sombras Multicapa */
  --shadow-subtle: 0 1px 2px rgba(0, 0, 0, 0.04), 0 2px 4px rgba(0, 0, 0, 0.02);
  --shadow-card: 0 2px 4px rgba(0, 0, 0, 0.04), 0 6px 12px rgba(0, 0, 0, 0.03), 0 12px 24px rgba(0, 0, 0, 0.02);
  --shadow-modal: 0 4px 8px rgba(0, 0, 0, 0.06), 0 12px 24px rgba(0, 0, 0, 0.06), 0 24px 48px rgba(0, 0, 0, 0.04);
  
  /* Radios de Esquina */
  --radius-xs: 6px;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 18px;
  --radius-xl: 24px;
}

.dark {
  /* Paleta Base Dark Mode (OLED & Carbon Depth) */
  --bg-primary: #000000;
  --bg-secondary: #121214;
  --bg-tertiary: #1C1C1E;
  --text-primary: #F5F5F7;
  --text-secondary: #A1A1A6;
  --text-tertiary: #6E6E73;
  --accent-color: #2997FF;
  --accent-hover: #0077ED;
  
  /* Sombras de Oclusión con Borde Iluminado */
  --shadow-subtle: inset 0 1px 0 rgba(255, 255, 255, 0.06), 0 2px 6px rgba(0, 0, 0, 0.6);
  --shadow-card: inset 0 1px 0 rgba(255, 255, 255, 0.08), 0 8px 20px rgba(0, 0, 0, 0.8);
  --shadow-modal: inset 0 1px 0 rgba(255, 255, 255, 0.12), 0 16px 40px rgba(0, 0, 0, 0.9);
}
```

---

## 3. Principio de Sombras Multicapa (Layered Shadows)

La luz natural no produce bordes oscuros duros. Los sistemas de diseño de élite superponen 3 capas con dispersión progresiva:

```css
/* Tarjetas en Light Mode */
.apple-card {
  background: var(--bg-primary);
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: var(--radius-md);
  box-shadow:
    0 1px 2px rgba(0, 0, 0, 0.03),
    0 4px 8px rgba(0, 0, 0, 0.03),
    0 12px 24px rgba(0, 0, 0, 0.02);
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.apple-card:hover {
  transform: translateY(-2px);
  box-shadow:
    0 2px 4px rgba(0, 0, 0, 0.04),
    0 8px 16px rgba(0, 0, 0, 0.04),
    0 20px 32px rgba(0, 0, 0, 0.04);
}
```

---

## 4. Materiales Translúcidos y Vidrio Esmerilado (*Vibrancy / Frosted Glass*)

Para barras de navegación, menús emergentes y barras flotantes estilo iOS / macOS:

```css
.frosted-nav {
  background-color: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(20px) saturate(190%);
  -webkit-backdrop-filter: blur(20px) saturate(190%);
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.dark .frosted-nav {
  background-color: rgba(18, 18, 20, 0.72);
  backdrop-filter: blur(20px) saturate(190%);
  -webkit-backdrop-filter: blur(20px) saturate(190%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
```

---

## 5. Regla Matemática de Anidamiento de Radios (*Corner Smoothing*)

Para evitar que las esquinas de un elemento interior parezcan deformadas dentro de su contenedor:

$$\mathbf{R_{\text{exterior}} = R_{\text{interior}} + \text{Padding}}$$

**Ejemplo Práctico**:
- Contenedor con `padding: 12px`:
- Elemento interior (botón o badge): `border-radius: 8px`
- Contenedor exterior (tarjeta o panel): `border-radius: 20px` (8px + 12px)

---

## 6. Jerarquía Tipográfica de Precisión

* **Escala armónica**:
  - `Hero Display`: 48px - 64px | Peso 700 | Tracking `-0.035em` | Line-height `1.08`
  - `Section Title`: 32px - 40px | Peso 600 | Tracking `-0.025em` | Line-height `1.15`
  - `Card Title`: 18px - 22px | Peso 600 | Tracking `-0.015em` | Line-height `1.25`
  - `Body Regular`: 15px - 16px | Peso 400 | Tracking `-0.005em` | Line-height `1.55`
  - `Footnote / Meta`: 12px - 13px | Peso 500 | Tracking `+0.01em` | Line-height `1.4`
* **Contraste estricto**: Nunca usar grises ilegibles. Asegurar ratio mínimo de contraste de 4.5:1 para texto normal y 7:1 para titulares (WCAG AAA).

---

## 7. Integración con el Ecosistema de la Agencia
* Para la ingeniería de movimiento y microinteracciones: ver [`../emil-design-eng/SKILL.md`](../emil-design-eng/SKILL.md).
* Para parámetros numéricos de resortes: ver [`../animation-vocabulary/SKILL.md`](../animation-vocabulary/SKILL.md).
* Para el catálogo de componentes React: ver [`../react-bits/SKILL.md`](../react-bits/SKILL.md).
* Para animaciones SVG y timelines: ver [`../animejs-motion/SKILL.md`](../animejs-motion/SKILL.md).
* Para base de datos exhaustiva de 50 estilos y 21 paletas: ver [`../ui-ux-pro-max/SKILL.md`](../ui-ux-pro-max/SKILL.md).
