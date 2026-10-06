# Guía de Estándares de Diseño y Motion de Emil Kowalski

Esta suite reúne los estándares de diseño de interfaces, física de animaciones y principios de Apple (*WWDC Designing Fluid Interfaces*) desarrollados por **Emil Kowalski** (diseñador/ingeniero de Linear, Vercel y creador de [Sonner](https://sonner.emilkowal.ski)).

---

## 1. Filosofía Central: Físicas Fluidas e Interrumpibles

Una interfaz deja de sentirse como una computadora y se convierte en una extensión natural del usuario cuando:
1. **Responde en `pointerdown`, no al soltar (`click`):** Reducción total de latencia perceptual.
2. **Manipulación directa 1:1:** El elemento sigue exactamente el dedo o cursor desde el punto donde se agarró, sin saltos al centro.
3. **Interrumpibilidad absoluta:** El usuario puede atrapar cualquier elemento en pleno movimiento y redirigirlo sin esperar a que termine la animación.
4. **Físicas de resorte (*Springs*):** El movimiento no tiene duración fija arbitraria; nace de la masa, amortiguación (*damping*) y velocidad heredada del gesto.

---

## 2. Catálogo de Habilidades Instaladas (14 Skills)

| Skill | Comando / Carpeta | Propósito Principal |
| :--- | :--- | :--- |
| **Apple Design** | [apple-design](skills/apple-design/SKILL.md) | Principios de Apple (WWDC): latencia cero, físicas fluidas, materiales translúcidos, tipografía y feedback háptico. |
| **Animate** | [animate](skills/animate/SKILL.md) | Creación de animaciones web con Motion/Framer Motion seleccionando curvas y duraciones ideales (ej. `ease-out` en entradas, nunca `ease-in`). |
| **Ask Sonner** | [ask-sonner](skills/ask-sonner/SKILL.md) | Guía oficial para la librería de notificaciones Sonner (estándar obligatorio de la agencia en React). |
| **Emil Design Eng** | [emil-design-eng](skills/emil-design-eng/SKILL.md) | Filosofía central de ingeniería de diseño y microinteracciones de clase Linear/Vercel. |
| **Improve Animations** | [improve-animations](skills/improve-animations/SKILL.md) | Auditoría de animaciones en la base de código y generación de planes de mejora técnica ejecutables. |
| **Review Animations** | [review-animations](skills/review-animations/SKILL.md) | Revisión de código de animación basada en estándares estrictos de rendimiento. |
| **Find Animation Opportunities** | [find-animation-opportunities](skills/find-animation-opportunities/SKILL.md) | Detección de momentos en la interfaz donde el movimiento añade valor real vs qué NO animar. |
| **Animation Vocabulary** | [animation-vocabulary](skills/animation-vocabulary/SKILL.md) | Vocabulario técnico preciso para describir físicas y parámetros (`stiffness`, `damping`, `mass`, `response`). |
| **Break UI** | [break-ui](skills/break-ui/SKILL.md) | Pruebas de estrés con datos extremos (textos hiperlargos, cadenas sin espacios, listas vacías, emojis masivos). |
| **Pick UI Library** | [pick-ui-library](skills/pick-ui-library/SKILL.md) | Selección de librerías UI fiables y accesibles (Radix, React Aria, Base UI) evitando componentes reinventados. |
| **Mobile Native** | [mobile-native](skills/mobile-native/SKILL.md) | Optimización para que la web se sienta nativa en teléfonos (bug 100vh, zoom al enfocar inputs, safe areas, retardo de tap). |
| **Prototype** | [prototype](skills/prototype/SKILL.md) | Prototipado rápido de variantes de interfaz con selector interactivo. |
| **Animate Expo** | [animate-expo](skills/animate-expo/SKILL.md) | Animaciones de alto rendimiento en React Native / Expo con React Native Reanimated. |
| **Write Swift** | [write-swift](skills/write-swift/SKILL.md) | Buenas prácticas modernas de Swift 6 y SwiftUI para aplicaciones nativas Apple. |

---

## 3. Hoja de Rendimiento de Animaciones (*Performance Cheatsheet*)

| Problema Común | Causa Raíz | Solución Estándar |
| :--- | :--- | :--- |
| **La animación da tirones (*jank*)** | Se anima `width`, `height`, `top` o `left`. | Animar únicamente `transform` y `opacity` (hilo GPU/Compositor). |
| **La lista larga va lenta al hacer scroll** | Demasiados nodos DOM simultáneos. | Virtualizar con `@tanstack/react-virtual` o similar. |
| **El efecto desenfoque (*blur*) ralentiza** | Filtro `blur()` excesivo. | Mantener los filtros animados de `blur()` por debajo de 20px. |
| **Propiedades aleatorias parpadean** | Uso de `transition: all`. | **Prohibido `transition: all`**. Especificar propiedades exactas (`transition: transform 150ms ease-out`). |
| **React re-renderiza cada frame** | Actualizar estado en un listener de scroll/pointer. | Mutar directamente `ref.current.style` o usar Motion values sin disparar renders de React. |
| **Salto de 1px al comenzar la animación** | Cambio de capa de composición a destiempo. | Añadir `will-change: transform` (solo en el elemento específico y cuando sea necesario). |

---

## 4. Fórmulas de Resorte de Apple

Apple sustituyó el trío clásico masa/rigidez/amortiguación por dos parámetros intuitivos:
- **Damping ratio (amortiguación):**
  - `1.0`: Críticamente amortiguado (suave, sin rebote oscilatorio). **Estándar por defecto para el 90% de la UI.**
  - `0.8`: Con ligero rebote elástico. **Solo cuando el gesto del usuario traía inercia física (flick o lanzamiento).**
- **Response (tiempo de respuesta en segundos):**
  - Menor = más reactivo y rápido (ej. `0.3s` - `0.4s`).

### Valores Oficiales de Apple (WWDC):
- **Desplazar / Reposicionar elemento (ej. PiP):** Damping `1.0`, Response `0.4s`.
- **Rotación:** Damping `0.8`, Response `0.4s`.
- **Panel lateral / Drawer / Sheet:** Damping `0.8`, Response `0.3s`.

---

## 5. Integración con Agentes de la Agencia

1. **[agente-frontend.md](../../agentes/agente-frontend.md):**
   - Utiliza [ask-sonner](skills/ask-sonner/SKILL.md) para toasts y notificaciones.
   - Aplica [mobile-native](skills/mobile-native/SKILL.md) para garantizar ergonomía táctil en choferes y móviles.
   - Aplica [break-ui](skills/break-ui/SKILL.md) antes de entregar componentes para verificar resiliencia ante desbordamientos.

2. **[diseno-motion.md](../../agentes/diseno-motion.md):**
   - Aplica [apple-design](skills/apple-design/SKILL.md) y [animate](skills/animate/SKILL.md) como referencia principal para físicas elásticas, respuestas en menos de 16 ms y directrices WWDC.
   - Realiza auditorías con [improve-animations](skills/improve-animations/SKILL.md) y [review-animations](skills/review-animations/SKILL.md).
