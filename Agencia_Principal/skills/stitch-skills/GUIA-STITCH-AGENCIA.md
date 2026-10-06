# Guía Operativa de Google Stitch Skills en Agencia Principal

Esta suite curada reúne las habilidades y directrices técnicas oficiales de **Google Stitch** ([google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills.git)), diseñadas para operar en **sinergia perfecta** con el servidor **Stitch MCP de Google** disponible en nuestro entorno (`mcp/stitch`), eliminando errores de límites de tokens, alucinaciones de parámetros y facilitando la transición desde pantallas generadas hasta código frontend de nivel élite.

---

## 1. Sinergia entre el Stitch MCP y las Habilidades

El servidor MCP de Stitch provee las herramientas básicas de conexión (`create_project`, `generate_screen_from_text`, `upload_design_md`, `apply_design_system`, `get_screen`, etc.). Sin embargo, la interacción directa con el MCP suele fallar sin estas directrices. 

La suite resuelve los siguientes problemas críticos:

| Desafío del MCP de Stitch | Causa Raíz | Solución Aportada por la Suite |
| :--- | :--- | :--- |
| **Fallo al subir archivos grandes (`upload_design_md`)** | El LLM debe emitir el Base64 en el cuerpo del tool call; al superar ~16K tokens de salida, se trunca el payload. | Uso del script [`upload_to_stitch.py`](skills/stitch-upload-to-stitch/scripts/upload_to_stitch.py) que lee el archivo y lo envía directamente por HTTP a la API REST de Stitch. |
| **Error `"Invalid argument"` en `apply_design_system`** | Enviar campos de dimensión o posición (`x`, `y`, `width`, `height`) en `selectedScreenInstances`. | Regla estricta documentada en [`stitch-manage-design-system`](skills/stitch-manage-design-system/SKILL.md): enviar **únicamente** `id` y `sourceScreen`. |
| **Descarga de capturas borrosas (`get_screen`)** | Google CDN sirve miniaturas de baja resolución por defecto en `screenshot.downloadUrl`. | Agregar `=w{width}` al final de la URL antes de descargar, usando el ancho del metadata de la pantalla. |
| **Conflicto de tokens en generación de pantallas** | Poner colores o tipografías en el prompt colisiona con el `designTheme` de Stitch. | [`stitch-generate-design`](skills/stitch-generate-design/SKILL.md) prohíbe hex codes en prompts; el prompt solo define estructura y layout; el tema gobierna el aspecto. |
| **Código HTML plano monolítico** | Stitch devuelve un único bloque HTML con Tailwind y enlaces `href="#"`. | [`stitch-react-components`](skills/stitch-react-components/SKILL.md) y [`stitch-react-vite-dashboard`](skills/stitch-react-vite-dashboard/SKILL.md) descomponen en componentes modulares, `Props` tipadas y `mockData.ts`. |
| **Walkthroughs y demos del producto** | Dificultad para presentar flujos de pantallas interactivas a clientes. | [`stitch-remotion`](skills/stitch-remotion/SKILL.md) orquesta pantallas para generar videos programáticos con paneos, zoom y texto. |

---

## 2. Catálogo de Habilidades Instaladas (15 Skills)

### Módulo A: Diseño y Extracción (`stitch-design`)
1. **[stitch-generate-design](skills/stitch-generate-design/SKILL.md):** Pipeline de estructuración de prompts por secciones (Header, Hero, Content, Footer), mapeo de vocabulario UI/UX y creación de variantes.
2. **[stitch-manage-design-system](skills/stitch-manage-design-system/SKILL.md):** Creación y actualización de sistemas de diseño en Stitch y aplicación estricta a pantallas existentes.
3. **[stitch-upload-to-stitch](skills/stitch-upload-to-stitch/SKILL.md):** Manejo y ejecución de [`upload_to_stitch.py`](skills/stitch-upload-to-stitch/scripts/upload_to_stitch.py) para subir imágenes, HTML o `DESIGN.md` sin límites de tokens.
4. **[stitch-code-to-design](skills/stitch-code-to-design/SKILL.md):** Cadena completa para migrar código frontend existente hacia un proyecto de Stitch.
5. **[stitch-extract-design-md](skills/stitch-extract-design-md/SKILL.md):** Extracción estática de tokens de diseño desde código fuente (React, Vue, Angular, CSS) sin requerir ejecución.
6. **[stitch-extract-static-html](skills/stitch-extract-static-html/SKILL.md):** Captura de HTML estático autosuficiente (utilizando el Browser Subagent nativo o Puppeteer).

