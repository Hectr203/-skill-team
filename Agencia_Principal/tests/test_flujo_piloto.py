"""Piloto reproducible del ciclo CLI/MCP con dos clientes en un almacén aislado."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


class FlujoPilotoTests(unittest.TestCase):
    def test_crear_arrancar_cerrar_y_reanudar_sin_mezclar_clientes(self):
        with tempfile.TemporaryDirectory() as temporal:
            agencia = Path(temporal) / "agencia"
            for carpeta in ("scripts", "plantillas", "stacks"):
                shutil.copytree(RAIZ / carpeta, agencia / carpeta, ignore=shutil.ignore_patterns("__pycache__"))

            def cli(*argumentos):
                resultado = subprocess.run([sys.executable, str(agencia / "scripts/agencia.py"), *argumentos],
                                           cwd=agencia, capture_output=True, text=True, timeout=15)
                self.assertEqual(resultado.returncode, 0, resultado.stdout + resultado.stderr)
                return resultado.stdout

            cli("nuevo", "cliente-uno-web", "--cliente", "Cliente Uno")
            cli("nuevo", "cliente-dos-web", "--cliente", "Cliente Dos", "--stack", "laravel-livewire-alpine")
            cli("arranque", "cliente-uno-web", "--prime")
            cli("cierre", "cliente-uno-web", "--tareas", "PILOTO-UNO-VERIFICADO", "--decisiones", "Memoria por ID explícito")
            contexto = json.loads(cli("arranque", "cliente-uno-web", "--json"))
            self.assertIn("PILOTO-UNO-VERIFICADO", contexto["memoria"]["contenido"])
            self.assertTrue(contexto["timeline_reciente"])
            otro = json.loads(cli("arranque", "cliente-dos-web", "--json"))
            self.assertNotIn("PILOTO-UNO-VERIFICADO", otro["memoria"]["contenido"])
            solicitud = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {
                "name": "agencia_arranque", "arguments": {"proyecto": "cliente-uno-web", "formato": "json"}}}
            respuesta = subprocess.run([sys.executable, str(agencia / "scripts/agencia_mcp.py")],
                                       input=json.dumps(solicitud) + "\n", capture_output=True, text=True, timeout=15)
            datos = json.loads(respuesta.stdout)["result"]
            self.assertFalse(datos["isError"])
            self.assertIn("PILOTO-UNO-VERIFICADO", datos["content"][0]["text"])


if __name__ == "__main__":
    unittest.main()
