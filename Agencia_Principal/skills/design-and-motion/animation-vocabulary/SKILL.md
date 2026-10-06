---
name: animation-vocabulary
description: Vocabulario formal de físicas de movimiento y parámetros de animación. Tablas cuantitativas de resortes (rigidez/stiffness, amortiguación/damping, masa), curvas de aceleración (cubic-bezier) y tiempos de desfase para interfaces fluidas.
---

# Vocabulario de Animación e Ingeniería de Movimiento

Basado en los estándares de movimiento de **Emil Kowalski** ([github.com/emilkowalski/skills](https://github.com/emilkowalski/skills)) y los sistemas de diseño de Apple, Linear y Vercel. Proporciona la nomenclatura estandarizada y los valores numéricos cuantitativos para diseñar animaciones realistas, predecibles y coherentes.

---

## 1. Tabla de Parámetros de Físicas de Resorte (*Spring Physics*)

| Tipo de Componente | Rigidez (`stiffness`) | Amortiguación (`damping`) | Masa (`mass`) | Comportamiento Resultante |
| :--- | :--- | :--- | :--- | :--- |
| **Botones / Toggles / Badges** | `400 - 500` | `28 - 32` | `0.8` | Respuesta instantánea, nítida, casi sin oscilación. Sensación táctil rápida (<120ms). |
| **Menús Desplegables / Selectores** | `300` | `25 - 28` | `1.0` | Entrada suave y decisiva sin rebote perceptible (~180ms). |
| **Modales / Diálogos Centrales** | `220` | `24 - 26` | `1.0` | Entrada señorial con desaceleración natural (~280ms). |
| **Paneles Laterales (Drawers)** | `180` | `22 - 24` | `1.2` | Inercia elegante para áreas grandes de pantalla (~320ms). |
| **Elementos Arrastrables (Drag & Drop)** | `240` | `20` | `1.0` | Rebote elástico sutil al soltar en la posición final. |
| **Indicadores Lúdicos / Toasts** | `350` | `16 - 18` | `0.9` | Rebote controlado y amigable (*sub-amortiguado*). |

---

## 2. Catálogo de Curvas de Aceleración (*Cubic-Bezier Easings*)

Cuando se emplean transiciones temporales en CSS o JavaScript:

```css
:root {
  /* Entrada Suave (Ease Out) - Para elementos que ingresan a pantalla */
  --ease-out-apple: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-out-quad: cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --ease-out-expo: cubic-bezier(0.19, 1, 0.22, 1);

  /* Salida Rápida (Ease In) - Para elementos que desaparecen */
  --ease-in-swift: cubic-bezier(0.7, 0, 0.84, 0);

  /* Movimiento en Pantalla (Ease In Out) - Para morphing de tamaño o posición */
  --ease-in-out-smooth: cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Reglas de Aplicación Temporal:
1. **Entradas (`enter`)**: Usar siempre `--ease-out-apple` con duración de 200ms a 280ms.
2. **Salidas (`exit`)**: Usar siempre `--ease-in-swift` con duración de 100ms a 160ms.
3. **Cambios de Dimensiones / Reordenamiento**: Usar `--ease-in-out-smooth` con duración de 250ms a 320ms.

---

## 3. Desfases Secuenciales (*Stagger Timing*)

Para listas, cuadrículas y tablas de datos:
* **Intervalo Óptimo**: Entre **30ms y 50ms** por elemento.
* **Límite Máximo de Retardo**: Ningún elemento debe esperar más de **300ms** para iniciar su animación. Si hay más de 8 elementos, agrupar los restantes o limitar el retraso máximo acumulado.
* **Dirección del Desfase**:
  - `from: 'first'`: Lectura estándar de arriba hacia abajo o izquierda a derecha.
  - `from: 'center'`: Expansión radial para cuadrículas o dashboards visuales.

---

## 4. Morfología y Elementos Compartidos (*Layout Morph*)
* Al expandir una tarjeta hacia un modal detallado, sincronizar la interpolación de posición (`top`, `left`) y tamaño (`width`, `height`) usando la técnica FLIP (*First, Last, Invert, Play*).
* Preservar el radio de esquina (`border-radius`) interpolándolo suavemente entre el valor de la tarjeta original y el del modal expandido.

---

## 5. Referencias Cruzadas
* Para microinteracciones y latencia: consultar [`../emil-design-eng/SKILL.md`](../emil-design-eng/SKILL.md).
* Para interrumpibilidad: consultar [`../interruptible-animation/SKILL.md`](../interruptible-animation/SKILL.md).
* Para implementar timelines y stagger con código: consultar [`../animejs-motion/SKILL.md`](../animejs-motion/SKILL.md).
* Para componentes reactivos preconstruidos: consultar [`../react-bits/SKILL.md`](../react-bits/SKILL.md).
