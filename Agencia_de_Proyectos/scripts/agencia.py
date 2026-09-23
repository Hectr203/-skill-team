#!/usr/bin/env python3
"""
CLI Unificado — Agencia de Proyectos (Estándar Élite 11/10).

Proporciona un punto de entrada centralizado para todas las operaciones de la agencia:
- Diagnóstico del entorno (doctor)
- Creación de proyectos (nuevo)
- Carga de memoria y Context Engine (arranque)
- Registro de tareas y cierre trazable (cierre)
- Dashboard de estado de proyectos (estado)
- Validación estructural completa (validar)

Uso:
    python3 scripts/agencia.py doctor
    python3 scripts/agencia.py nuevo mi-proyecto --tipo nuevo
    python3 scripts/agencia.py arranque mi-proyecto [--json] [--prime]
    python3 scripts/agencia.py cierre mi-proyecto --tareas "Endpoints implementados" --notificar
    python3 scripts/agencia.py estado
    python3 scripts/agencia.py validar
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Agregar directorio scripts al sys.path
SCRIPT_DIR = Path(__file__).parent.resolve()
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# Colores ANSI
VERDE = "\033[92m"
AMARILLO = "\033[93m"
AZUL = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def cmd_doctor(args: argparse.Namespace) -> int:
    from doctor import Doctor
    doc = Doctor(verbose=args.verbose)
    return doc.ejecutar()


def cmd_nuevo(args: argparse.Namespace) -> int:
    from nuevo_proyecto import crear_proyecto
    crear_proyecto(nombre=args.nombre, cliente=args.cliente, tipo=args.tipo)
    return 0


def cmd_arranque(args: argparse.Namespace) -> int:
    from arranque import ejecutar_arranque
    ejecutar_arranque(
        proyecto_arg=args.proyecto or None,
        formato_json=args.json,
        formato_prime=args.prime,
    )
    return 0


def cmd_cierre(args: argparse.Namespace) -> int:
    from cierre import ejecutar_cierre
    ejecutar_cierre(args)
    return 0


def cmd_validar(args: argparse.Namespace) -> int:
    import subprocess
    script_validar = SCRIPT_DIR / "validar_agencia.py"
    res = subprocess.run([sys.executable, str(script_validar)], text=True, capture_output=True)
    if res.stdout:
        print(res.stdout, end="")
    if res.stderr:
        print(res.stderr, end="", file=sys.stderr)
    return res.returncode


def cmd_estado(args: argparse.Namespace) -> int:
    from arranque import estimar_tokens, inspeccionar_git, rutas_memoria
    raiz_agencia = SCRIPT_DIR.parent
    raiz_proyectos = raiz_agencia / "contexts" / "projects"

    print(f"\n{BOLD}{AZUL}======================================================={RESET}")
    print(f"{BOLD}📊 ESTADO GENERAL DE PROYECTOS — AGENCIA DE PROYECTOS{RESET}")
    print(f"{BOLD}{AZUL}======================================================={RESET}\n")

    if not raiz_proyectos.exists():
        print("[i] Carpeta contexts/projects/ no existe aún.")
        return 0

    proyectos = sorted(
        [p for p in raiz_proyectos.iterdir() if p.is_dir() and not p.name.startswith(".")],
        key=lambda x: x.name,
    )

    if not proyectos:
        print("[i] No hay proyectos registrados en contexts/projects/.")
        print("    Crea uno con: python3 scripts/agencia.py nuevo <nombre>\n")
        return 0

    for p in proyectos:
        rutas = rutas_memoria(p)
        tiene_manifiesto = rutas["manifiesto_md"].exists()
        adrs = list(rutas["adrs"].glob("ADR-*.md")) if rutas["adrs"].exists() else []
        timeline = (rutas["base"] / "timeline.jsonl").exists() or (rutas["base"] / "cloudmem.jsonl").exists()
        
        texto_acum = ""
        if tiene_manifiesto:
            texto_acum += rutas["manifiesto_md"].read_text(encoding="utf-8")
        if rutas["memoria_md"].exists():
            texto_acum += rutas["memoria_md"].read_text(encoding="utf-8")
        tokens = estimar_tokens(texto_acum)

        git_info = inspeccionar_git(p)
        git_str = f"Git: {git_info.get('rama', 'n/a')}" if git_info.get("es_repo") else "Git: no versionado"

        print(f"  {BOLD}• {p.name:<25}{RESET}")
        print(f"    ├─ Manifiesto: {'✓' if tiene_manifiesto else '○ ausente'} | ADRs: {len(adrs)} | Timeline: {'✓' if timeline else '○ vacío'}")
        print(f"    ├─ FinOps:     ~{tokens} tokens estimados ({len(texto_acum)} caracteres)")
        print(f"    └─ Estado:     {git_str}")
        print()

    print(f"{BOLD}Total de proyectos activos:{RESET} {len(proyectos)}\n")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="agencia",
        description="CLI Centralizado de la Agencia de Proyectos (Nivel 11/10).",
    )
    subparsers = parser.add_subparsers(dest="subcomando", required=True)

    # 1. Doctor
    p_doctor = subparsers.add_parser("doctor", help="Diagnóstico preflight completo de la agencia.")
    p_doctor.add_argument("-v", "--verbose", action="store_true", help="Reporte detallado.")
    p_doctor.set_defaults(func=cmd_doctor)

    # 2. Nuevo
    p_nuevo = subparsers.add_parser("nuevo", help="Inicializa un nuevo proyecto en contexts/projects/.")
    p_nuevo.add_argument("nombre", help="Nombre o ID del proyecto (ej: mi-api, vtptransportes).")
    p_nuevo.add_argument("--cliente", default="", help="Nombre del cliente o marca asociada.")
    p_nuevo.add_argument(
        "--tipo",
        default="nuevo",
        choices=["nuevo", "existente", "auditoria", "correccion", "produccion"],
        help="Tipo de proyecto.",
    )
    p_nuevo.set_defaults(func=cmd_nuevo)

    # 3. Arranque
    p_arranque = subparsers.add_parser("arranque", help="Context Engine: carga memoria, manifiesto y ADRs.")
    p_arranque.add_argument("proyecto", nargs="?", default="", help="Nombre o coincidencia difusa del proyecto.")
    p_arranque.add_argument("--json", action="store_true", help="Salida en formato JSON estructurado.")
    p_arranque.add_argument("--prime", "--prompt", action="store_true", dest="prime", help="Genera System Primer para LLMs.")
    p_arranque.set_defaults(func=cmd_arranque)

    # 4. Cierre
    p_cierre = subparsers.add_parser("cierre", help="Registra el cierre de tarea o sesión con trazabilidad.")
    p_cierre.add_argument("proyecto", help="Nombre del proyecto.")
    p_cierre.add_argument("--tareas", required=True, help="Descripción de tareas completadas.")
    p_cierre.add_argument("--agente", default="Asistente Principal", help="Nombre del agente especialista.")
    p_cierre.add_argument("--archivos", default="", help="Archivos afectados separados por comas.")
    p_cierre.add_argument("--decisiones", default="", help="Decisiones técnicas o arquitectónicas tomadas.")
    p_cierre.add_argument("--pendientes", default="", help="Tareas pendientes para la siguiente sesión.")
    p_cierre.add_argument("--riesgos", default="", help="Riesgos detectados.")
    p_cierre.add_argument("--cloud-resumen", default="", help="Resumen para timeline estructurado.")
    p_cierre.add_argument("--tipo", default="operativo", help="Tipo de actividad.")
    p_cierre.add_argument("--notificar", action="store_true", help="Emite alertas sonoras y de escritorio.")
    p_cierre.set_defaults(func=cmd_cierre)

    # 5. Estado
    p_estado = subparsers.add_parser("estado", help="Dashboard con el estado y FinOps de todos los proyectos.")
    p_estado.set_defaults(func=cmd_estado)

    # 6. Validar
    p_validar = subparsers.add_parser("validar", help="Ejecuta la suite de validación integral (11/10).")
    p_validar.set_defaults(func=cmd_validar)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
