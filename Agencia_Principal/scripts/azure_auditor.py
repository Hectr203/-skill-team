#!/usr/bin/env python3
"""Inventario local de dependencias para evaluar un despliegue; no aprovisiona Azure."""
import argparse
import json
from pathlib import Path


def detect_technologies(cwd):
    raiz = Path(cwd).resolve()
    if not raiz.is_dir():
        raise ValueError('Directorio de proyecto inexistente.')
    resultado = {'raiz': str(raiz), 'manifiestos': {}, 'advertencia': 'Las dependencias declaradas no demuestran arquitectura, funcionamiento ni proveedor de base de datos.'}
    for relativo in ('package.json','frontend/package.json','backend/package.json','composer.json','pyproject.toml','go.mod'):
        archivo = raiz / relativo
        if not archivo.exists():
            continue
        if archivo.resolve() != archivo:
            raise ValueError('Un manifiesto no puede redirigirse fuera del proyecto.')
        if archivo.suffix == '.json':
            datos = json.loads(archivo.read_text(encoding='utf-8'))
            if not isinstance(datos, dict):
                raise ValueError(f'Manifiesto inválido: {relativo}')
            resultado['manifiestos'][relativo] = {'dependencias': datos.get('dependencies', {}), 'desarrollo': datos.get('devDependencies', {}), 'require': datos.get('require', {})}
        else:
            resultado['manifiestos'][relativo] = {'presente': True, 'revision': 'Consultar con herramientas del ecosistema; no se infiere proveedor cloud.'}
    return resultado


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('proyecto', nargs='?', default='.')
    args = parser.parse_args()
    try:
        print(json.dumps(detect_technologies(args.proyecto), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as exc:
        print(str(exc))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
