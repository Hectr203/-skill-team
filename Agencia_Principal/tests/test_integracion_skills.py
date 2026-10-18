"""Descubrimiento independiente, incorporación de roles y transporte sin ejecución implícita."""
import argparse
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import consulta_skills
import registrar_agente
import agencia_mcp
import configurar_mcp
import solicitar_validacion
import memoria_proyecto
import notificar_tarea
import arranque


class IntegracionSkillsTests(unittest.TestCase):
    def fuente(self, raiz, nombre='habilidad'):
        carpeta = raiz / 'skills' / nombre
        carpeta.mkdir(parents=True)
        archivo = carpeta / 'SKILL.md'
        archivo.write_text(f'---\nname: {nombre}\ndescription: >-\n  Revisa interfaz reutilizable.\n  Usa entradas reales.\n---\n\nNO EJECUTAR ESTE PROCEDIMIENTO\n')
        return archivo

    def test_descubrimiento_y_resolucion_no_exponen_procedimiento(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            archivo = self.fuente(raiz)
            antes = archivo.read_bytes()
            datos = consulta_skills.listar_skills('interfaz', raiz)
            self.assertEqual(datos[0]['nombre'], 'habilidad')
            self.assertIn('Usa entradas reales.', datos[0]['descripcion'])
            ficha = consulta_skills.resolver_skill('habilidad', raiz)
            self.assertEqual(ficha['directorio_recursos'], 'skills/habilidad')
            self.assertNotIn('NO EJECUTAR', json.dumps(ficha))
            self.assertEqual(antes, archivo.read_bytes())
            for nombre in ('../habilidad','desconocida',''):
                with self.assertRaises(ValueError):
                    consulta_skills.resolver_skill(nombre, raiz)

    def test_nueva_skill_es_descubierta_sin_editar_roles(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            self.fuente(raiz)
            self.fuente(raiz, 'otra-habilidad')
            self.assertEqual({f['nombre'] for f in consulta_skills.listar_skills(raiz=raiz)}, {'habilidad','otra-habilidad'})

    def test_skill_redirigida_se_rechaza(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            fuente = self.fuente(raiz)
            exterior = raiz / 'externa.md'
            fuente.rename(exterior)
            fuente.symlink_to(exterior)
            with self.assertRaises(ValueError):
                consulta_skills.listar_skills(raiz=raiz)

    def test_nuevo_rol_reutiliza_seleccion_sin_lista_fija(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            (raiz/'agentes').mkdir()
            (raiz/'reglas').mkdir()
            registro = raiz/'reglas/rutas-agentes.json'
            registro.write_text('{"version":1,"roles":{}}')
            (raiz/'agentes/nuevo.md').write_text('contrato-agente.md precedencia.md Activación Entradas Entrega aceptación')
            registrar_agente.registrar('nuevo', raiz)
            self.assertEqual(json.loads(registro.read_text())['roles']['nuevo']['skills'], [])
            antes=registro.read_bytes()
            (raiz/'agentes/otro.md').write_text('incompleto')
            with self.assertRaises(ValueError): registrar_agente.registrar('otro', raiz)
            self.assertEqual(antes,registro.read_bytes())

    def test_mcp_publica_consulta_y_resolucion_y_propaga_fallos(self):
        nombres={t['name'] for t in agencia_mcp.TOOLS_DEFINITIONS}
        self.assertTrue({'agencia_skills','agencia_skill'} <= nombres)
        with patch('consulta_skills.resolver_skill',return_value={'fuente':'skills/ejemplo/SKILL.md'}) as resolver:
            texto, fallo = agencia_mcp.ejecutar_herramienta('agencia_skill',{'nombre':'ejemplo'})
            self.assertFalse(fallo)
            self.assertIn('fuente', json.loads(texto))
            resolver.assert_called_once_with('ejemplo')
        self.assertTrue(agencia_mcp.ejecutar_herramienta('agencia_skill',{'nombre':'../escapa'})[1])

    def test_generador_configuracion_adapta_ruta_del_checkout(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz=Path(tmp)
            (raiz/'scripts').mkdir()
            (raiz/'scripts/agencia_mcp.py').write_text('')
            generic=configurar_mcp.configuracion(raiz)
            self.assertEqual(generic['mcpServers']['agencia']['args'], [str(raiz/'scripts/agencia_mcp.py')])
            self.assertIn(str(raiz),configurar_mcp.configuracion(raiz,'opencode')['skills']['paths'][0])

    def test_validacion_pendiente_y_silencio_no_aprueban(self):
        args=argparse.Namespace(preguntas='prueba',sin_interfaz=True,sin_navegador=False,sin_sonido=False,sin_escritorio=False,esperar=False)
        with tempfile.TemporaryDirectory() as tmp, patch.object(solicitar_validacion,'parse_args',return_value=args), patch.object(solicitar_validacion,'ARCHIVO_AUDITORIA',Path(tmp)/'auditoria.jsonl'), patch.object(solicitar_validacion.sys.stdin,'isatty',return_value=False), patch.object(solicitar_validacion,'reproducir_sonido_sistema') as audio, patch.object(solicitar_validacion,'crear_html_validacion') as html, redirect_stdout(io.StringIO()):
            self.assertEqual(solicitar_validacion.main(),2)
            audio.assert_not_called()
            html.assert_not_called()

    def test_validacion_fallo_de_registro_bloquea(self):
        args=argparse.Namespace(preguntas='prueba',sin_interfaz=True,sin_navegador=True,sin_sonido=True,sin_escritorio=True,esperar=True)
        with tempfile.TemporaryDirectory() as tmp, patch.object(solicitar_validacion,'parse_args',return_value=args), patch.object(solicitar_validacion,'ARCHIVO_AUDITORIA',Path(tmp)/'ausente/auditoria.jsonl'), patch('builtins.input') as entrada, redirect_stdout(io.StringIO()):
            self.assertEqual(solicitar_validacion.main(),1)
            entrada.assert_not_called()

    def test_notificacion_respeta_silencio(self):
        args=argparse.Namespace(diagnostico=False,auto_completado=True,urgente=False,estado='',mensaje='',tarea='prueba',repeticiones=2,sin_interfaz=True,sin_navegador=False,sin_sonido=False,sin_escritorio=False)
        with patch.object(notificar_tarea,'parse_args',return_value=args), patch.object(notificar_tarea,'crear_html_notificacion') as html, patch.object(notificar_tarea,'reproducir_sonido_sistema') as audio, patch.object(notificar_tarea,'enviar_notificacion_escritorio') as escritorio, redirect_stdout(io.StringIO()):
            self.assertEqual(notificar_tarea.main(),0)
            html.assert_not_called(); audio.assert_not_called(); escritorio.assert_not_called()

    def test_memoria_no_activa_proveedores_externos_instalados(self):
        with tempfile.TemporaryDirectory() as tmp, patch('subprocess.run') as ejecutar:
            memoria_proyecto.agregar_cloudmem(Path(tmp),'nota',[])
            ejecutar.assert_not_called()

    def test_adr_redirigido_se_rechaza(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz=Path(tmp);(raiz/'adrs').mkdir();externo=raiz/'externo.md';externo.write_text('externo')
            (raiz/'adrs/ADR-001.md').symlink_to(externo)
            with self.assertRaises(ValueError):arranque.obtener_paquete_contexto(raiz)


if __name__=='__main__':unittest.main()
