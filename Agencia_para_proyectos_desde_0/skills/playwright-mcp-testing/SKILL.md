---
name: playwright-mcp-testing
description: QA y testing con Playwright MCP para proyectos nuevos. Usar para escribir y ejecutar pruebas E2E, de integracion y unitarias usando Playwright y el protocolo MCP. Incluye configuracion, reporteria y CI.
---

# Playwright MCP Testing

## Proposito
Integrar Playwright como framework de testing E2E y de integracion en proyectos nuevos, usando el ecosistema MCP para orquestacion automatica de navegadores. Esta skill garantiza que el proyecto tenga pruebas reales desde el dia uno, sin configuracion manual repetitiva.

## Prerequisitos
- Proyecto Node.js 22 LTS con TypeScript.
- Playwright instalado (`npm init playwright@latest` o `npm install -D @playwright/test`).
- Playwright MCP server configurado (ver abajo).

## Configuracion de Playwright MCP

### 1. Instalar dependencias
```bash
npm install -D @playwright/test
npx playwright install --with-deps chromium
```

### 2. Configurar playwright.config.ts
```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [['html'], ['list']],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
  ],
});
```

### 3. Integracion MCP para agentes
Los agentes usan Playwright MCP server para ejecutar pruebas en navegadores reales. El MCP server expone herramientas para:
- `browser_navigate` - Navegar a URLs
- `browser_click` - Hacer clic en elementos
- `browser_snapshot` - Capturar estado accesible del DOM
- `browser_take_screenshot` - Capturar pantallazos
- `browser_type` - Escribir en campos
- `browser_evaluate` - Ejecutar JavaScript en pagina

## Flujo de trabajo

### Fase 1 - Analisis
1. Identificar flujos criticos del modulo.
2. Definir que probar: unitario, integracion o E2E.
3. Revisar contratos API, DTOs y tipos.

### Fase 2 - Pruebas unitarias
```typescript
// tests/unitarios/nombre-modulo.test.ts
import { describe, it, expect } from '@playwright/test';

describe('NombreModulo', () => {
  it('debe procesar entrada valida correctamente', () => {
    const resultado = funcionAProbar(entradaValida);
    expect(resultado).toEqual(esperado);
  });

  it('debe rechazar entrada invalida con error', () => {
    expect(() => funcionAProbar(entradaInvalida)).toThrow('mensaje de error');
  });
});
```

### Fase 3 - Pruebas de integracion
```typescript
// tests/integracion/api-nombre-modulo.test.ts
import { test, expect } from '@playwright/test';

test('POST /api/modulo debe crear recurso', async ({ request }) => {
  const respuesta = await request.post('/api/modulo', {
    data: { /* datos */ }
  });
  expect(respuesta.ok()).toBeTruthy();
  expect(await respuesta.json()).toMatchObject({
    ok: true
  });
});
```

### Fase 4 - Pruebas E2E con Playwright MCP
```typescript
// tests/e2e/flujo-critico.test.ts
import { test, expect } from '@playwright/test';

test('flujo completo de usuario', async ({ page }) => {
  await page.goto('/');
  await page.click('text=Iniciar Sesion');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  await expect(page.locator('text=Dashboard')).toBeVisible();
});
```

### Fase 5 - Reporteria y CI
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: npm test
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

## Reglas
1. No mezclar niveles de prueba en un mismo archivo.
2. Cada prueba debe verificar UN concepto.
3. Usar describe/it para estructura BDD.
4. Pruebas E2E solo para flujos criticos de usuario.
5. Mockear solo fronteras del sistema (API externa, base de datos).
6. No usar snapshot tests como unica validacion.
7. Etiquetar pruebas lentas con `test.slow()`.
8. Los nombres de prueba deben describir comportamiento en espanol.

## Salidas
- `tests/` con estructura: `unitarios/`, `integracion/`, `e2e/`.
- `playwright-report/` con reporte HTML.
- CI configurado para ejecutar pruebas en cada push.

## Referencias
- `agente-skills/skills/test-driven-development/SKILL.md` para TDD classico.
- `agente-skills/skills/browser-testing-with-devtools/SKILL.md` para debugging visual.
- `agente-skills/references/testing-patterns.md` para patrones de pruebas.
