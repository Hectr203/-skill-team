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
        # La última sesión en la ventana debe ser la #7
        self.assertIn("Tarea completada #7", parsed["sesiones_recientes"][-1])
        # Deben haber 3 hitos compactados en la bitácora anterior (inicialización + tarea 1 + tarea 2)
        self.assertEqual(len(parsed["hitos_anteriores"]), 3)
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
        self.assertNotIn("Hitos Anteriores", enfocada)

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
            ejecutar_cierre(args, raiz_agencia=self.tmp_dir)

        contenido = (self.proyecto_dir / "memoria.md").read_text(encoding="utf-8")
        parsed = analizar_memoria(contenido)
        self.assertEqual(len(parsed["sesiones_recientes"]), 5)
        self.assertEqual(len(parsed["hitos_anteriores"]), 2)

if __name__ == "__main__":
    unittest.main()
