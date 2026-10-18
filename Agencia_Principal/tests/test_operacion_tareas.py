"""Dependencias, conflictos, cierre vinculado al código y recuperación por CLI/MCP."""
import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'scripts'))
from operacion_tareas import crear_plan, consultar, cambiar


class OperacionTareasTests(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory(); self.addCleanup(self.temporal.cleanup)
        self.raiz = Path(self.temporal.name)
        (self.raiz / 'contexts/projects/uno').mkdir(parents=True)
        (self.raiz / 'reglas').mkdir()
        (self.raiz / 'reglas/rutas-agentes.json').write_text(json.dumps({'roles': {'backend': {}, 'frontend': {}}}))
        self.plan = {'version': 1, 'proyecto': 'uno', 'objetivo': 'Integrar dominio', 'tareas': [
            {'id': 'api', 'rol': 'backend', 'depende_de': [], 'archivos': ['api.js'], 'criterios': ['C1'], 'skills': []},
            {'id': 'ui', 'rol': 'frontend', 'depende_de': ['api'], 'archivos': ['ui.jsx'], 'criterios': ['C1'], 'skills': []}]}

    def entrega(self, tarea='api'):
        artefacto = 'api.js' if tarea == 'api' else 'ui.jsx'
        (self.raiz / artefacto).write_text('implementación observada')
        (self.raiz / f'{tarea}.log').write_text('control ejecutado: éxito')
        def huella(name): return {'archivo': name, 'sha256': hashlib.sha256((self.raiz / name).read_bytes()).hexdigest()}
        datos = {'version': 1, 'proyecto': 'uno', 'tarea': tarea, 'responsable': 'principal', 'alcance': 'Dominio',
                 'perfil': 'existente', 'estado': 'completado', 'inicio': '2026-10-08T09:00:00-06:00',
                 'fin': '2026-10-08T10:00:00-06:00', 'retrabajo_minutos': 0, 'costo': None, 'skills': [], 'riesgos': [],
                 'criterios': [{'id': 'C1', 'descripcion': 'Contrato compatible', 'estado': 'cumplido', 'evidencias': [huella(f'{tarea}.log')]}],
                 'artefactos': [huella(artefacto)]}
        p = self.raiz / f'{tarea}.json'; p.write_text(json.dumps(datos)); return p

    def test_dependencia_no_inicia_hasta_entrega_vigente(self):
        crear_plan('uno', self.plan, self.raiz)
        with self.assertRaises(ValueError): cambiar('uno', 'ui', 'en_curso', 1, raiz=self.raiz)
        cambiar('uno', 'api', 'en_curso', 1, raiz=self.raiz)
        with self.assertRaises(ValueError): cambiar('uno', 'api', 'completado', 2, raiz=self.raiz)
        cambiar('uno', 'api', 'completado', 2, informe=self.entrega(), raiz_entrega=self.raiz, raiz=self.raiz)
        cambiar('uno', 'ui', 'en_curso', 3, raiz=self.raiz)
        (self.raiz / 'api.js').write_text('cambio posterior no probado')
        self.assertFalse(consultar('uno', self.raiz)['tareas'][0]['evidencia_vigente'])
        with self.assertRaises(ValueError): cambiar('uno', 'ui', 'completado', 4, informe=self.entrega('ui'), raiz_entrega=self.raiz, raiz=self.raiz)

    def test_ciclos_roles_archivos_duplicados_y_ids_no_se_registran(self):
        for defecto in ('ciclo', 'rol', 'archivo', 'id', 'dependencia'):
            with self.subTest(defecto=defecto):
                p = copy.deepcopy(self.plan)
                if defecto == 'ciclo': p['tareas'][0]['depende_de'] = ['ui']
                elif defecto == 'rol': p['tareas'][0]['rol'] = 'fantasma'
                elif defecto == 'archivo': p['tareas'][1]['archivos'] = ['api.js']
                elif defecto == 'id': p['tareas'][1]['id'] = 'api'
                else: p['tareas'][1]['depende_de'] = ['inexistente']
                with self.assertRaises(ValueError): crear_plan('uno', p, self.raiz)
        self.assertFalse((self.raiz / 'contexts/projects/uno/.memoria/operacion.sqlite3').exists())

    def test_concurrencia_rechaza_actualizacion_perdida(self):
        crear_plan('uno', self.plan, self.raiz)
        def escribir():
            try: cambiar('uno', 'api', 'en_curso', 1, raiz=self.raiz); return True
            except ValueError: return False
        with ThreadPoolExecutor(max_workers=2) as ejecutor:
            self.assertEqual(sorted(ejecutor.map(lambda _: escribir(), range(2))), [False, True])
        self.assertEqual(consultar('uno', self.raiz)['revision'], 2)

    def test_cierre_ajeno_o_sin_artefacto_no_modifica_revision(self):
        crear_plan('uno', self.plan, self.raiz); cambiar('uno', 'api', 'en_curso', 1, raiz=self.raiz)
        p = self.entrega()
        for campo in ('tarea', 'artefactos'):
            datos = json.loads(p.read_text()); datos[campo] = 'otra' if campo == 'tarea' else []
            p.write_text(json.dumps(datos))
            with self.assertRaises(ValueError): cambiar('uno', 'api', 'completado', 2, informe=p, raiz_entrega=self.raiz, raiz=self.raiz)
            self.assertEqual(consultar('uno', self.raiz)['revision'], 2)
            p = self.entrega()

    def test_reabrir_exige_motivo_y_no_sobrescribe_plan(self):
        crear_plan('uno', self.plan, self.raiz)
        with self.assertRaises(ValueError): crear_plan('uno', self.plan, self.raiz)
        cambiar('uno', 'api', 'en_curso', 1, raiz=self.raiz)
        cambiar('uno', 'api', 'completado', 2, informe=self.entrega(), raiz_entrega=self.raiz, raiz=self.raiz)
        with self.assertRaises(ValueError): cambiar('uno', 'api', 'en_curso', 3, raiz=self.raiz)
        cambiar('uno', 'api', 'en_curso', 3, motivo='Corregir contrato', raiz=self.raiz)
        vista = consultar('uno', self.raiz)
        self.assertFalse(vista['tareas'][1]['lista_para_iniciar'])
        self.assertEqual(len(vista['historial']), 4)

    def test_almacen_redirigido_y_clientes_aislados(self):
        crear_plan('uno', self.plan, self.raiz)
        (self.raiz / 'contexts/projects/dos').mkdir()
        with self.assertRaises(ValueError): consultar('dos', self.raiz)
        db = self.raiz / 'contexts/projects/uno/.memoria/operacion.sqlite3'
        db.rename(db.with_suffix('.backup')); db.symlink_to(db.with_suffix('.backup'))
        with self.assertRaises(ValueError): consultar('uno', self.raiz)

    def test_cierre_completo_y_cascada_de_evidencia(self):
        crear_plan('uno', self.plan, self.raiz)
        cambiar('uno', 'api', 'en_curso', 1, raiz=self.raiz)
        cambiar('uno', 'api', 'completado', 2, informe=self.entrega(), raiz_entrega=self.raiz, raiz=self.raiz)
        cambiar('uno', 'ui', 'en_curso', 3, raiz=self.raiz)
        cambiar('uno', 'ui', 'completado', 4, informe=self.entrega('ui'), raiz_entrega=self.raiz, raiz=self.raiz)
        self.assertTrue(all(t['evidencia_vigente'] for t in consultar('uno', self.raiz)['tareas']))
        (self.raiz / 'api.js').write_text('cambio no validado')
        self.assertFalse(any(t['evidencia_vigente'] for t in consultar('uno', self.raiz)['tareas']))
        with self.assertRaises(ValueError): crear_plan('uno', self.plan, self.raiz, revision=5)

    def test_almacen_corrupto_no_se_borra_ni_reinicia(self):
        base = self.raiz / 'contexts/projects/uno/.memoria'; base.mkdir()
        p = base / 'operacion.sqlite3'; p.write_bytes(b'contenido corrupto')
        with self.assertRaises(ValueError): consultar('uno', self.raiz)
        self.assertEqual(p.read_bytes(), b'contenido corrupto')

    def test_cambiar_sin_plan_no_crea_almacen(self):
        with self.assertRaises(ValueError): cambiar('uno', 'api', 'en_curso', 1, raiz=self.raiz)
        self.assertFalse((self.raiz / 'contexts/projects/uno/.memoria/operacion.sqlite3').exists())

    def test_nueva_fase_archiva_sin_perder_historial(self):
        from operacion_tareas import historial_planes
        crear_plan('uno', self.plan, self.raiz)
        with self.assertRaises(ValueError): crear_plan('uno', self.plan, self.raiz, revision=1)
        with self.assertRaises(ValueError): cambiar('uno', 'api', 'cancelado', 1, raiz=self.raiz)
        cambiar('uno', 'api', 'cancelado', 1, motivo='Cambio de alcance autorizado', raiz=self.raiz)
        cambiar('uno', 'ui', 'cancelado', 2, motivo='Depende del contrato retirado', raiz=self.raiz)
        crear_plan('uno', self.plan, self.raiz, revision=3)
        self.assertEqual(consultar('uno', self.raiz)['revision'], 4)
        anterior = historial_planes('uno', self.raiz)
        self.assertEqual(len(anterior), 1)
        self.assertEqual(anterior[0]['tareas'][0]['estado'], 'cancelado')
        self.assertEqual(anterior[0]['revision'], 3)

    def test_cli_mcp_reanuda_plan_sin_crear_agentes(self):
        shutil.copytree(RAIZ / 'scripts', self.raiz / 'scripts', ignore=shutil.ignore_patterns('__pycache__'))
        p = self.raiz / 'plan.json'; p.write_text(json.dumps(self.plan))
        cmd = [sys.executable, str(self.raiz / 'scripts/agencia.py'), 'tareas']
        creado = subprocess.run(cmd + ['crear', 'uno', '--plan', str(p)], capture_output=True, text=True, timeout=10)
        self.assertEqual(creado.returncode, 0, creado.stderr)
        result = subprocess.run(cmd + ['cambiar', 'uno', '--tarea', 'api', '--estado', 'en_curso', '--revision', '1'], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        mensaje = {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call', 'params': {'name': 'agencia_plan', 'arguments': {'proyecto': 'uno'}}}
        proceso = subprocess.run([sys.executable, str(self.raiz / 'scripts/agencia_mcp.py')], input=json.dumps(mensaje)+'\n', capture_output=True, text=True, timeout=10)
        resultado = json.loads(proceso.stdout)['result']; self.assertFalse(resultado['isError'])
        vista = json.loads(resultado['content'][0]['text'])
        self.assertEqual(vista['revision'], 2); self.assertEqual(vista['tareas'][0]['estado'], 'en_curso')


if __name__ == '__main__': unittest.main()
