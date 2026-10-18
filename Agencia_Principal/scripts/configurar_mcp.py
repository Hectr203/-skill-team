#!/usr/bin/env python3
"""Genera configuración local para este checkout; no instala ni conecta servidores."""
import argparse
import json
import sys
from pathlib import Path


def configuracion(raiz, formato='generico'):
    raiz = Path(raiz).resolve()
    script = raiz / 'scripts/agencia_mcp.py'
    if not script.is_file():
        raise ValueError('No se encuentra el servidor de la agencia.')
    comando = [sys.executable, str(script)]
    if formato == 'opencode':
        return {'mcp': {'agencia': {'type': 'local', 'command': comando, 'enabled': True}},
                'skills': {'paths': [str(raiz / '.agencia/skills-activos')]}}
    if formato != 'generico':
        raise ValueError('Formato no soportado.')
    return {'mcpServers': {'agencia': {'command': comando[0], 'args': comando[1:]}}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--formato', choices=['generico','opencode'], default='generico')
    parser.add_argument('--salida', type=Path)
    args = parser.parse_args()
    try:
        texto = json.dumps(configuracion(Path(__file__).resolve().parents[1], args.formato), ensure_ascii=False, indent=2)+'\n'
        if args.salida:
            if args.salida.exists():
                raise ValueError('La salida existe; conservarla y combinar el fragmento manualmente.')
            with args.salida.open('x', encoding='utf-8') as archivo:
                archivo.write(texto)
        else:
            print(texto, end='')
        return 0
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
