# Guía Operativa de Impeccable en Agencia Principal

Impeccable es una suite integral de dirección de diseño, artesanía de interfaces de usuario (UI/UX) y detección determinista de anti-patrones de diseño generativo por IA (*AI design slop*).

---

## 1. ¿Por qué existe Impeccable?

La mayoría de los modelos de IA generan código frontend visualmente idéntico y genérico:
- Tipografía Inter o fuentes predeterminadas del sistema para todo.
- Degradados predecibles de morado a azul.
- Jerarquías compuestas exclusivamente por tarjetas dentro de tarjetas (*nested cards*).
- Iconos en cuadros redondeados encima de cada encabezado (*eyebrow/kicker*).
- Texto gris de bajo contraste sobre fondos con color.
- Animaciones con rebote anticuado (*bounce/elastic easing*).

Impeccable transforma a los agentes frontend (`agente-frontend.md` y `diseno-motion.md`) en **directores de diseño de clase mundial**, estableciendo un estándar inflexible de producción profesional (*out-of-distribution craft*).

---

## 2. Los 24 Comandos de Impeccable

Todos los comandos están disponibles mediante `/impeccable <comando> <objetivo>` o de forma autónoma por los agentes:

### Fase 1: Construcción (Build)
| Comando | Propósito |
| :--- | :--- |
| `/impeccable init` | Entrevista estratégica inicial que captura la verdad duradera del producto en `PRODUCT.md` (audiencia, tono, principios). |
| `/impeccable document` | Analiza el código frontend existente y genera `DESIGN.md` con los tokens y sistema visual actual. |
| `/impeccable extract` | Extrae y consolida componentes repetidos y tokens en el sistema de diseño central. |
| `/impeccable shape` | Planificación profunda de UX/UI y flujos de usuario antes de escribir una sola línea de código. |

### Fase 2: Evaluación (Evaluate)
| Comando | Propósito |
| :--- | :--- |
| `/impeccable critique` | Revisión heurística de UX: jerarquía visual, arquitectura de información, resonancia emocional y carga cognitiva. |
| `/impeccable audit` | Auditoría técnica rigurosa: contraste WCAG AA/AAA, accesibilidad (a11y), rendimiento de renderizado y responsividad. |

### Fase 3: Refinamiento (Refine)
| Comando | Propósito |
| :--- | :--- |
| `/impeccable polish` | Pase final de calidad antes de producción: alineación subpíxel, consistencia y detalles de acabado. |
| `/impeccable bolder` | Amplifica diseños tímidos, aburridos o excesivamente corporativos dándoles carácter y fuerza visual. |
| `/impeccable quieter` | Suaviza interfaces visualmente agresivas o sobreestimuladas, creando elegancia y balance. |
| `/impeccable distill` | Elimina complejidad innecesaria, ruido visual y elementos superfluos para llegar a la esencia pura. |
| `/impeccable harden` | Blindaje de producción: estados vacíos, manejo de errores, textos desbordados, i18n y resiliencia de datos. |
| `/impeccable onboard` | Diseño de primeras experiencias (FTUX), onboarding progresivo y momentos de activación (*aha moments*). |

### Fase 4: Enriquecimiento (Enhance)
| Comando | Propósito |
| :--- | :--- |
| `/impeccable animate` | Microinteracciones intencionales y físicas de resorte suaves (sin bloquear la interacción del usuario). |
| `/impeccable colorize` | Paletas de color estratégicas, vibrantes y matizadas en interfaces monocromáticas. |
| `/impeccable typeset` | Escala tipográfica intencional, ritmo vertical, longitud de línea (65-75ch) y emparejamiento tipográfico. |
| `/impeccable layout` | Ritmo espacial, márgenes asimétricos intencionales y ruptura de grillas monótonas. |
| `/impeccable delight` | Detalles memorables y toques táctiles que elevan la experiencia de funcional a extraordinaria. |
| `/impeccable overdrive` | Efectos visuales de vanguardia: shaders, física de fluidos, scroll interactivo a 60/120 fps. |

### Fase 5: Corrección e Iteración (Fix & Iterate)
| Comando | Propósito |
| :--- | :--- |
| `/impeccable clarify` | Reescribe microcopy, etiquetas confusas y mensajes de error orientados a la recuperación del usuario. |
| `/impeccable adapt` | Adaptabilidad ergonómica para dispositivos móviles, tablets, pantallas táctiles y escritorio. |
| `/impeccable optimize` | Diagnóstico y solución de caídas de FPS, render jank, reflows y tamaño de bundle. |
| `/impeccable live` | Modo interactivo en navegador para iterar variantes visuales en tiempo real vía Hot Module Reloading. |
| `/impeccable generate` | Generación autónoma de $N$ variantes visuales de un componente específico directamente en el navegador. |

---

## 3. Motor Determinista de Detección (Detector CLI)

Impeccable incluye un motor compilado nativo en Linux x64 ubicado en:
`skills/impeccable/scripts/bin/linux-x64/impeccable`

Este motor ejecuta **61 reglas deterministas** sin requerir llamadas lentas a APIs ni consumir tokens LLM:

```bash
# Escanear archivos o componentes en busca de anti-patrones
skills/impeccable/scripts/impeccable detect src/

# Salida en formato JSON para herramientas automatizadas
skills/impeccable/scripts/impeccable detect --json src/components/

# Escanear enfocándose en tipografía o maquetación
skills/impeccable/scripts/impeccable detect --scope type src/
skills/impeccable/scripts/impeccable detect --scope layout src/
```

### Principales Anti-Patrones Detectados:
- **Fuentes saturadas:** Detección de fuentes cliché como Inter, Arial o fuentes del sistema usadas por defecto.
- **Contraste insuficiente:** Verificación de contraste mínimo (4.5:1 para cuerpo, 3:1 para titulares).
- **Sombras duras tipo pegatina:** Sombras sin desenfoque (`4px 4px 0`) cuando no es estilo neobrutalista explícito.
- **Degradado en texto:** Uso de texto degradado sin justificación tipográfica.
- **Tarjetas anidadas:** Tarjetas dentro de tarjetas en lugar de jerarquía basada en espacio y peso visual.

---

## 4. El Suelo de Calidad (*Craft Floor*)

El archivo [craft-floor.md](reference/craft-floor.md) establece las reglas obligatorias e inquebrantables antes de autorizar cualquier entrega visual:

1. **Superficies del navegador:** La selección de texto, scrollbars personalizadas, anillos de foco accesibles y números en tablas deben estar estilizados acorde a la paleta de la marca.
2. **Rechazo a lo genérico:**
   - No usar emojis como sustitutos de un sistema de iconos coherente (usar Lucide React o SVGs vectoriales).
   - No usar máscaras geométricas baratas sobre fotos; usar transparencias reales o silueteado orgánico.
   - Prohibido el texto gris sobre fondos de color; debe usarse un matiz armónico del color de fondo o primer plano.
   - Prohibido el "eyebrow/kicker" decorativo sobre los títulos principales.

---

## 5. Integración con los Agentes de la Agencia

- **Agente Frontend (`agentes/agente-frontend.md`):**
  Aplica el detector `skills/impeccable/scripts/impeccable detect` y ejecuta `/impeccable audit` y `/impeccable polish` antes de marcar cualquier tarea como completada.

- **Agente de Diseño y Motion (`agentes/diseno-motion.md`):**
  Consulta [craft-floor.md](reference/craft-floor.md), `/impeccable animate`, `/impeccable delight` y `/impeccable typeset` para garantizar animaciones a 60/120 fps e identidades visuales memorables.