### Módulo B: Utilidades y Calidad Semántica (`stitch-utilities`)
7. **[stitch-enhance-prompt](skills/stitch-enhance-prompt/SKILL.md):** Expansión de peticiones iniciales del usuario hacia especificaciones ricas con componentes semánticos y estados.
8. **[stitch-taste-design](skills/stitch-taste-design/SKILL.md):** Reglas anti-clichés de IA (prohíbe resplandores morados/azules genéricos, prohíbe fuentes monótonas en dashboards, impone físicas de resorte).
9. **[stitch-design-md](skills/stitch-design-md/SKILL.md):** Síntesis de un `DESIGN.md` a partir del análisis de pantallas y metadatos de proyectos Stitch.
10. **[stitch-site-md](skills/stitch-site-md/SKILL.md):** Constitución y memoria del proyecto en `.stitch/SITE.md` (roadmap, sitemap, identidad y voz).
11. **[stitch-loop](skills/stitch-loop/SKILL.md):** Bucle autónomo por relevos con `.stitch/next-prompt.md` para construcción de sitios multipágina.

### Módulo C: Construcción y Motion (`stitch-build`)
12. **[stitch-react-components](skills/stitch-react-components/SKILL.md):** Conversión obligatoria de pantallas de Stitch a componentes React modulares con TypeScript, hooks aislados y `<Link>` de React Router.
13. **[stitch-react-vite-dashboard](skills/stitch-react-vite-dashboard/SKILL.md):** Paneles y tableros densos en Vite + React con TanStack Query y tokens de diseño.
14. **[stitch-remotion](skills/stitch-remotion/SKILL.md):** Generación de videos de recorrido (walkthroughs) de interfaces usando Remotion y las pantallas del proyecto.
15. **[stitch-react-native](skills/stitch-react-native/SKILL.md):** Adaptación opcional de pantallas web hacia componentes móviles nativos con `StyleSheet`.

---

## 3. Flujo Operativo Estándar

### Paso 1: Ideación y Refinamiento del Prompt
Cuando se requiera una nueva pantalla o interfaz:
1. Usar [`stitch-enhance-prompt`](skills/stitch-enhance-prompt/SKILL.md) y [`stitch-taste-design`](skills/stitch-taste-design/SKILL.md) para generar un prompt estructurado:
   - **Plataforma:** Web, Desktop-first / Mobile-first.
   - **Secciones:** Header, Hero (sin texto sobrepuesto ni clichés), Contenido primario, Footer.
   - **Regla de oro:** No incluir códigos de color hexadecimales ni nombres de fuentes en el prompt de generación de pantallas.

### Paso 2: Ejecución en Stitch MCP
1. Verificar proyecto con `list_projects` o crear uno nuevo con `create_project`.
2. Generar pantalla con `generate_screen_from_text(projectId, prompt, deviceType)`.
3. Para asociar o actualizar un sistema de diseño:
   - Subir el `DESIGN.md` usando [`upload_to_stitch.py`](skills/stitch-upload-to-stitch/scripts/upload_to_stitch.py) para no saturar el contexto del modelo:
     ```bash
     python3 skills/stitch-skills/skills/stitch-upload-to-stitch/scripts/upload_to_stitch.py \
       --project-id <PROJECT_ID> \
       --file-path .stitch/DESIGN.md \
       --api-key <API_KEY>
     ```
   - Llamar a `create_design_system_from_design_md`.
   - Para aplicar a pantallas existentes, llamar a `apply_design_system` enviando **solamente** `[{"id": "...", "sourceScreen": "..."}]`.

### Paso 3: Descarga en Alta Fidelidad
1. Obtener la pantalla con `get_screen(projectId, screenId)`.
2. Descargar el HTML desde `htmlCode.downloadUrl`.
3. Descargar el screenshot agregando `=w{width}`:
   ```bash
   curl -L -sS "${screenshotUrl}=w${width}" -o .stitch/designs/${page}.png
   ```

### Paso 4: Transición a Código de Producción
1. El **Agente Frontend** toma el HTML descargado y aplica [`stitch-react-components`](skills/stitch-react-components/SKILL.md):
   - Extrae el tema a `src/index.css` o `style-guide.json`.
   - Separa componentes en `src/components/`.
   - Extrae contenido estático a `src/data/mockData.ts`.
   - Reemplaza `href="#"` por navegación con React Router.
2. Si el proyecto requiere motion o presentaciones, el **Agente de Diseño Motion** utiliza [`stitch-remotion`](skills/stitch-remotion/SKILL.md) y las físicas de resorte de [`stitch-taste-design`](skills/stitch-taste-design/SKILL.md) en sinergia con `emilkowalski-skills`.

---

## 4. Integración con Agentes de la Agencia

- **[agente-frontend.md](../../agentes/agente-frontend.md):** Integra Stitch como motor de ideación y utiliza `stitch-react-components` para maquetación limpia.
- **[diseno-motion.md](../../agentes/diseno-motion.md):** Conecta las físicas de resorte y `stitch-remotion` para walkthroughs audiovisuales y micro-interacciones de alto impacto.
- **[skills/impeccable](../impeccable/README.md) & [skills/emilkowalski-skills](../emilkowalski-skills/GUIA-EMILKOWALSKI.md):** Actúan como el filtro de calidad artesanal ("Craft Floor") sobre las pantallas generadas.
