# Architecture Quality Gate

Esta lista guía una revisión manual; no demuestra que el validador automático compruebe todos estos criterios. Los ejemplos de lenguaje se adaptan al perfil aprobado. En React Native conservar primitives y navegación nativos.

### Structural integrity
- [ ] Lógica del caso de uso en el segmento model de su módulo.
- [ ] Responsabilidades coherentes con arquitectura modular por dominio: módulos por dominio, APIs públicas e dependencias entre módulos y recursos compartidos.
- [ ] All static text/URLs moved to `src/data/mockData.ts`.

### Type safety and syntax
- [ ] Props use `Readonly<T>` interfaces.
- [ ] File is syntactically valid TypeScript (no red squiggles).
- [ ] Placeholders from templates (e.g., `StitchComponent`) have been replaced with actual names.

### Styling and theming
- [ ] Dark mode (`dark:`) applied to all color classes.
- [ ] No hardcoded hex values; use theme-mapped Tailwind classes.