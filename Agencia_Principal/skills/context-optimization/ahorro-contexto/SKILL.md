---
name: ahorro-contexto
description: Suite integral de optimización extrema de contexto y ahorro de tokens. Combina Graphify, claude-mem, Headroom y protocolos de exclusión para evitar la saturación de la ventana de contexto.
---

# Suite de Optimización de Contexto y Reducción de Tokens

Esta skill formaliza la estrategia integral de la Agencia de Proyectos para minimizar el consumo de tokens en modelos de lenguaje sin perder precisión técnica ni contexto histórico.

---

## 1. La Suite de 3 Capas Complementarias

Para lograr un ahorro de hasta el 85% de tokens en flujos de desarrollo complejos, la agencia orquesta tres herramientas complementarias:

| Herramienta | Función Principal | Cuándo se Invoca | Impacto en Tokens |
|---|---|---|---|
| **`claude-mem`** | Memoria persistente universal multicapa (SQLite + vectores) | **Inicio y cierre** de cada sesión o tarea | Evita inyectar historiales conversacionales y transcripciones pesadas |
| **`Graphify`** | Navegación topológica por grafo de dependencias de código | **Antes de explorar** o responder preguntas estructurales | Elimina lecturas masivas de código y búsquedas globales a ciegas |
| **`Headroom`** | Compresión semántica en tiempo real (MCP / wrapper) | Al ejecutar **tests, builds, logs masivos y git diffs** | Comprime hasta un 80% de salidas verbose reteniendo errores y stack traces |

---

## 2. Reglas de Exclusión Estricta de Rutas Ruidosas

Nunca leer, indexar ni volcar en prompts las siguientes rutas salvo requerimiento explícito del usuario:

- Dependencias: `node_modules/`, `vendor/`, `.pnpm-store/`
- Compilación y artefactos: `dist/`, `build/`, `out/`, `target/`, `.next/`, `.nuxt/`
- Cachés y entornos: `.git/`, `.cache/`, `tmp/`, `coverage/`, `.turbo/`
- Logs y bloqueos: `*.log`, `*.lock`, `package-lock.json`, `pnpm-lock.yaml`, `composer.lock`

---

## 3. Protocolo de Trabajo Minimalista (Ponytail Context)

1. **Comprensión**: Identificar la necesidad específica del usuario.
2. **Consulta a Memoria**: Recuperar acuerdos y estado previo desde `claude-mem` o `contexts/projects/<id>/memoria.md`.
3. **Consulta al Grafo**: Usar `graphify query` para identificar exclusivamente los 2-3 archivos o símbolos relevantes.
4. **Lectura Quirúrgica**: Leer únicamente los bloques o funciones afectadas utilizando rangos de líneas (`file:///path#L20-L60`), nunca archivos enteros.
5. **Compresión de Salidas**: Si se ejecutan suites de pruebas o linters masivos, utilizar `headroom` o filtrar las líneas de error.
6. **Resumen y Cierre**: Generar respuestas concisas y actualizar la memoria del proyecto con `scripts/cierre.py`.

---

## 4. Scripts Locales de Memoria por Proyecto

- **Arranque de Sesión**:
  ```bash
  python3 scripts/arranque.py --proyecto contexts/projects/<project-id>
  ```
- **Cierre de Tarea**:
  ```bash
  python3 scripts/cierre.py \
    --proyecto contexts/projects/<project-id> \
    --tareas "Implementado endpoint de almacenes con DTO Zod" \
    --decisiones "Transacción atómica en traspasos" \
    --archivos "backend/src/modules/almacen/traspasos.service.ts"
  ```
