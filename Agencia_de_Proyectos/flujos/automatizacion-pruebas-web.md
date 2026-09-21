# Flujo de Automatización y Pruebas Web E2E

Este flujo establece el protocolo de verificación visual y funcional en navegadores reales, aplicando una regla de fallback estricta entre el entorno nativo de Google Antigravity y otros editores.

---

## Regla de Precedencia del Navegador

```text
┌────────────────────────────────────────────────────────────────────────┐
│                      REGLA DE PRECEDENCIA DE NAVEGADOR                 │
├───────────────────────────────────┬────────────────────────────────────┤
│    PRIORIDAD 1: NATIVO ANTIGRAVITY │      PRIORIDAD 2: FALLBACK MCP     │
├───────────────────────────────────┼────────────────────────────────────┤
│ Opera en Google Antigravity IDE.  │ Opera en Cursor, Windsurf, Claude  │
│ Usa el navegador Chrome integrado │ Code, VS Code o terminales CLI.    │
│ con inspección directa de DOM y   │ Activa automáticamente el servidor │
│ grabación automática en WebP.     │ oficial `@playwright/mcp@latest`.  │
└───────────────────────────────────┴────────────────────────────────────┘
```

---

## Fases de Ejecución

### Fase 1: Preparación del Entorno de Pruebas
1. Levantar la aplicación localmente en modo desarrollo o preview (`npm run build && npm run preview`).
2. Esperar confirmación de readiness en el puerto configurado (ej. `https://localhost:5173`).

### Fase 2: Ejecución de Flujos Críticos de Usuario
Verificación automatizada de escenarios clave:
1. **Autenticación y Registro**: Formulario de login, refresco de sesión JWT y cierre de sesión.
2. **Navegación e Interacción**: Despliegue de menús responsivos, apertura de modales y llenado de formularios complejos con validaciones Zod.
3. **Manejo de Errores Visuales**: Comprobación de mensajes de error accesibles ante respuestas HTTP 4xx o 5xx.
4. **Verificación Multidispositivo**: Pruebas en viewports clave:
   - Desktop: 1440x900px
   - Tablet: 768x1024px
   - Móvil: 375x812px

### Fase 3: Accesibilidad (a11y) y Taste Visual
1. Comprobar contraste de colores (mínimo 4.5:1 para texto normal, 3:1 para texto grande).
2. Verificar foco visible y navegación secuencial completa mediante teclado (`Tab`, `Enter`, `Escape`).
3. Validar cumplimiento de la preferencia `prefers-reduced-motion`.

### Fase 4: Reporte de Evidencias
- Captura de artefactos visuales (grabaciones WebP o capturas PNG en caso de fallo).
- Logs de consola limpios sin advertencias de reactividad ni errores no capturados.
- Generación del informe de pruebas en `docs/pruebas/`.
