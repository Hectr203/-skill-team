---
name: interruptible-animation
description: Directiva de animaciones interrumpibles en tiempo real. Garantiza que ninguna transición bloquee la entrada del usuario ni genere saltos visuales al cambiar de dirección o estado a mitad de recorrido.
---

# Microinteracciones Interrumpibles (Interruptible Animation)

Basado en las directivas de interacción de **Emil Kowalski** ([github.com/emilkowalski/skills](https://github.com/emilkowalski/skills)) y los sistemas operativos modernos (iOS, macOS). Establece el principio fundamental para que una interfaz de usuario nunca se sienta rígida, bloqueada o artificial.

---

## 1. La Ley Inviolable de la Interrupción

> [!IMPORTANT]
> **NINGUNA ANIMACIÓN DEBE RETENER EL CONTROL NI BLOQUEAR AL USUARIO**:
> Si un usuario interactúa mientras una animación está en curso (por ejemplo: cerrar un modal mientras aún se abría, presionar otro botón mientras el menú bajaba, o cambiar de tabulación a mitad de una transición), la interfaz **debe responder en ese mismo instante**.
>
> Queda estrictamente prohibido usar `pointer-events: none` prolongados para obligar al usuario a esperar que termine una transición visual.

---

## 2. Por Qué Fallan las Animaciones Clásicas de CSS

Cuando se utiliza una transición CSS con duración fija:
```css
/* ANTIPATRÓN: Produce saltos bruscos (jitter) si el usuario cambia de estado rápidamente */
.bad-drawer {
  transition: transform 0.4s ease-out;
}
```
Si el usuario abre el drawer (avanza 100px) y repentinamente hace clic en cerrar antes de los 400ms:
1. El navegador reinicia la transición desde el inicio de la nueva curva de aceleración.
2. Se produce una desaceleración artificial o un salto de velocidad instantáneo porque el tiempo restante se calcula de forma desvinculada de la inercia actual.
3. La interfaz se siente "torpe" y robótica.

---

## 3. Soluciones de Grado de Producción

### Solución A: Físicas de Resorte con Preservación de Velocidad
Los motores basados en resortes (como Framer Motion o Anime.js con simulación de resorte) preservan la **velocidad momentánea** ($v_0$). Al revertir la dirección:
- La velocidad inicial no se restablece a cero abruptamente.
- El resorte absorbe la inercia existente y redirige el elemento suavemente hacia la nueva posición sin saltos visuales (*zero jitter*).

```tsx
// Implementación recomendada en React
import { motion, AnimatePresence } from 'framer-motion';

export const InterruptibleModal = ({ isOpen, onClose, children }) => (
  <AnimatePresence>
    {isOpen && (
      <motion.div
        initial={{ opacity: 0, scale: 0.94 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.96 }}
        transition={{
          type: 'spring',
          stiffness: 300,
          damping: 28,
        }}
        onClick={onClose}
        className="modal-overlay"
      >
        <div onClick={(e) => e.stopPropagation()} className="modal-body">
          {children}
        </div>
      </motion.div>
    )}
  </AnimatePresence>
);
```

---

### Solución B: Controlador Interrumpible en Anime.js

```typescript
import anime from 'animejs';

class InterruptibleDrawerController {
  private currentAnimation: anime.AnimeInstance | null = null;
  private element: HTMLElement;

  constructor(element: HTMLElement) {
    this.element = element;
  }

  public open() {
    if (this.currentAnimation) {
      this.currentAnimation.pause(); // Pausa instantánea sin salto
    }

    this.currentAnimation = anime({
      targets: this.element,
      translateX: ['-100%', '0%'],
      easing: 'spring(1, 200, 24, 0)',
    });
  }

  public close() {
    if (this.currentAnimation) {
      this.currentAnimation.pause();
    }

    this.currentAnimation = anime({
      targets: this.element,
      translateX: '-100%',
      easing: 'cubicBezier(0.7, 0, 0.84, 0)',
      duration: 150, // Salida rápida
    });
  }
}
```

---

## 4. Lista de Control para Validación de Interrumpibilidad

Antes de dar por finalizado cualquier componente con animación, somételo a estas 4 pruebas:
1. **Prueba del Clic Rápido Doble**: Presionar rápidamente abrir y cerrar. ¿El elemento oscila suavemente o parpadea/salta?
2. **Prueba de Escritura en Formulario**: Al abrir un modal con un campo de texto, ¿el usuario puede comenzar a escribir de inmediato mientras la animación de apertura termina? (Debe tener autofocus funcional sin perder caracteres).
3. **Prueba de Desplazamiento (Scroll Interrupt)**: Si hay un scroll automático hacia una sección, ¿un toque del usuario en la pantalla cancela inmediatamente el desplazamiento sin forzar la vista?
4. **Prueba de Cierre por Escape**: Presionar la tecla `Escape` en cualquier milisegundo de la apertura debe iniciar el cierre inmediato sin demoras.

---

## 5. Referencias Cruzadas
* Para vocabulario y parámetros cuantitativos: ver [`../animation-vocabulary/SKILL.md`](../animation-vocabulary/SKILL.md).
* Para principios de latencia y tactilidad: ver [`../emil-design-eng/SKILL.md`](../emil-design-eng/SKILL.md).
* Para componentes reactivos de React Bits: ver [`../react-bits/SKILL.md`](../react-bits/SKILL.md).
