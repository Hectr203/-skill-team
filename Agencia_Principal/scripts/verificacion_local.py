#!/usr/bin/env python3
"""Comprobaciones locales con evidencia vinculada a los archivos verificados."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
INFORME = Path(".agencia/verificacion-local.json")
COMANDOS = [["scripts/validar_agencia.py"], ["-m", "unittest", "discover", "-s", "tests", "-q"]]
OMITIR = {".git", "__pycache__", ".pytest_cache", ".cache", "node_modules", "dist", "build", ".memoria", "evidencias"}


def huellas(raiz: Path) -> dict[str, str]:
    resultado = {}
    for carpeta, directorios, archivos in os.walk(raiz, followlinks=False):
        directorios[:] = sorted(d for d in directorios if d not in OMITIR)
        if any((Path(carpeta) / d).is_symlink() for d in directorios):
            raise ValueError("No se verifican directorios redirigidos mediante enlaces simbólicos.")
        for nombre in sorted(archivos):
            archivo = Path(carpeta) / nombre
            relativa = archivo.relative_to(raiz)
            privado = nombre.startswith(".env") and nombre != ".env.example"
            if relativa == INFORME or privado or archivo.suffix in (".key", ".enc", ".pyc", ".log") or nombre.startswith(".hitl_"):
                continue
            if archivo.is_symlink():
                raise ValueError("No se verifican archivos redirigidos mediante enlaces simbólicos.")
            resultado[relativa.as_posix()] = hashlib.sha256(archivo.read_bytes()).hexdigest()
    return resultado


def ruta_informe(raiz):
    destino = raiz / INFORME
    if destino.resolve() != destino:
        raise ValueError("El informe o su directorio no pueden redirigirse.")
    return destino


def verificar(raiz: Path = RAIZ) -> int:
    destino = ruta_informe(raiz)
    antes = huellas(raiz)
    resultados = []
    for argumentos in COMANDOS:
        try:
            proceso = subprocess.run([sys.executable, *argumentos], cwd=raiz, capture_output=True, text=True, timeout=120)
            resultados.append({"argumentos": argumentos, "codigo": proceso.returncode,
                               "stdout": proceso.stdout, "stderr": proceso.stderr})
        except (OSError, subprocess.TimeoutExpired):
            resultados.append({"argumentos": argumentos, "codigo": 1, "stdout": "", "stderr": "La comprobación no pudo completarse."})
    estable = antes == huellas(raiz)
    aprobado = estable and all(resultado["codigo"] == 0 for resultado in resultados)
    datos = {"version": 1, "fecha_utc": datetime.now(timezone.utc).isoformat(),
             "aprobado": aprobado, "contenido_estable": estable,
             "huellas": antes, "resultados": resultados}
    destino.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=destino.parent, delete=False) as temporal:
        json.dump(datos, temporal, ensure_ascii=False, indent=2)
        temporal.write("\n")
        nombre_temporal = temporal.name
    os.replace(nombre_temporal, destino)
    print("VERIFICACIÓN LOCAL APROBADA" if aprobado else "VERIFICACIÓN LOCAL FALLIDA")
    for resultado in resultados:
        print(f"{' '.join(resultado['argumentos'])}: código {resultado['codigo']}")
    if not estable:
        print("Los archivos cambiaron durante las comprobaciones; el resultado no es válido.")
    return 0 if aprobado else 1


def comprobar(raiz: Path = RAIZ) -> int:
    try:
        datos = json.loads(ruta_informe(raiz).read_text(encoding="utf-8"))
        resultados = datos["resultados"]
        valido = (type(datos["version"]) is int and datos["version"] == 1 and datos["aprobado"] is True and datos["contenido_estable"] is True
                  and [r["argumentos"] for r in resultados] == COMANDOS
                  and all(type(r["codigo"]) is int and r["codigo"] == 0 for r in resultados)
                  and datos["huellas"] == huellas(raiz))
    except (OSError, ValueError, KeyError, TypeError):
        valido = False
    print("EVIDENCIA LOCAL VIGENTE" if valido else "EVIDENCIA AUSENTE, FALLIDA O DESACTUALIZADA: ejecutar verificar.")
    return 0 if valido else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("accion", choices=["verificar", "comprobar"])
    argumentos = parser.parse_args()
    try:
        return verificar() if argumentos.accion == "verificar" else comprobar()
    except (OSError, ValueError) as exc:
        print(f"No se pudo verificar: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
