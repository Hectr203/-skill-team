#!/usr/bin/env python3
"""Plan y estados locales transaccionales; no crea agentes ni ejecuta instrucciones."""
import copy
import hashlib
import json
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path, PurePosixPath
from memoria_proyecto import resolver_proyecto, rutas_memoria, validar_identificador, ahora_iso
from control_entregas import evaluar, cargar, texto

RAIZ = Path(__file__).resolve().parents[1]


def validar_plan(datos, proyecto, raiz=RAIZ):
    if not isinstance(datos, dict) or type(datos.get('version')) is not int or datos['version'] != 1:
        raise ValueError('Versión de plan inválida.')
    if datos.get('proyecto') != proyecto:
        raise ValueError('El plan pertenece a otro proyecto.')
    texto(datos.get('objetivo'), 'objetivo')
    tareas = datos.get('tareas')
    if not isinstance(tareas, list) or not 1 <= len(tareas) <= 200:
        raise ValueError('El plan requiere entre 1 y 200 tareas.')
    roles = cargar(raiz / 'reglas/rutas-agentes.json')['roles']
    ids, duenos = set(), {}
    for t in tareas:
        if not isinstance(t, dict) or set(t) - {'id', 'rol', 'depende_de', 'archivos', 'criterios', 'skills'}:
            raise ValueError('Campos de tarea inválidos; el estado lo gestiona la agencia.')
        validar_identificador(t.get('id'))
        if t['id'] in ids:
            raise ValueError('IDs de tarea duplicados.')
        ids.add(t['id'])
        if not isinstance(t.get('rol'), str) or (t['rol'] != 'asistente-principal' and t['rol'] not in roles):
            raise ValueError('Rol no registrado.')
        for campo in ('depende_de', 'archivos', 'criterios', 'skills'):
            v = t.get(campo)
            if not isinstance(v, list) or any(not isinstance(x, str) or not x.strip() for x in v) or len(v) != len(set(v)):
                raise ValueError(f'Lista inválida: {campo}.')
        if not t['criterios']:
            raise ValueError('Cada tarea requiere criterios de aceptación.')
        for archivo in t['archivos']:
            p = PurePosixPath(archivo)
            if p.is_absolute() or '..' in p.parts or '\\' in archivo or p.as_posix() != archivo or archivo == '.':
                raise ValueError('Los artefactos deben ser rutas relativas normalizadas.')
            if any(archivo == a or archivo.startswith(a + '/') or a.startswith(archivo + '/') for a in duenos):
                raise ValueError('Un artefacto necesita un único responsable; dividir tareas o definir un traspaso en un nuevo plan.')
            duenos[archivo] = t['id']
    restantes = {t['id']: set(t['depende_de']) for t in tareas}
    if any(deps - ids for deps in restantes.values()):
        raise ValueError('Dependencia inexistente.')
    while restantes:
        disponibles = {id_ for id_, deps in restantes.items() if not deps}
        if not disponibles:
            raise ValueError('Dependencias cíclicas.')
        restantes = {id_: deps - disponibles for id_, deps in restantes.items() if id_ not in disponibles}
    # Skills are optional, but names must resolve to a canonical source.
    if any(t['skills'] for t in tareas):
        from consulta_skills import resolver_skill
        for t in tareas:
            for nombre in t['skills']:
                resolver_skill(nombre, raiz)
    resultado = copy.deepcopy(datos)
    resultado['tareas'] = [{**t, 'estado': 'pendiente', 'motivo': '', 'entrega': None} for t in tareas]
    resultado['revision'] = 1
    resultado['historial'] = [{'fecha': ahora_iso(), 'accion': 'crear', 'revision': 1}]
    return resultado


