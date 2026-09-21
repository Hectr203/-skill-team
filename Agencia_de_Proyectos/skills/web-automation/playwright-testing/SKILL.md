---
name: playwright-testing
description: Use for browser E2E and visual/accessibility checks with Antigravity browser first and Playwright MCP only as approved fallback.
---
# Browser testing
Prefer Antigravity integrated browser. If another environment and approval exists, configure the official `@playwright/mcp@latest`; it uses accessibility snapshots and is not a security boundary. Reuse the existing test framework, cover critical flows, isolate test data and never use production accounts. This session does not activate it.
