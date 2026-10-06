# Gestión de Marcas y Tono de Voz — Agencia Principal

Este directorio alberga la identidad corporativa, guías de estilo, tono de comunicación y directivas de Voice Builder para cada marca gestionada por la agencia.

---

## 1. Principio de Aislamiento de Voz
Cada marca tiene su propio subdirectorio en `contexts/brands/<nombre_marca>/`. El agente `redes-sociales` y la skill `voice-builder` deben cargar exclusivamente el perfil correspondiente para redactar copys, guiones o publicaciones con absoluta coherencia estilística.

---

## 2. Estructura de una Marca

```txt
contexts/brands/<nombre_marca>/
├── voz_y_tono.md              # Adjetivos de marca, vocabulario prohibido y arquetipo
├── identidad_visual.md        # Paleta de colores, tipografías, logotipo y enlaces a assets
└── ejemplos_dorados.md        # Publicaciones previas aprobadas que sirven de ejemplo (Few-Shot)
```

---

## 3. Plantilla Base para `voz_y_tono.md`

```markdown
# Guía de Voz y Tono: [Nombre de la Marca]

- **Arquetipo:** [El Sabio / El Creador / El Héroe / El Amigo]
- **Tono Principal:** [Profesional, cercano, directo, técnico, inspirador]
- **Palabras Clave Permitidas:** [Términos distintivos que la marca promueve]
- **Palabras Prohibidas:** [Jerga no deseada, clichés o términos de competencia]
- **Estilo de Puntuación y Emojis:** [Uso moderado / Sin emojis / Emojis temáticos]
```
