# Validacion y escenarios

## Ejecutado localmente

`python3 scripts/validar_agencia.py` comprueba archivos obligatorios, JSON,
frontmatter de skills, enlaces Markdown locales, URLs inseguras, directorios
vacíos, ausencia de estados privados y que no se hayan modificado las agencias
fuente. Resultado actual: `VALIDACION OK` (63 skills con frontmatter YAML, 148 Markdown). No instala
paquetes, no conecta MCP, no usa navegador y no muta fuentes.

## Escenarios simulados

| Escenario | Flujo esperado | Resultado |
|---|---|---|
| React + Node + PostgreSQL nuevo | `proyecto-nuevo`, monorepo dividido, ADR, Graphify tras base | diseñado/documentado |
| Brownfield con stack propio | `proyecto-existente`, memoria + Graphify, conservar stack | diseñado/documentado |
| Corrección urgente | diagnóstico, reproducción, parche mínimo, regresión | diseñado/documentado |
| Diseño | Stitch opt-in, tokens, Atomic Design, contingencia local | diseñado/documentado |
| Integración externa | MCP desactivado, HITL, fallback y permisos | validado estáticamente |
| Auditoría y seguridad | improve + ledger + refutación + planes read-only | contratos documentados |
| Producción/SEO | observabilidad, SEO, CRM privado, growth con compuertas | diseñado/documentado |

No se marcan pruebas E2E ni MCP como ejecutadas porque el usuario pidió
continuar sin ellos.
