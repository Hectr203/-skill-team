---
name: playwright-mcp-testing
description: QA y testing con Playwright MCP para proyectos existentes. Usar para escribir y ejecutar pruebas E2E, de integracion y regresion con Playwright. Se adapta al framework de pruebas ya presente en el repositorio.
---

# Playwright MCP Testing para Proyectos Existentes

## Proposito
Agregar o extender cobertura de pruebas con Playwright en proyectos ya iniciados, respetando el setup existente y sin romper configuraciones previas. Cuando el proyecto ya tenga un framework de pruebas (Vitest, Jest, Mocha), Playwright se suma solo para E2E e integracion.

## Prerequisitos
- Node.js compatible con el proyecto existente.
- Si ya existe framework de pruebas, mantenerlo y agregar Playwright solo para E2E.
- Playwright MCP server disponible para los agentes.

## Diagnostico inicial
1. Revisar `package.json` para ver que framework de testing ya existe.
2. Revisar `playwright.config.ts` si ya existe configuracion.
3. Revisar `tests/` o `__tests__/` para patrones existentes.
4. Identificar flujos criticos sin cobertura.

## Cuando NO agregar Playwright
- El proyecto ya tiene E2E con Cypress/Cypress Cloud y funciona.
- Solo se necesitan pruebas unitarias (usar Vitest/Jest existente).
- El proyecto no tiene interfaz web (CLI, libreria, backend puro).

## Instalacion (si no existe)
```bash
npm install -D @playwright/test
npx playwright install --with-deps chromium
```

## Configuracion (adaptativa)
```typescript
// playwright.config.ts (junto a config existente)
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests-e2e',
  fullyParallel: true,
  retries: 1,
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
  },
});
```

## Flujo de trabajo

### 1. Pruebas de regresion
Escribir pruebas para bugs existentes antes de modificarlos (Prove-It pattern):
```typescript
test('reproduce bug #123: error al enviar formulario vacio', async ({ page }) => {
  await page.goto('/formulario');
  await page.click('button[type="submit"]');
  await expect(page.locator('.error')).toBeVisible();
});
```

### 2. Pruebas de flujos criticos
Identificar los 3-5 flujos mas importantes y cubrirlos primero.

### 3. Pruebas de API (integracion)
Si el proyecto expone API:
```typescript
test('GET /api/recurso responde 200', async ({ request }) => {
  const res = await request.get('/api/recurso');
  expect(res.status()).toBe(200);
});
```

## Reglas
1. No cambiar configuracion de pruebas existente.
2. No duplicar cobertura: si ya hay prueba unitaria, no hacer E2E de lo mismo.
3. Usar `tests-e2e/` como directorio para no mezclar con pruebas existentes.
4. Priorizar flujos criticos y bugs activos.
5. Cada prueba de regresion debe referenciar el issue o bug que reproduce.
6. Los nombres en espanol, salvo tecnicismos inevitables.

## Salidas
- `tests-e2e/` con pruebas nuevas o ampliadas.
- Reporte de brechas de cobertura.
- Pruebas de regresion para bugs activos.

## Integracion con el ecosistema
- `testing.md` - Skill base de testing local.
- `agente-skills/skills/test-driven-development/SKILL.md` - TDD.
- `agente-skills/skills/browser-testing-with-devtools/SKILL.md` - DevTools MCP.
