#!/usr/bin/env python3
"""
Pruebas exhaustivas para optimización de memoria de proyecto, ventana deslizante,
recuperación histórica, presupuesto FinOps y preservación de estado activo.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Asegurar que tanto 'scripts/' como la raíz de la agencia estén en sys.path
AGENCIA_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = AGENCIA_ROOT / "scripts"
for ruta in (str(SCRIPTS_DIR), str(AGENCIA_ROOT)):
    if ruta not in sys.path:
        sys.path.insert(0, ruta)

try:
    from scripts.memoria_proyecto import (
        _obtener_fernet_opcional,
        agregar_cloudmem,
        analizar_memoria,
        compactar_sesion_a_hito,
        consolidar_estado_activo,
        guardar_mem_palace,
        informe,
        inicializar,
        leer_cloudmem,
        leer_mem_palace,
        leer_memoria_enfocada,
        recuperar_historia,
        reconstruir_memoria,
        rotar_memoria,
        rutas_memoria,
    )
    from scripts.arranque import generar_primer_prompt, obtener_paquete_contexto
    from scripts.cierre import ejecutar_cierre
    import scripts.agencia_mcp as agencia_mcp
    from scripts.agencia_mcp import ejecutar_herramienta
except ImportError:
    from memoria_proyecto import (  # type: ignore
        _obtener_fernet_opcional,
        agregar_cloudmem,
        analizar_memoria,
        compactar_sesion_a_hito,
        consolidar_estado_activo,
        guardar_mem_palace,
        informe,
        inicializar,
        leer_cloudmem,
        leer_mem_palace,
        leer_memoria_enfocada,
        recuperar_historia,
        reconstruir_memoria,
        rotar_memoria,
        rutas_memoria,
    )
    from arranque import generar_primer_prompt, obtener_paquete_contexto  # type: ignore
    from cierre import ejecutar_cierre  # type: ignore
    import agencia_mcp  # type: ignore
    from agencia_mcp import ejecutar_herramienta  # type: ignore


class TestMemoriaOptimizada(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())
        self.proyecto_dir = self.tmp_dir / "contexts" / "projects" / "proyecto-test"
        inicializar(self.proyecto_dir)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_rotacion_ventana_deslizante_e_idempotencia(self):
        """Al registrar 7 cierres, quedan 5 recientes en detalle y 2 hitos compactados; repetir rotación no duplica."""
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

        # 5 detalladas en ventana reciente
        self.assertEqual(len(parsed["sesiones_recientes"]), 5)
        self.assertIn("Tarea completada #7", parsed["sesiones_recientes"][-1])
        self.assertIn("Tarea completada #3", parsed["sesiones_recientes"][0])

        # 3 hitos anteriores compactados (inicialización + tarea #1 + tarea #2)
        self.assertEqual(len(parsed["hitos_anteriores"]), 3)
        self.assertTrue(any("Tarea completada #1" in hito for hito in parsed["hitos_anteriores"]))
        self.assertTrue(any("Tarea completada #2" in hito for hito in parsed["hitos_anteriores"]))

        # Prueba de idempotencia: rotar 3 veces consecutivas no altera nada ni duplica hitos
        rotar_memoria(self.proyecto_dir, max_sesiones=5)
        rotar_memoria(self.proyecto_dir, max_sesiones=5)
        contenido_despues = (self.proyecto_dir / "memoria.md").read_text(encoding="utf-8")
        parsed_despues = analizar_memoria(contenido_despues)
        self.assertEqual(len(parsed_despues["sesiones_recientes"]), 5)
        self.assertEqual(len(parsed_despues["hitos_anteriores"]), 3)
        self.assertEqual(contenido, contenido_despues)

    def test_conservacion_pendientes_y_decisiones_antiguas(self):
        """Los pendientes y decisiones de sesiones compactadas deben mantenerse en el Estado Activo y ADRs."""
        # Sesión 1 agrega un pendiente crítico y una decisión arquitectónica
        b1 = informe(
            tareas="Definir arquitectura de pagos",
            pendientes="Migrar certificados bancarios a HSM",
            decisiones="ADR-009: Usar mTLS en API de pagos",
            agente="Arquitecto",
        )
        guardar_mem_palace(self.proyecto_dir, b1, acumular=True)
        rotar_memoria(self.proyecto_dir, max_sesiones=5)

        # Agregamos 6 sesiones más para que la sesión 1 salga de la ventana de 5
        for i in range(2, 8):
            b = informe(
                tareas=f"Paso operativo #{i}",
                pendientes=f"Pendiente rutinario #{i}",
                decisiones="",
                agente="Backend",
            )
            guardar_mem_palace(self.proyecto_dir, b, acumular=True)
            rotar_memoria(self.proyecto_dir, max_sesiones=5)

        enfocada = leer_memoria_enfocada(self.proyecto_dir)
        parsed_enf = analizar_memoria(enfocada)
        # La tarea 1 ya no está como sesión reciente
        self.assertFalse(any("Definir arquitectura de pagos" in s for s in parsed_enf["sesiones_recientes"]))
        # Pero el pendiente crítico y la decisión de la sesión 1 siguen presentes en el Estado Activo / Decisiones
        self.assertIn("Migrar certificados bancarios a HSM", enfocada)
        self.assertIn("ADR-009", enfocada)

    def test_recuperabilidad_historial_completo_timeline(self):
        """Todo el detalle de sesiones compactadas debe existir en timeline.jsonl y ser recuperable."""
        for i in range(1, 8):
            agregar_cloudmem(
                proyecto=self.proyecto_dir,
                resumen=f"Refactor de seguridad #{i}",
                archivos=[f"seguridad_{i}.py"],
                decisiones=f"Decisión criptográfica #{i}",
                pendientes=f"Revisión #{i}",
                agente="SecOps",
            )
        
        # Recuperar por query
        resultados = recuperar_historia(self.proyecto_dir, query="Refactor de seguridad #1")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0]["agente"], "SecOps")
        self.assertIn("seguridad_1.py", resultados[0]["archivos"])
        self.assertEqual(resultados[0]["decisiones"], "Decisión criptográfica #1")

    def test_backfill_seguridad_antes_de_compactar(self):
        """Si memoria.md contiene sesiones no registradas en timeline, rotar_memoria las archiva antes de compactar."""
        rutas = rutas_memoria(self.proyecto_dir)
        # Escribir memoria antigua con 6 sesiones sin entradas en timeline.jsonl
        texto_antiguo = """# Memoria del Proyecto: proyecto-test
