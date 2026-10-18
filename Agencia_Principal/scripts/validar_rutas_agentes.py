#!/usr/bin/env python3
"""Comprueba cobertura de roles y resolución segura de skills canónicas."""
import argparse
import json
from pathlib import Path
from catalogo_skills import catalogo

RAIZ = Path(__file__).resolve().parents[1]
APOYO = {'contrato-agente.md', 'guia-de-personas.md'}


def comprobar_rutas(raiz=RAIZ):
    errores = []
    registro = json.loads((raiz / 'reglas/rutas-agentes.json').read_text(encoding='utf-8'))
    if not isinstance(registro, dict):
        return ['Formato de registro de roles inválido']
    if registro.get('version') != 1 or not isinstance(registro.get('roles'), dict):
        return ['Formato de registro de roles inválido']
    fuentes = None
    existentes = {p.relative_to(raiz).as_posix() for p in (raiz / 'agentes').glob('*.md') if p.name not in APOYO}
    registrados = []
    for rol, datos in registro['roles'].items():
        if not isinstance(datos, dict):
            errores.append(f'Definición de rol inválida: {rol}')
            continue
        archivo = datos.get('archivo')
        if archivo != f'agentes/{rol}.md' or archivo not in existentes:
            errores.append(f'Archivo de rol inválido: {rol}')
            continue
        registrados.append(archivo)
        texto = (raiz / archivo).read_text(encoding='utf-8')
        for marcador in ('contrato-agente.md', 'precedencia.md', 'Activación', 'Entradas', 'Entrega', 'aceptación'):
            if marcador.lower() not in texto.lower():
                errores.append(f'Contrato de rol incompleto: {rol} ({marcador})')
        skills = datos.get('skills')
        if not isinstance(skills, list) or not all(isinstance(s, str) for s in skills):
            errores.append(f'Lista de skills inválida: {rol}')
            continue
        if len(set(skills)) != len(skills):
            errores.append(f'Skill duplicada en rol: {rol}')
        if skills and fuentes is None:
            fuentes = catalogo(raiz)
        for nombre in skills:
            if nombre not in fuentes:
                errores.append(f'Skill no resoluble: {rol}/{nombre}')
            elif f'`{nombre}`' not in texto:
                errores.append(f'Ruta sin criterio documentado: {rol}/{nombre}')
    for archivo in sorted(existentes - set(registrados)):
        errores.append(f'Rol sin registro: {archivo}')
    return errores


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    try:
        errores = comprobar_rutas()
    except (ValueError, OSError, TypeError) as exc:
        errores = [f'Registro no verificable: {exc}']
    for error in errores:
        print(error)
    print('RUTAS OK' if not errores else 'RUTAS FALLIDAS')
    return int(bool(errores))


if __name__ == '__main__':
    raise SystemExit(main())
