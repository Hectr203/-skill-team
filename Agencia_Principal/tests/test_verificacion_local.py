"""La evidencia se reutiliza solo mientras conserva contenido y comprobaciones."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import verificacion_local


class VerificacionLocalTests(unittest.TestCase):
    def preparar(self, raiz):
        (raiz / "scripts").mkdir()
        (raiz / "scripts/ejemplo.py").write_text("print('ejemplo')\n")

    def aprobado(self, raiz):
        with patch.object(verificacion_local.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "OK", "")):
            return verificacion_local.verificar(raiz)

    def test_evidencia_se_invalida_por_modificacion_alta_o_baja(self):
        for cambio in ("modificar", "agregar", "eliminar"):
            with self.subTest(cambio=cambio), tempfile.TemporaryDirectory() as temporal:
                raiz = Path(temporal)
                self.preparar(raiz)
                self.assertEqual(self.aprobado(raiz), 0)
                self.assertEqual(verificacion_local.comprobar(raiz), 0)
                archivo = raiz / "scripts/ejemplo.py"
                if cambio == "modificar": archivo.write_text("print('cambio')\n")
                elif cambio == "agregar": (raiz / "nuevo.md").write_text("nuevo")
                else: archivo.unlink()
                self.assertNotEqual(verificacion_local.comprobar(raiz), 0)

    def test_un_fallo_no_deja_evidencia_aprobada(self):
        with tempfile.TemporaryDirectory() as temporal:
            raiz = Path(temporal)
            self.preparar(raiz)
            with patch.object(verificacion_local.subprocess, "run", return_value=subprocess.CompletedProcess([], 1, "", "falló")):
                self.assertNotEqual(verificacion_local.verificar(raiz), 0)
            self.assertNotEqual(verificacion_local.comprobar(raiz), 0)

    def test_cambios_durante_las_pruebas_invalidan_el_resultado(self):
        with tempfile.TemporaryDirectory() as temporal:
            raiz = Path(temporal)
            self.preparar(raiz)
            def ejecutar(*args, **kwargs):
                (raiz / "scripts/ejemplo.py").write_text("cambio durante prueba")
                return subprocess.CompletedProcess([], 0, "OK", "")
            with patch.object(verificacion_local.subprocess, "run", side_effect=ejecutar):
                self.assertNotEqual(verificacion_local.verificar(raiz), 0)
            self.assertNotEqual(verificacion_local.comprobar(raiz), 0)

    def test_no_acepta_evidencia_sin_comprobaciones_requeridas(self):
        with tempfile.TemporaryDirectory() as temporal:
            raiz = Path(temporal)
            self.preparar(raiz)
            self.aprobado(raiz)
            archivo = raiz / verificacion_local.INFORME
            datos = json.loads(archivo.read_text())
            datos["resultados"] = []
            archivo.write_text(json.dumps(datos))
            self.assertNotEqual(verificacion_local.comprobar(raiz), 0)

    def test_cache_y_secretos_no_se_guardan_en_el_informe(self):
        with tempfile.TemporaryDirectory() as temporal:
            raiz = Path(temporal)
            self.preparar(raiz)
            self.aprobado(raiz)
            (raiz / "__pycache__").mkdir()
            (raiz / "__pycache__/cache.pyc").write_bytes(b"cache")
            (raiz / "privado.key").write_text("secreto")
            self.assertEqual(verificacion_local.comprobar(raiz), 0)
            self.assertNotIn("privado.key", (raiz / verificacion_local.INFORME).read_text())


if __name__ == "__main__":
    unittest.main()
