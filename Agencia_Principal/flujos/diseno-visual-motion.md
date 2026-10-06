# Flujo de Diseño Visual y Motion Engineering

Este flujo garantiza que toda interfaz construida por la agencia alcance acabados visuales de clase mundial (*look & feel* al nivel de Apple, Vercel y Linear), combinando Google Stitch, las directivas de Emil Kowalski, Anime.js y React Bits.

---

## Fases del Flujo

```text
1. Prototipado Stitch ──> 2. Extracción de Tokens ──> 3. Atomic Design ──> 4. Motion Engineering ──> 5. Verificación de Taste y a11y
```

### Fase 1: Prototipado Visual e Inspección (Google Stitch MCP)
1. Conectar con el servidor Stitch MCP para consultar proyectos y pantallas prototipadas.
2. Explorar variantes de interfaz y flujos visuales antes de redactar código de frontend.
3. *Contingencia*: Si Stitch no está disponible, utilizar las 12 bases de datos de `ui-ux-pro-max` (`landing.csv`, `styles.csv`, `colors.csv`) para componer el sistema visual.

### Fase 2: Ingeniería de Design Tokens
1. Extraer paletas semánticas, escala tipográfica armónica y escala de espaciados (4px/8px).
2. Sincronizar los tokens con las variables CSS/Tailwind en `src/shared/theme/`.

### Fase 3: Mapeo y Composición Atómica
1. Identificar átomos y moléculas neutros en `src/shared/components/`.
2. Ensamblar los organismos de dominio dentro de `src/modules/<dominio>/<submodulo>/components/`.

### Fase 4: Motion Engineering (Apple Design, Emil Kowalski, Anime.js, React Bits)
1. **Microinteracciones Interrumpibles**: Ninguna animación debe bloquear al usuario; si el usuario interactúa, la animación debe responder o reorientarse instantáneamente sin saltos.
2. **Físicas de Movimiento Naturales**: Usar resortes con amortiguación realista en lugar de transiciones rígidas; aplicar curvas `ease-out` en entradas.
3. **Sombras Multicapa**: Evitar bordes sólidos negros; utilizar sombras superpuestas semitransparentes para lograr profundidad elegante.
4. **Animaciones de Componentes**:
   - En React: Integrar componentes motion seleccionados de **React Bits** (tilt cards, text animations).
   - Animaciones generales y SVG: Usar la skill de **Anime.js Motion** para timelines y morphing vectorial.

### Fase 5: Verificación de Taste y Accesibilidad
1. Validar la respuesta del componente ante `prefers-reduced-motion` (desactivar movimientos cinéticos y conservar fundidos simples).
2. Inspección visual final mediante el navegador integrado de Google Antigravity o Playwright MCP.
