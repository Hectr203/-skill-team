"""
Cierre de memoria persistente — Agencia Universal para Proyectos Existentes.

Uso:
    python3 scripts/cierre.py --proyecto proyectos/<nombre> \\
        --tareas "Resumen de tareas" \\
        --pendientes "Pendientes" \\
        --decisiones "Decisiones tecnicas" \\
        --riesgos "Riesgos" \\
        --cloud-resumen "Resumen operativo no sensible" \\
        --archivos "archivo1.md,archivo2.md" \\
        --tipo "operativo"
"""

import argparse
import sys
from pathlib import Path


def _agregar_ruta_scripts() -> None:
    """Asegura que scripts/ esté en sys.path para importar memoria_proyecto."""
    directorio = Path(__file__).parent.resolve()
    ruta = str(directorio)
    if ruta not in sys.path:
        sys.path.insert(0, ruta)


def ejecutar_cierre(args: argparse.Namespace) -> None:
    print("=== AGENCIA PROYECTOS EXISTENTES — MEMORIA (CIERRE) ===")

    if not args.proyecto:
        print("[!] Debes especificar el proyecto con --proyecto.")
        print("    Ejemplo: python3 scripts/cierre.py --proyecto proyectos/mi-proyecto --tareas '...'")
        sys.exit(1)

    _agregar_ruta_scripts()

    try:
        from memoria_proyecto import (  # type: ignore[import]
            agregar_cloudmem,
            guardar_mem_palace,
            informe,
            inicializar,
            lista_archivos,
            resolver_proyecto,
        )
    except ImportError as exc:
        print(f"[!] No se pudo importar memoria_proyecto: {exc}")
        sys.exit(1)

    raiz_agencia = Path(__file__).parent.parent.resolve()
    ruta_proyecto = Path(args.proyecto)
    if not ruta_proyecto.is_absolute():
        ruta_proyecto = raiz_agencia / ruta_proyecto
    ruta_proyecto = ruta_proyecto.resolve()

    if not ruta_proyecto.exists():
        print(f"[!] Proyecto no encontrado: {ruta_proyecto}")
        sys.exit(1)

    tiene_memoria = (ruta_proyecto / ".memoria" / "mem_palace.enc").exists()
    if not tiene_memoria:
        print(f"[!] La memoria del proyecto no está inicializada: {ruta_proyecto}")
        print(f"    Inicialízala con: python3 scripts/memoria_proyecto.py --proyecto {args.proyecto} init")
        sys.exit(1)

    tareas = args.tareas or ""
    pendientes = args.pendientes or ""
    decisiones = args.decisiones or ""
    riesgos = args.riesgos or ""

    if not tareas:
        print("[!] El argumento --tareas es obligatorio.")
        sys.exit(1)

    guardar_mem_palace(ruta_proyecto, informe(tareas, pendientes, decisiones, riesgos))
    print(f"[+] Mem Palace actualizado: {ruta_proyecto / '.memoria' / 'mem_palace.enc'}")

    if args.cloud_resumen:
        agregar_cloudmem(
            ruta_proyecto,
            args.cloud_resumen,
            lista_archivos(args.archivos),
            args.tipo,
            decisiones,
            pendientes,
            riesgos,
        )
        print(f"[+] CloudMem actualizado: {ruta_proyecto / '.memoria' / 'cloudmem.jsonl'}")

    print(f"\n[+] Cierre registrado para: {ruta_proyecto.name}")
    print(f"    Memoria en: {ruta_proyecto / '.memoria'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Cierre de memoria persistente por proyecto."
    )
    parser.add_argument(
        "--proyecto",
        required=True,
        help="Ruta del proyecto (relativa a la agencia o absoluta). "
             "Ejemplo: proyectos/mi-proyecto",
    )
    parser.add_argument("--tareas", required=True, help="Resumen de tareas completadas.")
    parser.add_argument("--pendientes", default="", help="Tareas pendientes.")
    parser.add_argument("--decisiones", default="", help="Decisiones técnicas tomadas.")
    parser.add_argument("--riesgos", default="", help="Riesgos identificados.")
    parser.add_argument(
        "--cloud-resumen",
        default="",
        help="Resumen operativo no sensible para CloudMem (opcional).",
    )
    parser.add_argument(
        "--archivos",
        default="",
        help="Archivos modificados, separados por comas (opcional).",
    )
    parser.add_argument(
        "--tipo",
        default="operativo",
        help="Tipo de entrada CloudMem: operativo, documental, critico (default: operativo).",
    )
    ejecutar_cierre(parser.parse_args())
