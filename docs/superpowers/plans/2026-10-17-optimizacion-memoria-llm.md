# Plan de Implementación: Optimización Jerárquica y Ventana Deslizante de Memoria para LLMs

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reducir entre 70% y 85% el consumo de tokens y evitar la degradación de contexto ("lost in the middle") en los LLMs mediante memoria jerárquica con ventana deslizante y compactación progresiva en `Agencia_Principal`.

**Architecture:** Se divide la memoria Markdown de cada proyecto en 4 zonas (Estado Activo, ADRs vigentes, Ventana Deslizante de últimas 5 sesiones y Bitácora Compactada de hitos pasados). El Context Engine (`arranque.py --prime`) inyecta solo las zonas activas y recientes, manteniendo el 100% de los datos inmutables en `.memoria/timeline.jsonl`.

**Tech Stack:** Python 3.12 (standard library: `re`, `pathlib`, `json`, `datetime`, `fcntl`, `tempfile`), unittest.

---

### Task 1: Parsing y rotación de ventana deslizante en `memoria_proyecto.py`

**Files:**
- Create: `/mnt/nvme/skill-team/Agencia_Principal/tests/test_memoria_optimizada.py`
- Modify: `/mnt/nvme/skill-team/Agencia_Principal/scripts/memoria_proyecto.py`

- [ ] **Step 1: Escribir el test fallido para análisis y rotación de memoria**

Crear el archivo `/mnt/nvme/skill-team/Agencia_Principal/tests/test_memoria_optimizada.py`:

```python
import json
import shutil
import tempfile
import unittest
from pathlib import Path
import sys

# Agregar scripts al path
AGENCIA_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = AGENCIA_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from memoria_proyecto import (
    inicializar,
    guardar_mem_palace,
    analizar_memoria,
    rotar_memoria,
    leer_memoria_enfocada,
    informe,
)

class TestMemoriaOptimizada(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())
        self.proyecto_dir = self.tmp_dir / "contexts" / "projects" / "proyecto-test"
        inicializar(self.proyecto_dir)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_rotacion_ventana_deslizante(self):
        """Al registrar más de 5 sesiones, las más antiguas deben compactarse en hitos de 1 línea."""
        for i in range(1, 8):
            bloque = informe(
                tareas=f"Tarea completada #{i}",
                pendientes=f"Pendiente #{i}",
                decisiones=f"Decision #{i}",
                riesgos="Ninguno",
                agente="Backend",
                archivos=[f"archivo_{i}.py"],
            )
            guardar_mem_palace(self.proyecto_dir, bloque, acumular=True)
            rotar_memoria(self.proyecto_dir, max_sesiones=5)

        contenido = (self.proyecto_dir / "memoria.md").read_text(encoding="utf-8")
        parsed = analizar_memoria(contenido)
        
        # Deben quedar exactamente 5 sesiones detalladas en la ventana
        self.assertEqual(len(parsed["sesiones_recientes"]), 5)
        # La primera sesión en la ventana debe ser la #3 o posterior
        self.assertIn("Tarea completada #7", parsed["sesiones_recientes"][-1])
        # Deben haber 2 hitos compactados en la bitácora anterior
        self.assertEqual(len(parsed["hitos_anteriores"]), 2)
        self.assertTrue(any("Tarea completada #1" in hito for hito in parsed["hitos_anteriores"]))
        self.assertTrue(any("Tarea completada #2" in hito for hito in parsed["hitos_anteriores"]))

    def test_lectura_memoria_enfocada(self):
        """leer_memoria_enfocada solo debe devolver estado activo y sesiones recientes, omitiendo hitos históricos."""
        for i in range(1, 8):
            bloque = informe(
                tareas=f"Tarea #{i}",
                agente="Backend",
            )
            guardar_mem_palace(self.proyecto_dir, bloque, acumular=True)
            rotar_memoria(self.proyecto_dir, max_sesiones=5)

        enfocada = leer_memoria_enfocada(self.proyecto_dir)
        self.assertIn("Tarea #7", enfocada)
        self.assertIn("Tarea #3", enfocada)
        # Tarea #1 y #2 están compactadas en el archivo pero no deben estar en la memoria enfocada
        self.assertNotIn("### [", enfocada.split("Tarea #1")[0] if "Tarea #1" in enfocada else "")
        self.assertNotIn("Hitos Anteriores", enfocada)

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Ejecutar test para verificar que falla**

Ejecutar:
```bash
python3 -m unittest Agencia_Principal/tests/test_memoria_optimizada.py
```
Resultado esperado: `FAIL` o `ImportError` indicando que `analizar_memoria`, `rotar_memoria`, o `leer_memoria_enfocada` no existen.

- [ ] **Step 3: Implementar `analizar_memoria`, `rotar_memoria` y `leer_memoria_enfocada` en `memoria_proyecto.py`**

Modificar `/mnt/nvme/skill-team/Agencia_Principal/scripts/memoria_proyecto.py`:
- Implementar la función `analizar_memoria(contenido: str) -> dict` para parsear cabecera, estado activo, ADRs, sesiones detalladas (`### [...] Sesión`) e hitos compactados.
- Implementar la función `rotar_memoria(proyecto: Path, max_sesiones: int = 5) -> None` que compacta sesiones que excedan el límite a hitos sintéticos (`- [YYYY-MM-DD] (<Agente>) <Tareas> (<N> archivos)`).
- Implementar `leer_memoria_enfocada(proyecto: Path) -> str` que compone la vista optimizada para el prompt LLM.

