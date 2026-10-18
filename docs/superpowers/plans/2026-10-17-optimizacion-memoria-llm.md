# Plan de Implementación: Optimización Jerárquica y Gestión de Memoria para LLMs

> **Guía de Ejecución:** Tareas verificables e incrementales en `Agencia_Principal`. Cada tarea incluye pruebas específicas y verificación de retrocompatibilidad.

**Objetivo:** Reducir el contexto innecesario que reciben los LLMs, conservar la continuidad del trabajo y permitir recuperar información histórica relevante sin cargarla completa en cada arranque. Medir honestamente el ahorro (meta 70%-85%) sin comprometer decisiones vigentes ni pendientes abiertos.

**Ubicación Base:** `/mnt/nvme/PROYECTO GILBERTO/Agencia_Principal`

---

### Task 1: Parser Robusto, Consolidación de Estado Activo y Rotación Idempotente en `memoria_proyecto.py`

**Archivos:**
- Crear: `Agencia_Principal/tests/test_memoria_optimizada.py`
- Modificar: `Agencia_Principal/scripts/memoria_proyecto.py`

- [ ] **Step 1: Escribir suite de pruebas unitarias para análisis, consolidación y rotación segura**
  - Probar parsing de 4 secciones respetando bloques de código (evitar falsos positivos dentro de ```markdown).
  - Probar rotación idempotente (ejecutar 5 veces sin eventos nuevos no altera el contenido ni duplica hitos).
  - Probar preservación de pendientes abiertos y decisiones de sesiones antiguas (que no desaparezcan al compactar).
  - Probar backfill de seguridad: si un cierre antiguo en `memoria.md` no está en `timeline.jsonl`, archivarlo antes de compactar.

- [ ] **Step 2: Ejecutar test y verificar fallos iniciales (TDD Red)**
  ```bash
  python3 -m unittest Agencia_Principal/tests/test_memoria_optimizada.py
  ```

- [ ] **Step 3: Implementar en `memoria_proyecto.py`:**
  - `analizar_memoria(contenido: str) -> dict`: parser tolerante con estado activo, ADRs, sesiones e hitos.
  - `consolidar_estado_activo(sesiones: list[dict], estado_previo: dict, nuevos_pendientes: str, nuevas_decisiones: str, pendientes_resueltos: list[str]) -> dict`: preserva pendientes no resueltos y decisiones vigentes.
  - `compactar_sesion_a_hito(bloque_sesion: str, evento_id: str) -> str`: genera hito de 1 línea con referencia al evento.
  - `rotar_memoria(proyecto: Path, max_sesiones: int = 5, presupuesto_tokens: int | None = None) -> None`: compactación idempotente con respaldo previo en timeline.
  - `leer_memoria_enfocada(proyecto: Path, presupuesto_tokens: int = 4000) -> str`: selecciona secciones activas y ventana reciente respetando presupuesto.
  - `recuperar_historia(proyecto: Path, query: str = "", evento_id: str = "", archivo: str = "", limite: int = 10) -> list[dict]`: consulta específica de timeline.
  - `reconstruir_memoria(proyecto: Path, reparar_archivo: bool = False) -> str`: reconstruye `memoria.md` desde timeline preservando estado activo.

- [ ] **Step 4: Ejecutar test y confirmar éxito (TDD Green)**
  ```bash
  python3 -m unittest Agencia_Principal/tests/test_memoria_optimizada.py
  ```

---

### Task 2: Extracción Enfocada, Presupuesto y Métricas FinOps Honestas en `arranque.py`

**Archivos:**
- Modificar: `Agencia_Principal/scripts/arranque.py`
- Pruebas en: `Agencia_Principal/tests/test_memoria_optimizada.py`

- [ ] **Step 1: Escribir pruebas para `--prime` enfocado vs `--completo` y presupuesto de tokens**
  - Probar que `--prime` inyecta Estado Activo, ADRs y sesiones recientes, omitiendo la bitácora extensa.
  - Probar que `--completo` devuelve el historial íntegro.
  - Probar cálculo honesto de FinOps: comparación entre prompt enfocado y prompt de referencia completo.
  - Probar que ante sesiones muy extensas que superan el presupuesto, se comprime el detalle secundario sin mutilar requisitos ni identificadores.

- [ ] **Step 2: Ejecutar test y verificar fallos esperados**

- [ ] **Step 3: Implementar cambios en `arranque.py`:**
  - `obtener_paquete_contexto(ruta_proyecto: Path, modo_completo: bool = False, presupuesto_tokens: int = 4000) -> dict`.
  - Calcular métricas de FinOps reales: `tokens_prompt_enfocado`, `tokens_prompt_referencia`, `ahorro_pct`.
  - Generar primer prompt enfocado y documentar mecanismo de recuperación en el header.
  - Actualizar CLI con `--completo` y `--presupuesto`.

- [ ] **Step 4: Ejecutar test y confirmar éxito**

---

### Task 3: Cierre Transaccional y Seguro en `cierre.py`

**Archivos:**
- Modificar: `Agencia_Principal/scripts/cierre.py`
- Pruebas en: `Agencia_Principal/tests/test_memoria_optimizada.py`

- [ ] **Step 1: Escribir pruebas para cierre atómico y actualización de estado activo**
  - Probar que cada cierre genera un ID de evento único (`evento_id`).
  - Probar que se escribe en `timeline.jsonl` antes de publicar `memoria.md`.
  - Probar soporte para resolver pendientes explícitamente (`--resolver-pendientes`).
  - Probar que toda la operación ocurre bajo un único bloqueo para evitar condiciones de carrera.

- [ ] **Step 2: Ejecutar test y verificar fallos esperados**

- [ ] **Step 3: Implementar en `cierre.py`:**
  - Generación de `evento_id` determinista o UUID corto.
  - Bloqueo unificado `with bloqueo_proyecto(ruta_proyecto / ".memoria"):`.
  - Anexado durable a timeline, actualización de estado activo, rotación automática y reemplazo atómico de `memoria.md`.

- [ ] **Step 4: Ejecutar test y confirmar éxito**

---

### Task 4: Integración en CLI Central (`agencia.py`) y Servidor MCP (`agencia_mcp.py`)

**Archivos:**
- Modificar: `Agencia_Principal/scripts/agencia.py`
- Modificar: `Agencia_Principal/scripts/agencia_mcp.py`
- Pruebas en: `Agencia_Principal/tests/test_memoria_optimizada.py`

- [ ] **Step 1: Escribir pruebas para comandos CLI y herramientas MCP actualizadas**
  - Probar comando `agencia.py arranque <id> --completo`.
  - Probar comando `agencia.py historia <id> --query ...`.
  - Probar que las respuestas MCP de `agencia_arranque`, `agencia_cierre` y `agencia_estado` mantienen sus contratos JSON/texto sin contaminación.

- [ ] **Step 2: Implementar subcomandos en `agencia.py` y tools en `agencia_mcp.py`**

- [ ] **Step 3: Ejecutar suite de pruebas completa y validar integridad**