- **ID de Proyecto:** `proyecto-test`
- **Estado general:** Activo

## 1. Estado Activo
- **Objetivo actual:** Piloto legacy

## 2. Decisiones Técnicas
- Ninguna

## 3. Historial de Sesiones
"""
        for i in range(1, 7):
            texto_antiguo += f"""
### [2026-10-0{i}T10:00:00+00:00] Tarea Legacy #{i}
- **Agente:** LegacyDev
- **Tareas completadas:** Trabajo antiguo detallado #{i}
- **Archivos afectados:** `viejo_{i}.py`
- **Decisiones técnicas:** Decisión #{i}
- **Pendientes:** Pendiente #{i}
- **Riesgos:** Ninguno
"""
        rutas["memoria_md"].write_text(texto_antiguo, encoding="utf-8")
        # Asegurar timeline vacío
        rutas["timeline"].write_text("", encoding="utf-8")

        # Ejecutar rotación a 5
        rotar_memoria(self.proyecto_dir, max_sesiones=5)

        # Comprobar que la sesión #1 compactada fue respaldada en timeline.jsonl y NO se perdió
        historial = leer_cloudmem(self.proyecto_dir, limite=10)
        self.assertTrue(any("Trabajo antiguo detallado #1" in h.get("resumen", "") or "Trabajo antiguo detallado #1" in str(h) for h in historial))

    def test_parser_ignora_encabezados_dentro_de_bloques_de_codigo(self):
        """El parser no debe confundirse con encabezados dentro de bloques de código Markdown."""
        texto = """# Memoria del Proyecto: proyecto-test

## 1. Estado Activo
- **Objetivo actual:** Test parser

## 2. Decisiones Técnicas
- Ninguna

## 3. Historial Reciente

