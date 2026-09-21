"""
Arranque de memoria persistente — Agencia Universal para Proyectos Existentes.

Uso:
    python3 scripts/arranque.py --proyecto proyectos/<nombre>
    python3 scripts/arranque.py  (lista proyectos disponibles)
"""

import argparse
import os
import sys
from pathlib import Path


def _agregar_ruta_scripts() -> None:
    """Asegura que el directorio scripts/ esté en sys.path para importar memoria_proyecto."""
    directorio = Path(__file__).parent.resolve()
    ruta = str(directorio)
    if ruta not in sys.path:
        sys.path.insert(0, ruta)


def _listar_proyectos(raiz_proyectos: Path) -> list[Path]:
    """Devuelve subdirectorios de proyectos/ que no sean la plantilla."""
    if not raiz_proyectos.exists():
        return []
    return sorted(
        p for p in raiz_proyectos.iterdir()
        if p.is_dir() and p.name != "_plantilla_proyecto"
    )


def ejecutar_arranque(proyecto: str | None = None) -> None:
    print("=== AGENCIA PROYECTOS EXISTENTES — MEMORIA (ARRANQUE) ===")

    # Determinar raíz de la agencia (un nivel arriba de scripts/)
    raiz_agencia = Path(__file__).parent.parent.resolve()
    raiz_proyectos = raiz_agencia / "proyectos"

    if not proyecto:
        proyectos = _listar_proyectos(raiz_proyectos)
        if proyectos:
            print("\n[i] Proyectos disponibles (especifica uno con --proyecto):")
            for p in proyectos:
                tiene_memoria = (p / ".memoria" / "mem_palace.enc").exists()
                estado = "✓ con memoria" if tiene_memoria else "○ sin memoria inicializada"
                print(f"    - {p.name}  [{estado}]")
        else:
            print("\n[i] No hay proyectos en proyectos/. Crea uno con:")
            print("    python3 scripts/nuevo_proyecto.py <nombre-proyecto>")
        print("\n[!] Especifica un proyecto para ver su memoria:")
        print("    python3 scripts/arranque.py --proyecto proyectos/<nombre>")
        return

    _agregar_ruta_scripts()

    try:
        from memoria_proyecto import (  # type: ignore[import]
            imprimir_cloudmem,
            leer_cloudmem,
            leer_mem_palace,
            resolver_proyecto,
        )
    except ImportError as exc:
        print(f"[!] No se pudo importar memoria_proyecto: {exc}")
        sys.exit(1)

    # Resolver la ruta: puede ser relativa a la raíz de la agencia o absoluta
    ruta_proyecto = Path(proyecto)
    if not ruta_proyecto.is_absolute():
        ruta_proyecto = raiz_agencia / ruta_proyecto
    ruta_proyecto = ruta_proyecto.resolve()

    if not ruta_proyecto.exists():
        print(f"[!] Proyecto no encontrado: {ruta_proyecto}")
        print("    Crea el proyecto con: python3 scripts/nuevo_proyecto.py <nombre>")
        sys.exit(1)

    print(f"\n[+] Proyecto: {ruta_proyecto.name}")
    print(f"    Ruta:     {ruta_proyecto}")

    tiene_memoria = (ruta_proyecto / ".memoria" / "mem_palace.enc").exists()
    if not tiene_memoria:
        print("\n[!] Este proyecto no tiene memoria inicializada. Ejecuta:")
        print(f"    python3 scripts/memoria_proyecto.py --proyecto {proyecto} init")
        return

    contexto = leer_mem_palace(ruta_proyecto)
    if contexto:
        print("\n--- MEM PALACE DEL PROYECTO ---")
        print(contexto)
        print("--------------------------------")
    else:
        print("\n[i] Mem Palace del proyecto no tiene entradas aún.")

    imprimir_cloudmem(leer_cloudmem(ruta_proyecto, limite=8))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Arranque de memoria persistente por proyecto."
    )
    parser.add_argument(
        "--proyecto",
        default="",
        help="Ruta del proyecto (relativa a la agencia o absoluta). "
             "Ejemplo: proyectos/mi-proyecto",
    )
    args = parser.parse_args()
    ejecutar_arranque(args.proyecto or None)
