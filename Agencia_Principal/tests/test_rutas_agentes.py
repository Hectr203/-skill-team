"""Regresiones de resolución y cobertura de roles, aisladas del repositorio vivo."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validar_rutas_agentes import comprobar_rutas


class RutasAgentes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.raiz = Path(self.tmp.name)
        for carpeta in ('agentes', 'reglas', 'skills/habilidad'):
            (self.raiz / carpeta).mkdir(parents=True)
        (self.raiz / 'skills/habilidad/SKILL.md').write_text('---\nname: habilidad\ndescription: Resolver tarea.\n---\n')
        (self.raiz / 'agentes/rol.md').write_text('contrato-agente.md precedencia.md Activación Entradas Entrega aceptación `habilidad`')
        self.registro = {'version': 1, 'roles': {'rol': {'archivo': 'agentes/rol.md', 'skills': ['habilidad']}}}

    def comprobar(self):
        (self.raiz / 'reglas/rutas-agentes.json').write_text(json.dumps(self.registro))
        return comprobar_rutas(self.raiz)

    def test_resuelve_fuente_existente(self):
        self.assertEqual(self.comprobar(), [])

    def test_detecta_skill_no_disponible(self):
        self.registro['roles']['rol']['skills'].append('inexistente')
        self.assertTrue(any('no resoluble' in e for e in self.comprobar()))

    def test_detecta_rol_sin_ruta(self):
        (self.raiz / 'agentes/nuevo.md').write_text('otro rol')
        self.assertTrue(any('sin registro' in e for e in self.comprobar()))

    def test_rechaza_escape_del_directorio(self):
        self.registro['roles']['rol']['archivo'] = '../exterior.md'
        self.assertTrue(any('Archivo de rol inválido' in e for e in self.comprobar()))

    def test_detecta_desacuerdo_ficha_registro(self):
        (self.raiz / 'agentes/rol.md').write_text('contrato-agente.md precedencia.md Activación Entradas Entrega aceptación')
        self.assertTrue(any('sin criterio documentado' in e for e in self.comprobar()))

    def test_detecta_invocacion_duplicada(self):
        self.registro['roles']['rol']['skills'].append('habilidad')
        self.assertTrue(any('duplicada' in e for e in self.comprobar()))


if __name__ == '__main__':
    unittest.main()
