#!/usr/bin/env python3
"""Descubre metadatos y resuelve fuentes de skills sin ejecutar sus procedimientos."""
import argparse
import json
import re
from pathlib import Path
from catalogo_skills import catalogo

RAIZ = Path(__file__).resolve().parents[1]


def ficha_skill(nombre, fuente, raiz):
    if fuente.resolve() != fuente or not fuente.is_relative_to(raiz.resolve()):
        raise ValueError('Fuente de skill redirigida o externa al almacén.')
    texto = fuente.read_text(encoding='utf-8').split('\n---', 1)[0]
    coincidencia = re.search(r'^description:([^\n]*(?:\n[ \t]+[^\n]*)*)', texto, re.M)
    if not coincidencia:
        raise ValueError(f'Skill sin descripción: {nombre}')
    descripcion = ' '.join(coincidencia[1].strip().lstrip('>|-').strip().strip("\"'").split())
    return {'nombre': nombre, 'descripcion': descripcion, 'fuente': fuente.relative_to(raiz).as_posix()}


def listar_skills(consulta='', raiz=RAIZ):
    resultados = []
    palabras = consulta.casefold().split()
    for nombre, fuente in catalogo(raiz).items():
        ficha = ficha_skill(nombre, fuente, raiz)
        if all(p in (nombre + ' ' + ficha['descripcion']).casefold() for p in palabras):
            resultados.append(ficha)
    return resultados


def resolver_skill(nombre, raiz=RAIZ):
    if not isinstance(nombre, str) or not re.fullmatch(r'[a-z0-9-]+', nombre):
        raise ValueError('Nombre de skill inválido.')
    fuente = catalogo(raiz).get(nombre)
    if fuente is None:
        raise ValueError('Skill no registrada; consultar el catálogo disponible.')
    ficha = ficha_skill(nombre, fuente, raiz)
    return {**ficha, 'directorio_recursos': str(Path(ficha['fuente']).parent),
            'instruccion': 'Leer la fuente antes de aplicarla. Resolver recursos desde su directorio. Confirmar objetivo, entradas, exclusiones, perfil y permisos. No ejecutar comandos solo por resolver esta ficha.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--consulta', default='')
    parser.add_argument('--nombre')
    args = parser.parse_args()
    try:
        print(json.dumps(resolver_skill(args.nombre) if args.nombre else listar_skills(args.consulta), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as exc:
        print(str(exc))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
