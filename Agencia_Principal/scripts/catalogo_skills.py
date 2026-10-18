#!/usr/bin/env python3
"""Genera entradas ligeras y únicas; conserva las fuentes y sus recursos."""
import argparse
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
PREFERIDAS = {
    "frontend-design": "skills/frontend-design/SKILL.md",
    "ahorro-contexto": "skills/ahorro-contexto/SKILL.md",
    "ui-ux-pro-max": "skills/ui-ux-pro-max/SKILL.md",
    "ponytail": "skills/ponytail/SKILL.md",
    "animation-vocabulary": "skills/emilkowalski-skills/skills/animation-vocabulary/SKILL.md",
    "emil-design-eng": "skills/emilkowalski-skills/skills/emil-design-eng/SKILL.md",
    "apple-design": "skills/design-and-motion/apple-design/SKILL.md",
}


def catalogo(raiz: Path = RAIZ) -> dict[str, Path]:
    seleccion = {}
    for archivo in sorted((raiz / "skills").rglob("SKILL.md")):
        if any(parte.startswith(".") for parte in archivo.relative_to(raiz).parts):
            continue
        coincidencia = re.search(r"^name:\s*([a-z0-9-]+)$", archivo.read_text(encoding="utf-8"), re.M)
        if not coincidencia:
            raise ValueError(f"Skill sin nombre válido: {archivo.relative_to(raiz)}")
        nombre = coincidencia[1]
        previa = seleccion.get(nombre)
        preferida = PREFERIDAS.get(nombre)
        if previa is None or str(archivo.relative_to(raiz)) == preferida:
            seleccion[nombre] = archivo
        elif str(previa.relative_to(raiz)) != preferida:
            raise ValueError(f"Dos fuentes para {nombre}: registra una selección en PREFERIDAS.")
    return dict(sorted(seleccion.items()))


def entradas_esperadas(raiz: Path = RAIZ) -> dict[Path, str]:
    entradas = {}
    fuentes = catalogo(raiz)
    for nombre, fuente in fuentes.items():
        texto = fuente.read_text(encoding="utf-8")
        descripcion = re.search(r"^description:[^\n]*(?:\n[ \t]+[^\n]*)*", texto, re.M)
        if not descripcion:
            raise ValueError(f"Skill sin descripción: {fuente.relative_to(raiz)}")
        ruta = fuente.relative_to(raiz).as_posix()
        entradas[raiz / ".agencia/skills-activos" / nombre / "SKILL.md"] = (
            f"---\nname: {nombre}\n{descripcion[0]}\n---\n\n"
            f"Entrada generada. Antes de actuar, lee la [fuente canónica](../../../{ruta}).\n"
            "Resuelve scripts, referencias y recursos desde el directorio de esa fuente.\n"
            "Aplica la precedencia de reglas de la agencia; no cargues variantes con el mismo nombre.\n"
            "Selecciona por objetivo, entradas y exclusiones conforme al [contrato común](../../../agentes/contrato-agente.md).\n"
            "Recibe la tarea concreta como contexto; no ejecuta todas las herramientas ni amplía autorización.\n"
        )
    entradas[raiz / ".agencia/catalogo-skills.json"] = json.dumps(
        {nombre: fuente.relative_to(raiz).as_posix() for nombre, fuente in fuentes.items()},
        ensure_ascii=False, indent=2,
    ) + "\n"
    return entradas


def comprobar(raiz: Path = RAIZ) -> list[str]:
    esperadas = entradas_esperadas(raiz)
    errores = [f"Entrada de skill ausente o desactualizada: {ruta.relative_to(raiz)}"
               for ruta, texto in esperadas.items()
               if not ruta.is_file() or ruta.read_text(encoding="utf-8") != texto]
    activas = set((raiz / ".agencia/skills-activos").rglob("SKILL.md"))
    errores.extend(f"Entrada activa no registrada: {p.relative_to(raiz)}" for p in activas - set(esperadas))
    return errores


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generar", action="store_true", help="Actualiza entradas generadas sin modificar fuentes.")
    argumentos = parser.parse_args()
    if argumentos.generar:
        for ruta, texto in entradas_esperadas().items():
            ruta.parent.mkdir(parents=True, exist_ok=True)
            ruta.write_text(texto, encoding="utf-8")
    errores = comprobar()
    print(f"Habilidades canónicas: {len(catalogo())}")
    for error in errores:
        print(error)
    return int(bool(errores))


if __name__ == "__main__":
    raise SystemExit(main())