- [ ] **Step 4: Ejecutar test para verificar que pasa**

Ejecutar:
```bash
python3 -m unittest Agencia_Principal/tests/test_memoria_optimizada.py
```
Resultado esperado: `Ran 2 tests ... OK`.

- [ ] **Step 5: Commit de la Tarea 1**

```bash
git add Agencia_Principal/scripts/memoria_proyecto.py Agencia_Principal/tests/test_memoria_optimizada.py
git commit -m "feat(memoria): implementar parsing y rotacion con ventana deslizante"
```

---

### Task 2: Extracción enfocada y soporte `--completo` en `arranque.py`

**Files:**
- Modify: `/mnt/nvme/skill-team/Agencia_Principal/scripts/arranque.py`
- Modify: `/mnt/nvme/skill-team/Agencia_Principal/scripts/agencia.py`
- Test: `/mnt/nvme/skill-team/Agencia_Principal/tests/test_memoria_optimizada.py`

- [ ] **Step 1: Escribir test fallido para `--prime` enfocado vs `--completo`**

Agregar a `/mnt/nvme/skill-team/Agencia_Principal/tests/test_memoria_optimizada.py`:

```python
    def test_primer_prompt_ahorro_tokens(self):
        """El primer prompt debe incluir métrica de tokens y ahorro."""
        from arranque import obtener_paquete_contexto, generar_primer_prompt
        for i in range(1, 8):
            bloque = informe(
                tareas=f"Implementar funcionalidad grande con mucho texto y detalles de código #{i}",
                pendientes=f"Control de calidad #{i}",
                agente="Fullstack",
            )
            guardar_mem_palace(self.proyecto_dir, bloque, acumular=True)
            rotar_memoria(self.proyecto_dir, max_sesiones=3)

        ctx_enfocado = obtener_paquete_contexto(self.proyecto_dir, modo_completo=False)
        prompt_enfocado = generar_primer_prompt(ctx_enfocado)
        
        ctx_completo = obtener_paquete_contexto(self.proyecto_dir, modo_completo=True)
        prompt_completo = generar_primer_prompt(ctx_completo)

        # El prompt enfocado debe ser notablemente más corto que el completo
        self.assertLess(len(prompt_enfocado), len(prompt_completo))
        self.assertIn("Ahorro estimado:", prompt_enfocado)
        self.assertIn("Hitos Anteriores", prompt_completo)
```

- [ ] **Step 2: Ejecutar test para verificar que falla**

Ejecutar:
```bash
python3 -m unittest Agencia_Principal/tests/test_memoria_optimizada.py
```
Resultado esperado: `FAIL` con error de argumentos en `obtener_paquete_contexto(..., modo_completo=...)`.

- [ ] **Step 3: Implementar soporte `--completo` y cálculo FinOps en `arranque.py` y `agencia.py`**

Modificar `/mnt/nvme/skill-team/Agencia_Principal/scripts/arranque.py`:
- Actualizar `obtener_paquete_contexto(ruta_proyecto: Path, modo_completo: bool = False) -> dict`:
  - Si `modo_completo=False`, usa `leer_memoria_enfocada`.
  - Calcula `tokens_estimados_prompt` y `tokens_estimados_disco`, junto al porcentaje de ahorro:
    `ahorro_pct = round((1 - tokens_prompt / tokens_disco) * 100)` si `tokens_disco > tokens_prompt`.
- Actualizar `generar_primer_prompt(ctx: dict)` para mostrar el porcentaje de ahorro y no inyectar ruido histórico.
- Actualizar argumentos CLI en `arranque.py` y `agencia.py` agregando `--completo`.

- [ ] **Step 4: Ejecutar test para verificar que pasa**

