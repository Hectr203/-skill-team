"""Evita lectura externa, evidencia redirigida y fallos persistentes del protocolo."""
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import agencia
import agencia_mcp
import verificacion_local


class ControlesRuntimeTests(unittest.TestCase):
    def test_estado_rechaza_almacen_simbolico(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp); (raiz / 'contexts').mkdir(); (raiz / 'externo').mkdir()
            (raiz / 'contexts/projects').symlink_to(raiz / 'externo', target_is_directory=True)
            with patch.object(agencia, 'SCRIPT_DIR', raiz / 'scripts'):
                with self.assertRaises(ValueError): agencia.cmd_estado(None)

    def test_evidencia_valida_copiada_a_ruta_externa_no_se_acepta(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp); (raiz / 'codigo.py').write_text('pass\n')
            with patch.object(verificacion_local.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')):
                verificacion_local.verificar(raiz)
            informe = raiz / verificacion_local.INFORME
            with tempfile.TemporaryDirectory() as externo:
                copia = Path(externo) / 'informe.json'; copia.write_bytes(informe.read_bytes())
                informe.unlink(); informe.symlink_to(copia)
                self.assertEqual(verificacion_local.comprobar(raiz), 1)

    def test_version_booleana_no_valida_verificacion(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            with patch.object(verificacion_local.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')):
                verificacion_local.verificar(raiz)
            informe = raiz / verificacion_local.INFORME; datos = json.loads(informe.read_text())
            datos['version'] = True; informe.write_text(json.dumps(datos))
            self.assertEqual(verificacion_local.comprobar(raiz), 1)

    def test_ids_malformados_no_interrumpen_protocolo(self):
        salida = io.StringIO()
        with redirect_stdout(salida):
            for id_ in (True, [], {}): agencia_mcp.procesar_mensaje({'jsonrpc': '2.0', 'id': id_, 'method': 'ping'})
            agencia_mcp.procesar_mensaje({'jsonrpc': '2.0', 'id': 'valido', 'method': 'ping'})
        respuestas = [json.loads(x) for x in salida.getvalue().splitlines()]
        self.assertTrue(all(r['error']['code'] == -32600 for r in respuestas[:3]))
        self.assertEqual(respuestas[3], {'jsonrpc': '2.0', 'id': 'valido', 'result': {}})

    def test_metodo_desconocido_con_id_nulo_responde(self):
        salida = io.StringIO()
        with redirect_stdout(salida): agencia_mcp.procesar_mensaje({'jsonrpc': '2.0', 'id': None, 'method': 'desconocido'})
        self.assertEqual(json.loads(salida.getvalue())['error']['code'], -32601)


if __name__ == '__main__': unittest.main()
