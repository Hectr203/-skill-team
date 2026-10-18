#!/usr/bin/env python3
"""Registra una ficha existente que cumple el contrato, sin fijar skills o tecnología."""
import argparse
import json
from pathlib import Path
from memoria_proyecto import validar_identificador, _escritura_atomica

RAIZ = Path(__file__).resolve().parents[1]


def registrar(nombre, raiz=RAIZ):
    validar_identificador(nombre)
    ficha = raiz / 'agentes' / f'{nombre}.md'
    if not ficha.is_file() or ficha.resolve() != ficha:
        raise ValueError('Ficha ausente o redirigida.')
    texto = ficha.read_text(encoding='utf-8').lower()
    for marca in ('contrato-agente.md', 'precedencia.md', 'activación', 'entradas', 'entrega', 'aceptación'):
        if marca not in texto:
            raise ValueError(f'Contrato incompleto: {marca}')
    ruta = raiz / 'reglas/rutas-agentes.json'
    if ruta.resolve() != ruta:
        raise ValueError('Registro redirigido.')
    registro = json.loads(ruta.read_text(encoding='utf-8'))
    if not isinstance(registro, dict) or registro.get('version') != 1 or not isinstance(registro.get('roles'), dict):
        raise ValueError('Registro inválido.')
    registro['roles'].setdefault(nombre, {'archivo': f'agentes/{nombre}.md', 'skills': []})
    _escritura_atomica(ruta, json.dumps(registro, ensure_ascii=False, indent=2)+'\n')
    return f'agentes/{nombre}.md'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('nombre')
    args = parser.parse_args()
    try:
        print(registrar(args.nombre))
        return 0
    except (ValueError, OSError) as exc:
        print(str(exc))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
