"""Regresiones de aislamiento, permisos y propagación de errores."""
import argparse
import io
import importlib.util
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "scripts"))
import agencia_mcp
import memoria_proyecto
import nuevo_proyecto
import solicitar_autorizacion


class ControlesTests(unittest.TestCase):
    def test_rutas_externas_no_se_aliasan_por_nombre(self):
        with tempfile.TemporaryDirectory() as temporal:
            for ruta in ("/clientes/uno/web", "/clientes/dos/web", "../web", "", ".", ".."):
                with self.subTest(ruta=ruta), self.assertRaises(ValueError):
                    memoria_proyecto.resolver_proyecto(ruta, Path(temporal))

    def test_id_y_ruta_central_resuelven_la_misma_memoria(self):
        with tempfile.TemporaryDirectory() as temporal:
            raiz = Path(temporal)
            esperado = raiz / "contexts/projects/cliente-uno-web"
            self.assertEqual(memoria_proyecto.resolver_proyecto("cliente-uno-web", raiz), esperado)
            self.assertEqual(memoria_proyecto.resolver_proyecto(esperado, raiz), esperado)

    def test_estado_de_memoria_no_admite_enlaces(self):
        with tempfile.TemporaryDirectory() as temporal:
            raiz = Path(temporal)
            proyecto = raiz / "proyecto"
            proyecto.mkdir()
            (proyecto / ".memoria").symlink_to(raiz, target_is_directory=True)
            with self.assertRaises(ValueError):
                memoria_proyecto.rutas_memoria(proyecto)

    def test_lectura_sin_clave_no_modifica_estado(self):
        with tempfile.TemporaryDirectory() as temporal:
            proyecto = Path(temporal)
            (proyecto / ".memoria").mkdir()
            cifrado = proyecto / ".memoria/mem_palace.enc"
            cifrado.write_bytes(b"historial-cifrado-sin-clave")
            with self.assertRaises(ValueError):
                memoria_proyecto.inicializar(proyecto)
            self.assertFalse((proyecto / ".memoria/mem_palace.key").exists())
            self.assertFalse((proyecto / "memoria.md").exists())
            self.assertEqual(cifrado.read_bytes(), b"historial-cifrado-sin-clave")

    @unittest.skipUnless(importlib.util.find_spec("cryptography"), "Cifrado opcional no instalado")
    def test_migracion_legacy_conserva_historial(self):
        from cryptography.fernet import Fernet
        with tempfile.TemporaryDirectory() as temporal:
            proyecto = Path(temporal)
            (proyecto / ".memoria").mkdir()
            clave = Fernet.generate_key()
            (proyecto / ".memoria/mem_palace.key").write_bytes(clave)
            (proyecto / ".memoria/mem_palace.enc").write_bytes(Fernet(clave).encrypt(b"HISTORIAL-PREVIO"))
            memoria_proyecto.inicializar(proyecto)
            self.assertEqual((proyecto / "memoria.md").read_text(), "HISTORIAL-PREVIO")

    def test_enlace_simbolico_no_sale_del_almacen(self):
        with tempfile.TemporaryDirectory() as temporal:
            raiz = Path(temporal)
            proyectos = raiz / "contexts/projects"
            proyectos.mkdir(parents=True)
            (proyectos / "escapa").symlink_to(raiz, target_is_directory=True)
            with self.assertRaises(ValueError):
                memoria_proyecto.resolver_proyecto("escapa", raiz)

    def test_mcp_propaga_codigos_de_fallo(self):
        for herramienta, funcion in (("agencia_validar", "agencia.cmd_validar"),
                                     ("agencia_doctor", "doctor.Doctor.ejecutar")):
            with self.subTest(herramienta=herramienta), patch(funcion, return_value=1):
                texto, fallo = agencia_mcp.ejecutar_herramienta(herramienta, {})
                self.assertTrue(fallo)
                self.assertIn("1", texto)

    def test_mcp_valida_argumentos_antes_de_mutar(self):
        with patch("nuevo_proyecto.crear_proyecto") as crear:
            for argumentos in ({}, {"nombre": None}, {"nombre": "prueba", "tipo": "invalido"},
                               {"nombre": "prueba", "extra": True}):
                _, fallo = agencia_mcp.ejecutar_herramienta("agencia_nuevo", argumentos)
                self.assertTrue(fallo)
            crear.assert_not_called()

    def test_mcp_nuevo_admite_stack(self):
        with patch("nuevo_proyecto.crear_proyecto") as crear:
            _, fallo = agencia_mcp.ejecutar_herramienta("agencia_nuevo", {"nombre": "prueba", "stack": "laravel-livewire-alpine"})
            self.assertFalse(fallo)
            self.assertEqual(crear.call_args.kwargs["stack"], "laravel-livewire-alpine")

    def test_mcp_sobrevive_json_de_forma_invalida(self):
        salida = io.StringIO()
        with redirect_stdout(salida):
            for mensaje in ([], None, {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": []}):
                agencia_mcp.procesar_mensaje(mensaje)
            agencia_mcp.procesar_mensaje({"jsonrpc": "2.0", "id": 2, "method": "ping"})
        respuestas = [json.loads(linea) for linea in salida.getvalue().splitlines()]
        self.assertEqual(respuestas[-1]["id"], 2)

    def test_autorizacion_pendiente_no_es_exito(self):
        argumentos = argparse.Namespace(recurso="prueba", sin_interfaz=False, sin_navegador=True,
                                        sin_sonido=True, sin_escritorio=True, esperar=False)
        with tempfile.TemporaryDirectory() as temporal, patch.object(solicitar_autorizacion, "parse_args", return_value=argumentos), \
             patch.object(solicitar_autorizacion, "ARCHIVO_AUDITORIA", Path(temporal)/"auditoria.jsonl", create=True), \
             patch.object(solicitar_autorizacion.sys.stdin, "isatty", return_value=False), \
             patch.object(solicitar_autorizacion, "reproducir_sonido_sistema"), \
             patch.object(solicitar_autorizacion, "crear_html_autorizacion", return_value=Path(temporal)/"aviso.html"), \
             patch.object(solicitar_autorizacion.webbrowser, "open_new_tab"):
            self.assertNotEqual(solicitar_autorizacion.main(), 0)

    def test_autorizacion_aprobada_rechazada_y_auditoria(self):
        for respuesta, esperado, estado in (("sí", 0, "aprobada"), ("n", 1, "rechazada")):
            argumentos = argparse.Namespace(recurso="prueba", sin_interfaz=True, sin_navegador=True,
                                            sin_sonido=True, sin_escritorio=True, esperar=True)
            with self.subTest(respuesta=respuesta), tempfile.TemporaryDirectory() as temporal:
                auditoria = Path(temporal) / "auditoria.jsonl"
                with patch.object(solicitar_autorizacion, "parse_args", return_value=argumentos), \
                     patch.object(solicitar_autorizacion, "ARCHIVO_AUDITORIA", auditoria), \
                     patch("builtins.input", return_value=respuesta), redirect_stdout(io.StringIO()):
                    self.assertEqual(solicitar_autorizacion.main(), esperado)
                eventos = [json.loads(linea) for linea in auditoria.read_text().splitlines()]
                self.assertEqual(eventos[-1]["resultado"], estado)
                self.assertEqual(eventos[0]["id"], eventos[-1]["id"])

    def test_auditoria_fallida_bloquea_aprobacion(self):
        argumentos = argparse.Namespace(recurso="prueba", sin_interfaz=True, sin_navegador=True,
                                        sin_sonido=True, sin_escritorio=True, esperar=True)
        with tempfile.TemporaryDirectory() as temporal, patch.object(solicitar_autorizacion, "parse_args", return_value=argumentos), \
             patch.object(solicitar_autorizacion, "ARCHIVO_AUDITORIA", Path(temporal)/"ausente/auditoria.jsonl"), \
             patch("builtins.input", return_value="s") as entrada:
            self.assertNotEqual(solicitar_autorizacion.main(), 0)
            entrada.assert_not_called()

    def test_creacion_aislada_y_stack_invalido_no_mutan_agencia(self):
        with tempfile.TemporaryDirectory() as temporal:
            raiz = Path(temporal)
            (raiz / "stacks/estandar").mkdir(parents=True)
            with redirect_stdout(io.StringIO()):
                destino = nuevo_proyecto.crear_proyecto("cliente-web", raiz_agencia=raiz)
            self.assertTrue((destino / "manifiesto.md").exists())
            for nombre, stack in (("..", "estandar"), ("otro", "../../escapa"), ("otro", "desconocido")):
                with self.subTest(nombre=nombre, stack=stack), self.assertRaises(ValueError):
                    nuevo_proyecto.crear_proyecto(nombre, stack=stack, raiz_agencia=raiz)
            self.assertFalse((raiz / "contexts/projects/otro").exists())


if __name__ == "__main__":
    unittest.main()