Ejecutar:
```bash
python3 -m unittest Agencia_Principal/tests/test_memoria_optimizada.py
```
Resultado esperado: `Ran 3 tests ... OK`.

- [ ] **Step 5: Commit de la Tarea 2**

```bash
git add Agencia_Principal/scripts/arranque.py Agencia_Principal/scripts/agencia.py Agencia_Principal/tests/test_memoria_optimizada.py
git commit -m "feat(arranque): integrar extraccion enfocada con FinOps y flag --completo"
```

---

### Task 3: Integración automática de rotación en `cierre.py`

**Files:**
- Modify: `/mnt/nvme/skill-team/Agencia_Principal/scripts/cierre.py`
- Test: `/mnt/nvme/skill-team/Agencia_Principal/tests/test_memoria_optimizada.py`

- [ ] **Step 1: Escribir test fallido para rotación automática al ejecutar cierre**

Agregar a `/mnt/nvme/skill-team/Agencia_Principal/tests/test_memoria_optimizada.py`:

```python
    def test_cierre_ejecuta_rotacion_automatica(self):
        """cierre.py debe disparar rotar_memoria automáticamente tras guardar."""
        from cierre import ejecutar_cierre
        import argparse

        for i in range(1, 7):
            args = argparse.Namespace(
                proyecto=self.proyecto_dir.name,
                tareas=f"Cierre de tarea #{i}",
                archivos=f"mod_{i}.py",
                decisiones="",
                pendientes="",
                riesgos="",
                agente="Backend",
                cloud_resumen="",
                tipo="operativo",
                notificar=False,
            )
            # Pasamos raíz temporal para resolver el proyecto
            ejecutar_cierre(args, raiz_agencia=self.tmp_dir)

        contenido = (self.proyecto_dir / "memoria.md").read_text(encoding="utf-8")
        parsed = analizar_memoria(contenido)
        self.assertEqual(len(parsed["sesiones_recientes"]), 5)
        self.assertEqual(len(parsed["hitos_anteriores"]), 1)
```

- [ ] **Step 2: Ejecutar test para verificar que falla**

Ejecutar:
```bash
python3 -m unittest Agencia_Principal/tests/test_memoria_optimizada.py
```
Resultado esperado: `FAIL` porque `ejecutar_cierre` aún no compacta automáticamente a 5 sesiones.

- [ ] **Step 3: Implementar invocación de `rotar_memoria` en `cierre.py`**

Modificar `/mnt/nvme/skill-team/Agencia_Principal/scripts/cierre.py`:
- Tras escribir el bloque informe y registrar en `cloudmem`, invocar `rotar_memoria(ruta_proyecto, max_sesiones=5)`.
- Imprimir en el resumen del cierre si se compactaron sesiones históricas.

- [ ] **Step 4: Ejecutar test para verificar que pasa**

Ejecutar:
```bash
python3 -m unittest Agencia_Principal/tests/test_memoria_optimizada.py
```
Resultado esperado: `Ran 4 tests ... OK`.

- [ ] **Step 5: Commit de la Tarea 3**

```bash
git add Agencia_Principal/scripts/cierre.py Agencia_Principal/tests/test_memoria_optimizada.py
git commit -m "feat(cierre): compactar sesiones excedentes automaticamente al cerrar tarea"
```

---

### Task 4: Verificación Integral y Suite Completa de la Agencia

**Files:**
- Audit & Verify: Toda la suite de `Agencia_Principal`

- [ ] **Step 1: Ejecutar validador estructural de la agencia**

Ejecutar:
```bash
python3 scripts/agencia.py validar
```
Resultado esperado: Código 0, `VALIDACION OK`.

- [ ] **Step 2: Ejecutar la suite completa de tests de la agencia**

Ejecutar:
```bash
python3 -m unittest discover tests/
```
Resultado esperado: Todos los tests pasan (71 tests OK, incluidos los 4 nuevos).

- [ ] **Step 3: Ejecutar verificación y actualizar evidencia local**

Ejecutar:
```bash
python3 scripts/agencia.py verificar
python3 scripts/agencia.py comprobar
```
Resultado esperado: `VERIFICACIÓN LOCAL APROBADA` y `EVIDENCIA LOCAL VIGENTE`.

- [ ] **Step 4: Ejecutar diagnóstico general de la agencia**

Ejecutar:
```bash
python3 scripts/agencia.py doctor
```
Resultado esperado: 23/23 comprobaciones aprobadas.

- [ ] **Step 5: Commit de la verificación final**

```bash
git add Agencia_Principal/.agencia/verificacion-local.json
git commit -m "chore(verificacion): actualizar evidencia local con memoria optimizada"
```