### [2026-10-17T12:00:00+00:00] Sesión Real #1
- **Agente:** Backend
- **Tareas completadas:** Código con snippets:
```markdown
### [2026-10-17T00:00:00+00:00] Falso encabezado en código
- Esto no es una sesión
## 4. Hitos falsos
```
- **Archivos afectados:** `test.py`
"""
        parsed = analizar_memoria(texto)
        self.assertEqual(len(parsed["sesiones_recientes"]), 1)
        self.assertIn("Falso encabezado en código", parsed["sesiones_recientes"][0])
        self.assertEqual(len(parsed["hitos_anteriores"]), 0)

    def test_presupuesto_contexto_y_recorte_secundario(self):
        """Si las sesiones recientes exceden el presupuesto, se comprime detalle secundario sin perder identificadores."""
        # Crear 5 sesiones extensas (~1,500 caracteres cada una)
        for i in range(1, 6):
            detalle_extenso = f"Detalle de tarea tecnica de backend con logs y trazas #{i}: " + ("x" * 1500)
            bloque = informe(
                tareas=f"Tarea #{i}: {detalle_extenso}",
                agente="Dev",
            )
            guardar_mem_palace(self.proyecto_dir, bloque, acumular=True)
            rotar_memoria(self.proyecto_dir, max_sesiones=5)

        # Con presupuesto ajustado (ej: 800 tokens ~ 3,000 caracteres), debe comprimir las sesiones antiguas
        enfocada = leer_memoria_enfocada(self.proyecto_dir, presupuesto_tokens=800)
        # La última sesión (#5) se conserva completa con su detalle
        self.assertIn("Tarea #5", enfocada)
        self.assertIn("x" * 1000, enfocada)
        # Las sesiones más antiguas (#1 a #4) fueron comprimidas a resúmenes con referencia timeline
        self.assertIn("timeline#", enfocada)
        # El total de la memoria enfocada debe haberse reducido sustancialmente respecto a la memoria sin comprimir
        memoria_completa = leer_mem_palace(self.proyecto_dir)
        self.assertLess(len(enfocada), len(memoria_completa) * 0.6)

    def test_tolerancia_timeline_corrupto(self):
        """Líneas corruptas en timeline no rompen la lectura ni la recuperación de líneas válidas."""
        rutas = rutas_memoria(self.proyecto_dir)
        linea_valida_1 = json.dumps({"fecha": "2026-10-17T01:00:00Z", "resumen": "Ok 1", "agente": "A"})
        linea_corrupta = '{"fecha": "2026-10-17", resumen: INCOMPLETO...'
        linea_valida_2 = json.dumps({"fecha": "2026-10-17T02:00:00Z", "resumen": "Ok 2", "agente": "B"})
        rutas["timeline"].write_text(f"{linea_valida_1}\n{linea_corrupta}\n{linea_valida_2}\n", encoding="utf-8")

        entradas = leer_cloudmem(self.proyecto_dir, limite=10)
        self.assertEqual(len(entradas), 2)
        self.assertEqual(entradas[0]["resumen"], "Ok 1")
        self.assertEqual(entradas[1]["resumen"], "Ok 2")

    def test_arranque_primer_prompt_finops_honesto(self):
        """El arranque debe comparar contextos equivalentes y reportar ahorro honesto y modo --completo."""
        for i in range(1, 8):
            bloque = informe(
                tareas=f"Implementar módulo financiero crítico y reglas contables detalladas #{i}: " + ("código y validaciones " * 30),
                pendientes=f"Control de calidad y auditoría #{i}",
                decisiones=f"ADR-10{i}: Política de redondeo y precisión #{i}",
                agente="Fullstack",
                archivos=[f"finanzas_{i}.py", f"test_finanzas_{i}.py"],
            )
            guardar_mem_palace(self.proyecto_dir, bloque, acumular=True)
            rotar_memoria(self.proyecto_dir, max_sesiones=3)

        ctx_enfocado = obtener_paquete_contexto(self.proyecto_dir, modo_completo=False)
        prompt_enfocado = generar_primer_prompt(ctx_enfocado)

        ctx_completo = obtener_paquete_contexto(self.proyecto_dir, modo_completo=True)
        prompt_completo = generar_primer_prompt(ctx_completo)

        # 1. El prompt enfocado debe ser sustancialmente menor que el completo
        self.assertLess(len(prompt_enfocado), len(prompt_completo))
        # 2. Las métricas FinOps deben ser honestas (comparar prompt enfocado vs referencia)
        finops = ctx_enfocado["finops"]
        self.assertGreater(finops["tokens_referencia"], finops["tokens_enfocado"])
        self.assertGreater(finops["ahorro_porcentaje"], 0.0)
        self.assertEqual(finops["modo"], "enfocado")
        self.assertIn("estimacion", finops["metodo_conteo"])
        # 3. El prompt enfocado debe indicar el ahorro y la referencia histórica
        self.assertIn("Métrica FinOps (enfocado)", prompt_enfocado)
        self.assertIn("Recuperación Histórica", prompt_enfocado)
        # 4. El prompt completo debe incluir la bitácora histórica de hitos
        self.assertIn("Hitos Anteriores", prompt_completo)
        # 5. El almacenamiento en disco se reporta por separado
        self.assertIn("almacenamiento_disco", finops)


    def test_cierre_ejecuta_rotacion_y_transaccion_segura(self):
        """cierre.py debe disparar rotación automática, registrar en timeline y resolver pendientes explícitos."""
        # Cierre 1 genera un pendiente específico
        args1 = argparse.Namespace(
            proyecto=self.proyecto_dir.name,
            tareas="Cierre de tarea inicial #1",
            archivos="mod_1.py",
            decisiones="ADR-201: Esquema de base de datos",
            pendientes="Configurar índices en Postgres",
            riesgos="",
            agente="Backend",
            cloud_resumen="",
            tipo="operativo",
            notificar=False,
            resolver_pendientes="",
        )
        ejecutar_cierre(args1, raiz_agencia=self.tmp_dir)

        # Cierres 2 a 7
        for i in range(2, 8):
            # En el cierre 4 resolvemos explícitamente el pendiente de Postgres
            resueltos = "Configurar índices en Postgres" if i == 4 else ""
            args = argparse.Namespace(
                proyecto=self.proyecto_dir.name,
                tareas=f"Cierre de tarea #{i}",
                archivos=f"mod_{i}.py",
                decisiones="",
                pendientes=f"Pendiente de tarea #{i}",
                riesgos="",
                agente="Backend",
                cloud_resumen="",
                tipo="operativo",
                notificar=False,
                resolver_pendientes=resueltos,
            )
            ejecutar_cierre(args, raiz_agencia=self.tmp_dir)

        contenido = (self.proyecto_dir / "memoria.md").read_text(encoding="utf-8")
        parsed = analizar_memoria(contenido)

        # Ventana deslizante respetada a 5 sesiones
        self.assertEqual(len(parsed["sesiones_recientes"]), 5)
        # Hitos anteriores compactados correctamente
        self.assertGreater(len(parsed["hitos_anteriores"]), 0)
        # Decisión ADR-201 preservada en sección 2
        self.assertIn("ADR-201", parsed["decisiones"])
        # El pendiente resuelto ya no aparece como pendiente abierto en la sección 1
        self.assertNotIn("- [ ] Configurar índices en Postgres", parsed["estado_activo"])

    def test_reconstruccion_memoria_desde_timeline(self):
        """reconstruir_memoria debe recuperar estado activo, decisiones y sesiones recientes a partir de timeline."""
        # Eliminar memoria.md y registrar 2 eventos en timeline
        rutas = rutas_memoria(self.proyecto_dir)
        rutas["memoria_md"].unlink()
        
        agregar_cloudmem(self.proyecto_dir, "Evento 1", ["a.py"], decisiones="ADR-301: JWT", pendientes="Hacer pruebas")
        agregar_cloudmem(self.proyecto_dir, "Evento 2", ["b.py"], decisiones="ADR-302: Redis", pendientes="Configurar cache")
        
        texto_reconstruido = reconstruir_memoria(self.proyecto_dir, reparar_archivo=True)
        self.assertTrue(rutas["memoria_md"].exists())
        self.assertIn("ADR-301", texto_reconstruido)
        self.assertIn("ADR-302", texto_reconstruido)
        self.assertIn("Hacer pruebas", texto_reconstruido)
        self.assertIn("Configurar cache", texto_reconstruido)

    def test_compatibilidad_fernet_cifrado(self):
        """El soporte opcional de Fernet debe mantenerse sincronizado."""
        rutas = rutas_memoria(self.proyecto_dir)
        fernet = _obtener_fernet_opcional(rutas, crear=True)
        if fernet:
            bloque = informe(tareas="Tarea segura con cifrado", agente="SecOps")
            guardar_mem_palace(self.proyecto_dir, bloque, acumular=True)
            self.assertTrue(rutas["mem_palace"].exists())
            desencriptado = fernet.decrypt(rutas["mem_palace"].read_bytes()).decode("utf-8")
            self.assertIn("Tarea segura con cifrado", desencriptado)

    def test_mcp_arranque_cierre_historia(self):
        """Las herramientas MCP agencia_arranque, agencia_cierre y agencia_historia deben responder limpiamente."""
        with patch.object(agencia_mcp, "RAIZ", self.tmp_dir):
            # 1. Cierre vía MCP en proyecto aislado de pruebas
            res_cierre, err = ejecutar_herramienta("agencia_cierre", {
                "proyecto": "proyecto-test",
                "tareas": "Prueba de cierre vía MCP",
                "agente": "MCP Tester",
            })
            self.assertFalse(err)
            self.assertIn("Cierre registrado con éxito", res_cierre)
            
            # 2. Arranque modo primer vía MCP
            res_arranque, err = ejecutar_herramienta("agencia_arranque", {
                "proyecto": "proyecto-test",
                "formato": "primer",
            })
            self.assertFalse(err)
            self.assertIn("CONTEXTO DEL PROYECTO: proyecto-test", res_arranque)
            self.assertIn("Métrica FinOps (enfocado)", res_arranque)

            # 3. Arranque modo completo vía MCP
            res_arranque_comp, err = ejecutar_herramienta("agencia_arranque", {
                "proyecto": "proyecto-test",
                "formato": "primer",
                "completo": True,
            })
            self.assertFalse(err)
            self.assertIn("Métrica FinOps (completo)", res_arranque_comp)

            # 4. Historia vía MCP
            res_hist, err = ejecutar_herramienta("agencia_historia", {
                "proyecto": "proyecto-test",
                "query": "MCP Tester",
            })
            self.assertFalse(err)
            data = json.loads(res_hist)
            self.assertTrue(len(data) >= 1)
            self.assertEqual(data[-1]["agente"], "MCP Tester")


if __name__ == "__main__":
    unittest.main()
