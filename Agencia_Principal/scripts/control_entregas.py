#!/usr/bin/env python3
"""Comprueba criterios y evidencias locales; nunca ejecuta comandos del informe."""
import argparse
import hashlib
import json
import math
import re
import statistics
from datetime import datetime
from pathlib import Path


def fecha(valor):
    if not isinstance(valor, str):
        raise ValueError('Fecha inválida.')
    resultado = datetime.fromisoformat(valor.replace('Z', '+00:00'))
    if resultado.tzinfo is None:
        raise ValueError('Las fechas deben indicar zona horaria.')
    return resultado


def numero(valor, campo):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)) or not math.isfinite(valor) or valor < 0:
        raise ValueError(f'{campo}: se requiere un número finito no negativo.')
    return valor


def texto(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f'{campo}: se requiere texto no vacío.')
    return valor


def comprobar_archivo(evidencia, raiz):
    if not isinstance(evidencia, dict):
        raise ValueError('Evidencia inválida.')
    ruta = Path(texto(evidencia.get('archivo'), 'evidencia.archivo'))
    if ruta.is_absolute() or '..' in ruta.parts:
        raise ValueError('La evidencia debe permanecer en la raíz indicada.')
    archivo = raiz / ruta
    if archivo.resolve() != archivo or not archivo.is_file():
        raise ValueError('Evidencia ausente o redirigida por enlace simbólico.')
    huella = evidencia.get('sha256')
    if not isinstance(huella, str) or not re.fullmatch('[a-f0-9]{64}', huella):
        raise ValueError('SHA-256 inválido.')
    # Stream large evidence rather than copying it entirely into memory.
    huella_actual = hashlib.sha256()
    with archivo.open('rb') as fuente:
        for bloque in iter(lambda: fuente.read(65536), b''):
            huella_actual.update(bloque)
    actual = huella_actual.hexdigest()
    if actual != huella:
        raise ValueError('Evidencia o artefacto modificado.')


def evaluar(datos, raiz):
    if not isinstance(datos, dict) or type(datos.get('version')) is not int or datos.get('version') != 1:
        raise ValueError('Informe de entrega incompatible.')
    for campo in ('proyecto', 'tarea', 'responsable', 'alcance', 'perfil'):
        texto(datos.get(campo), campo)
    if datos.get('estado') not in ('completado', 'parcial', 'bloqueado'):
        raise ValueError('Estado desconocido.')
    inicio, fin = fecha(datos.get('inicio')), fecha(datos.get('fin'))
    if fin < inicio:
        raise ValueError('El fin precede al inicio.')
    numero(datos.get('retrabajo_minutos'), 'retrabajo_minutos')
    costos = datos.get('costo')
    if costos is not None:
        if not isinstance(costos, dict):
            raise ValueError('Costo inválido.')
        numero(costos.get('importe'), 'costo.importe')
        if not isinstance(costos.get('moneda'), str) or not re.fullmatch('[A-Z]{3}', costos['moneda']):
            raise ValueError('Moneda: usar código de tres letras.')
    criterios = datos.get('criterios')
    if not isinstance(criterios, list) or not criterios:
        raise ValueError('Se requiere al menos un criterio acordado.')
    raiz = Path(raiz).resolve(strict=True)
    if not raiz.is_dir():
        raise ValueError('La raíz de evidencias debe ser un directorio.')
    pendientes, nombres = [], set()
    for criterio in criterios:
        if not isinstance(criterio, dict):
            raise ValueError('Criterio inválido.')
        nombre = texto(criterio.get('id'), 'criterio.id')
        texto(criterio.get('descripcion'), 'criterio.descripcion')
        if nombre in nombres:
            raise ValueError('IDs de criterio duplicados.')
        nombres.add(nombre)
        estado = criterio.get('estado')
        if estado not in ('cumplido', 'pendiente', 'fallido'):
            raise ValueError('Estado de criterio desconocido.')
        if estado != 'cumplido':
            pendientes.append(nombre)
            continue
        evidencias = criterio.get('evidencias')
        if not isinstance(evidencias, list) or not evidencias:
            raise ValueError(f'{nombre}: falta evidencia local.')
        for evidencia in evidencias:
            comprobar_archivo(evidencia, raiz)
    artefactos = datos.get('artefactos', [])
    if not isinstance(artefactos, list):
        raise ValueError('Artefactos inválidos.')
    for artefacto in artefactos:
        comprobar_archivo(artefacto, raiz)
    for campo in ('riesgos', 'skills'):
        if not isinstance(datos.get(campo), list) or any(not isinstance(x, str) for x in datos[campo]):
            raise ValueError(f'{campo}: se requiere una lista de textos.')
    if datos.get('estado') == 'completado' and pendientes:
        raise ValueError('No se puede declarar completado con criterios pendientes o fallidos.')
    return {'proyecto': datos['proyecto'], 'tarea': datos['tarea'],
            'aprobado': datos['estado'] == 'completado' and not pendientes,
            'pendientes': pendientes, 'duracion_minutos': (fin-inicio).total_seconds()/60,
            'retrabajo_minutos': datos['retrabajo_minutos'], 'costo': costos,
            'limite': 'Comprueba estructura e integridad local. No demuestra veracidad, calidad semántica ni autorización para publicar.'}


def cargar(archivo):
    return json.loads(Path(archivo).read_text(encoding='utf-8'))


def metricas(archivos, raiz):
    registros = [evaluar(cargar(p), raiz) for p in archivos]
    ids = [(r['proyecto'], r['tarea']) for r in registros]
    if len(set(ids)) != len(ids):
        raise ValueError('Entregas duplicadas: usar solo la revisión actual de cada tarea.')
    costos = {}
    for r in registros:
        if r['costo'] is not None:
            c = r['costo']; costos[c['moneda']] = costos.get(c['moneda'], 0) + c['importe']
    return {'muestra': len(registros), 'completadas': sum(r['aprobado'] for r in registros),
            'duracion_mediana_minutos': statistics.median(r['duracion_minutos'] for r in registros) if registros else None,
            'retrabajo_minutos': sum(r['retrabajo_minutos'] for r in registros),
            'costos_declarados_por_moneda': costos,
            'entregas_sin_costo': sum(r['costo'] is None for r in registros),
            'limite': 'Datos declarados por los responsables; duración transcurrida, no horas facturables. Sin conversión de monedas ni certificación externa.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('accion', choices=('evaluar', 'metricas'))
    parser.add_argument('informes', nargs='+')
    parser.add_argument('--raiz-entrega', required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.accion == 'evaluar':
            if len(args.informes) != 1:
                raise ValueError('Evaluar acepta un solo informe.')
            resultado = evaluar(cargar(args.informes[0]), args.raiz_entrega)
        else:
            resultado = metricas(args.informes, args.raiz_entrega)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        return 0 if args.accion == 'metricas' or resultado['aprobado'] else 2
    except (ValueError, OSError, TypeError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