@contextmanager
def almacen(proyecto, raiz=RAIZ, crear=False, escribir=False):
    raiz = Path(raiz).resolve()
    carpeta = resolver_proyecto(proyecto, raiz)
    if not carpeta.is_dir():
        raise ValueError('Proyecto no registrado.')
    base = rutas_memoria(carpeta)['base']
    destino = base / 'operacion.sqlite3'
    for nombre in ('operacion.sqlite3', 'operacion.sqlite3-journal', 'operacion.sqlite3-wal', 'operacion.sqlite3-shm'):
        if (base / nombre).is_symlink():
            raise ValueError('El almacén operativo no puede redirigirse.')
    if not destino.exists():
        if not crear:
            raise ValueError('Proyecto sin plan operativo.')
        base.mkdir(exist_ok=True)
        try:
            fd = os.open(destino, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.close(fd)
        except FileExistsError:
            pass
    try:
        conexion = sqlite3.connect(destino, timeout=5)
    except sqlite3.Error as exc:
        raise ValueError('No se puede abrir el almacén operativo; conservarlo y revisar su estado.') from exc
    try:
        conexion.execute('BEGIN IMMEDIATE' if crear or escribir else 'BEGIN')
        if crear:
            conexion.execute('CREATE TABLE IF NOT EXISTS plan (id INTEGER PRIMARY KEY CHECK(id=1), contenido TEXT NOT NULL)')
        yield conexion
        conexion.commit()
    except sqlite3.Error as exc:
        conexion.rollback()
        raise ValueError('Almacén operativo ocupado o inválido; conservarlo y revisar antes de reintentar.') from exc
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def _leer(db):
    fila = db.execute('SELECT contenido FROM plan WHERE id=1').fetchone()
    if not fila:
        raise ValueError('No existe un plan operativo.')
    datos = json.loads(fila[0])
    if not isinstance(datos, dict) or type(datos.get('revision')) is not int or datos['revision'] < 1:
        raise ValueError('Plan almacenado inválido; conservar y revisar el respaldo.')
    tareas = datos.get('tareas')
    if not isinstance(tareas, list) or not 1 <= len(tareas) <= 200 or not isinstance(datos.get('historial'), list):
        raise ValueError('Plan almacenado incompleto.')
    ids = set()
    for t in tareas:
        if not isinstance(t, dict) or not isinstance(t.get('id'), str) or t['id'] in ids:
            raise ValueError('Tareas almacenadas inconsistentes.')
        ids.add(t['id'])
        if t.get('estado') not in ('pendiente', 'en_curso', 'bloqueado', 'completado', 'cancelado') or not isinstance(t.get('depende_de'), list) or any(not isinstance(d, str) for d in t['depende_de']):
            raise ValueError('Estado o dependencias almacenadas inválidas.')
    if any(set(t['depende_de']) - ids for t in tareas):
        raise ValueError('Dependencia almacenada inexistente.')
    return datos


def vigente(tarea):
    if tarea['estado'] != 'completado':
        return False
    try:
        entrega = tarea['entrega']
        informe = Path(entrega['informe'])
        if informe.is_symlink() or hashlib.sha256(informe.read_bytes()).hexdigest() != entrega['sha256']:
            return False
        return evaluar(cargar(informe), entrega['raiz'])['aprobado']
    except (OSError, ValueError, TypeError, KeyError):
        return False


def crear_plan(proyecto, datos, raiz=RAIZ, revision=None):
    resultado = validar_plan(datos, proyecto, Path(raiz).resolve())
    with almacen(proyecto, raiz, crear=True) as db:
        existe = db.execute('SELECT id FROM plan WHERE id=1').fetchone()
        if existe:
            anterior = _leer(db)
            if type(revision) is not int or revision != anterior['revision']:
                raise ValueError('Plan existente: una nueva fase requiere su revisión actual explícita.')
            if not all(t['estado'] == 'cancelado' or t['evidencia_vigente'] for t in consultar(proyecto, raiz)['tareas']):
                raise ValueError('Cerrar o cancelar las tareas anteriores antes de iniciar otra fase.')
            db.execute('CREATE TABLE IF NOT EXISTS planes_anteriores (revision INTEGER PRIMARY KEY, contenido TEXT NOT NULL)')
            db.execute('INSERT INTO planes_anteriores VALUES (?, ?)', (anterior['revision'], json.dumps(anterior, ensure_ascii=False)))
            resultado['revision'] = anterior['revision'] + 1
            resultado['historial'] = anterior['historial'] + [{'fecha': ahora_iso(), 'accion': 'nueva_fase', 'revision': resultado['revision']}]
            db.execute('UPDATE plan SET contenido=? WHERE id=1', (json.dumps(resultado, ensure_ascii=False),))
        else:
            if revision is not None:
                raise ValueError('El primer plan no tiene revisión anterior.')
            db.execute('INSERT INTO plan VALUES (1, ?)', (json.dumps(resultado, ensure_ascii=False),))
    return resultado


def consultar(proyecto, raiz=RAIZ):
    with almacen(proyecto, raiz) as db:
        plan = _leer(db)
    tareas = {t['id']: t for t in plan['tareas']}
    # A completion loses validity when its own evidence or an ancestor changes.
    validez = {}
    restantes = set(tareas)
    while restantes:
        anterior = len(restantes)
        for id_ in list(restantes):
            t = tareas[id_]
            if all(dep in validez for dep in t['depende_de']):
                validez[id_] = vigente(t) and all(validez[d] for d in t['depende_de'])
                restantes.remove(id_)
        if len(restantes) == anterior:
            raise ValueError('Plan almacenado con dependencias inconsistentes.')
    for t in plan['tareas']:
        t['evidencia_vigente'] = validez[t['id']]
        t['lista_para_iniciar'] = t['estado'] in ('pendiente', 'bloqueado') and all(validez[d] for d in t['depende_de'])
    return plan


def cambiar(proyecto, tarea, estado, revision, motivo='', informe=None, raiz_entrega=None, raiz=RAIZ):
    if type(revision) is not int:
        raise ValueError('Indicar revisión entera esperada.')
    if estado not in ('en_curso', 'bloqueado', 'completado', 'cancelado'):
        raise ValueError('Estado de destino inválido.')
    with almacen(proyecto, raiz, escribir=True) as db:
        plan = _leer(db)
        if plan['revision'] != revision:
            raise ValueError('Conflicto de revisión: consultar y reconciliar antes de actualizar.')
        t = next((t for t in plan['tareas'] if t['id'] == tarea), None)
        if t is None:
            raise ValueError('Tarea no registrada.')
        permitido = {'pendiente': {'en_curso', 'bloqueado', 'cancelado'}, 'en_curso': {'bloqueado', 'completado', 'cancelado'}, 'bloqueado': {'en_curso', 'cancelado'}, 'completado': {'en_curso'}, 'cancelado': set()}
        if estado not in permitido[t['estado']]:
            raise ValueError('Transición de estado no permitida.')
        vista = consultar(proyecto, raiz)
        estados = {x['id']: x for x in vista['tareas']}
        if estado in ('en_curso', 'completado') and not all(estados[d]['evidencia_vigente'] for d in t['depende_de']):
            raise ValueError('Dependencias pendientes o evidencia desactualizada.')
        if estado in ('bloqueado', 'cancelado') or t['estado'] == 'completado':
            texto(motivo, 'motivo de bloqueo o reapertura')
        entrega = None
        if estado == 'completado':
            if informe is None or raiz_entrega is None:
                raise ValueError('Completar requiere informe y raíz de evidencia explícitos.')
            p = Path(informe).absolute()
            if p.resolve() != p:
                raise ValueError('Informe redirigido.')
            raw = p.read_bytes()
            datos = json.loads(raw)
            resultado = evaluar(datos, raiz_entrega)
            if not resultado['aprobado'] or (datos['proyecto'], datos['tarea']) != (proyecto, tarea):
                raise ValueError('Entrega incompleta o perteneciente a otra tarea.')
            if {c['id'] for c in datos['criterios']} != set(t['criterios']):
                raise ValueError('La entrega debe cubrir los criterios acordados en el plan.')
            if set(t['archivos']) - {a['archivo'] for a in datos.get('artefactos', [])}:
                raise ValueError('Faltan huellas de los artefactos asignados a la tarea.')
            entrega = {'informe': str(p), 'sha256': hashlib.sha256(raw).hexdigest(), 'raiz': str(Path(raiz_entrega).resolve())}
        t.update(estado=estado, motivo=motivo, entrega=entrega)
        plan['revision'] += 1
        plan['historial'].append({'fecha': ahora_iso(), 'tarea': tarea, 'estado': estado, 'motivo': motivo, 'revision': plan['revision']})
        db.execute('UPDATE plan SET contenido=? WHERE id=1', (json.dumps(plan, ensure_ascii=False),))
    return consultar(proyecto, raiz)


def historial_planes(proyecto, raiz=RAIZ):
    with almacen(proyecto, raiz) as db:
        existe = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='planes_anteriores'").fetchone()
        return [json.loads(fila[0]) for fila in db.execute('SELECT contenido FROM planes_anteriores ORDER BY revision')] if existe else []
