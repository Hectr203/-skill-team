import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


class AgenciaOperativaTests(unittest.TestCase):
    def mcp(self, messages):
        payload = "\n".join(json.dumps(m) for m in messages) + "\n"
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "agencia_mcp.py")],
            input=payload, text=True, capture_output=True, timeout=15,
        )

    def test_mcp_survives_invalid_tool_call(self):
        result = self.mcp([
            {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
             "params": {"name": "agencia_arranque", "arguments": {"proyecto": "__missing__"}}},
            {"jsonrpc": "2.0", "id": 2, "method": "ping"},
        ])
        self.assertEqual(result.returncode, 0)
        responses = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertTrue(responses[0]["result"]["isError"])
        self.assertEqual(responses[1]["id"], 2)

    def test_validator_is_json_safe_through_mcp(self):
        result = self.mcp([{"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                            "params": {"name": "agencia_validar", "arguments": {}}}])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        responses = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertIn("VALIDACION OK", responses[0]["result"]["content"][0]["text"])

    def test_fuzzy_lookup_does_not_choose_between_projects(self):
        import importlib
        if str(SCRIPTS) not in sys.path:
            sys.path.insert(0, str(SCRIPTS))
        arranque_mod = importlib.import_module("arranque")
        resolver_proyecto_fuzzy = getattr(arranque_mod, "resolver_proyecto_fuzzy")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projects = root / "contexts" / "projects"
            (projects / "cliente-web").mkdir(parents=True)
            (projects / "cliente-api").mkdir()
            self.assertIsNone(resolver_proyecto_fuzzy("cliente", root))

    def test_nuevo_proyecto_con_stack(self):
        import importlib
        nuevo_mod = importlib.import_module("nuevo_proyecto")
        crear_proyecto = getattr(nuevo_mod, "crear_proyecto")
        with tempfile.TemporaryDirectory() as tmp:
            # Probar creación de proyecto y verificación de manifiesto
            nombre = "test-proyecto-stack"
            # Simular en el directorio real de la agencia temporalmente y luego limpiar
            raiz_agencia = ROOT
            destino = raiz_agencia / "contexts" / "projects" / nombre
            try:
                crear_proyecto(nombre, cliente="Cliente Test", tipo="nuevo", stack="estandar")
                self.assertTrue(destino.exists())
                manifiesto = (destino / "manifiesto.md").read_text(encoding="utf-8")
                self.assertIn("Stack Tecnológico Asignado: stacks/estandar", manifiesto)
            finally:
                if destino.exists():
                    import shutil
                    shutil.rmtree(destino)


if __name__ == "__main__":
    unittest.main()
