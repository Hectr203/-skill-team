#!/usr/bin/env python3
"""
CLI de operaciones locales de Agencia Principal.

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
    crear_proyecto(nombre=args.nombre, cliente=args.cliente, tipo=args.tipo, stack=getattr(args, "stack", "estandar"))
    return 0


def cmd_arranque(args: argparse.Namespace) -> int:
    from arranque import ejecutar_arranque
    ejecutar_arranque(
        proyecto_arg=args.proyecto or None,
        formato_json=args.json,
        formato_prime=args.prime,
        modo_completo=getattr(args, "completo", False),
        presupuesto=getattr(args, "presupuesto", 4000),
        proveedor=getattr(args, "proveedor", "estandar"),
    )
    return 0


def cmd_cierre(args: argparse.Namespace) -> int:
    from cierre import ejecutar_cierre
    ejecutar_cierre(args)
    return 0


def cmd_historia(args: argparse.Namespace) -> int:
    import json
    from memoria_proyecto import recuperar_historia, resolver_proyecto
    proyecto = resolver_proyecto(args.proyecto, SCRIPT_DIR.parent)
    eventos = recuperar_historia(
        proyecto=proyecto,
        query=getattr(args, "query", ""),
        evento_id=getattr(args, "evento", ""),
        archivo=getattr(args, "archivo", ""),
        limite=getattr(args, "limite", 10),
    )
    print(json.dumps(eventos, ensure_ascii=False, indent=2))
    return 0


def cmd_reconstruir(args: argparse.Namespace) -> int:
    from memoria_proyecto import reconstruir_memoria, resolver_proyecto
    proyecto = resolver_proyecto(args.proyecto, SCRIPT_DIR.parent)
    res = reconstruir_memoria(proyecto, reparar_archivo=getattr(args, "reparar", False))
    if getattr(args, "reparar", False):
        print(f"[✓] Memoria reconstruida y reparada en: {proyecto / 'memoria.md'}")
    else:
        print(res)
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

    if raiz_proyectos.resolve() != raiz_proyectos:
        raise ValueError("El almacén de proyectos no puede redirigirse.")
    if not raiz_proyectos.exists():
        print("[i] Carpeta contexts/projects/ no existe aún.")
        return 0

    proyectos = sorted(
        [p for p in raiz_proyectos.iterdir() if p.is_dir() and not p.is_symlink() and not p.name.startswith((".", "_"))],
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


def cmd_verificacion(args: argparse.Namespace) -> int:
    from verificacion_local import verificar, comprobar
    return verificar() if args.subcomando == "verificar" else comprobar()


def cmd_skills(args):
    import json
    from consulta_skills import listar_skills, resolver_skill
    resultado = resolver_skill(args.nombre) if args.nombre else listar_skills(args.consulta)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


def cmd_registrar_agente(args):
    from registrar_agente import registrar
    print(registrar(args.nombre))
    return 0


def cmd_entregas(args):
    import json
    from control_entregas import cargar, evaluar, metricas
    if args.accion == "evaluar":
        if len(args.informes) != 1:
            raise ValueError("Evaluar acepta un solo informe.")
        resultado = evaluar(cargar(args.informes[0]), args.raiz_entrega)
    else:
        resultado = metricas(args.informes, args.raiz_entrega)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0 if args.accion == "metricas" or resultado["aprobado"] else 2


def cmd_tareas(args):
    import json
    from control_entregas import cargar
    from operacion_tareas import crear_plan, consultar, cambiar, historial_planes
    if args.accion == "crear":
        if not args.plan:
            raise ValueError("Crear requiere --plan archivo.json.")
        resultado = crear_plan(args.proyecto, cargar(args.plan), revision=args.revision)
    elif args.accion == "historial":
        resultado = historial_planes(args.proyecto)
    elif args.accion == "consultar":
        resultado = consultar(args.proyecto)
    else:
        if args.revision is None or not args.tarea or not args.estado:
            raise ValueError("Cambiar requiere --tarea, --estado y --revision.")
        resultado = cambiar(args.proyecto, args.tarea, args.estado, args.revision,
                            args.motivo, args.informe, args.raiz_entrega)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="agencia",
        description="CLI de operación local de la Agencia de Proyectos.",
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
    p_nuevo.add_argument(
        "--stack",
        default="estandar",
        help="Identificador del stack tecnológico (default: estandar, o perfil en stacks/alternativos/).",
    )
    p_nuevo.set_defaults(func=cmd_nuevo)

    # 3. Arranque
    p_arranque = subparsers.add_parser("arranque", help="Context Engine: carga memoria, manifiesto y ADRs.")
    p_arranque.add_argument("proyecto", nargs="?", default="", help="ID exacto del proyecto.")
    p_arranque.add_argument("--json", action="store_true", help="Salida en formato JSON estructurado.")
    p_arranque.add_argument("--prime", "--prompt", action="store_true", dest="prime", help="Genera System Primer para LLMs.")
    p_arranque.add_argument("--completo", action="store_true", help="Carga el historial completo sin recortar a ventana deslizante.")
    p_arranque.add_argument("--presupuesto", type=int, default=4000, help="Presupuesto máximo de tokens para contexto enfocado (default: 4000).")
    p_arranque.add_argument(
        "--proveedor",
        default="estandar",
        choices=["google", "anthropic", "openai", "deepseek", "estandar"],
        help="Proveedor de IA para estimación de tokens y optimización de prefijo KV-cache (default: estandar).",
    )
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
    p_cierre.add_argument("--resolver-pendientes", default="", help="Lista de pendientes resueltos en esta sesión separados por comas.")
    p_cierre.add_argument("--max-sesiones", type=int, default=5, help="Límite de sesiones en ventana deslizante (default: 5).")
    p_cierre.add_argument("--sustituir-decisiones", default="", help="Lista de IDs o nombres de ADRs anteriores sustituidos/obsoletos separados por comas.")
    p_cierre.set_defaults(func=cmd_cierre)

    # 4.1 Historia
    p_historia = subparsers.add_parser("historia", help="Consulta el historial completo estructurado por filtros.")
    p_historia.add_argument("proyecto", help="Nombre o ID del proyecto.")
    p_historia.add_argument("--query", default="", help="Búsqueda por texto o palabra clave.")
    p_historia.add_argument("--evento", default="", help="Filtro por ID de evento exacto.")
    p_historia.add_argument("--archivo", default="", help="Filtro por ruta de archivo afectado.")
    p_historia.add_argument("--limite", type=int, default=10, help="Cantidad máxima de eventos a recuperar (default: 10).")
    p_historia.set_defaults(func=cmd_historia)

    # 4.2 Reconstruir
    p_reconstruir = subparsers.add_parser("reconstruir", help="Reconstruye memoria.md a partir de timeline.jsonl.")
    p_reconstruir.add_argument("proyecto", help="Nombre o ID del proyecto.")
    p_reconstruir.add_argument("--reparar", action="store_true", help="Sobrescribe memoria.md con la vista reconstruida.")
    p_reconstruir.set_defaults(func=cmd_reconstruir)

    # 5. Estado
    p_estado = subparsers.add_parser("estado", help="Dashboard con el estado y FinOps de todos los proyectos.")
    p_estado.set_defaults(func=cmd_estado)

    # 6. Validar
    p_validar = subparsers.add_parser("validar", help="Ejecuta la comprobación de integridad local.")
    p_validar.set_defaults(func=cmd_validar)

    for accion, ayuda in (("verificar", "Ejecuta pruebas y guarda evidencia vinculada al contenido."),
                          ("comprobar", "Comprueba la evidencia existente sin repetir las pruebas.")):
        subparsers.add_parser(accion, help=ayuda).set_defaults(func=cmd_verificacion)

    p_skills = subparsers.add_parser("skills", help="Descubre metadatos o resuelve una skill sin ejecutarla.")
    p_skills.add_argument("--consulta", default="")
    p_skills.add_argument("--nombre")
    p_skills.set_defaults(func=cmd_skills)
    p_registrar = subparsers.add_parser("registrar-agente", help="Registra una ficha existente con contrato válido.")
    p_registrar.add_argument("nombre")
    p_registrar.set_defaults(func=cmd_registrar_agente)

    p_entregas = subparsers.add_parser("entregas", help="Comprueba entregas o calcula métricas locales sin ejecutar sus instrucciones.")
    p_entregas.add_argument("accion", choices=("evaluar", "metricas"))
    p_entregas.add_argument("informes", nargs="+")
    p_entregas.add_argument("--raiz-entrega", required=True, type=Path)
    p_entregas.set_defaults(func=cmd_entregas)

    p_tareas = subparsers.add_parser("tareas", help="Plan local transaccional; no inicia agentes.")
    p_tareas.add_argument("accion", choices=("crear", "consultar", "cambiar", "historial"))
    p_tareas.add_argument("proyecto", help="ID exacto de proyecto registrado.")
    p_tareas.add_argument("--plan", type=Path)
    p_tareas.add_argument("--tarea")
    p_tareas.add_argument("--estado", choices=("en_curso", "bloqueado", "completado", "cancelado"))
    p_tareas.add_argument("--revision", type=int)
    p_tareas.add_argument("--motivo", default="")
    p_tareas.add_argument("--informe", type=Path)
    p_tareas.add_argument("--raiz-entrega", type=Path)
    p_tareas.set_defaults(func=cmd_tareas)

    args = parser.parse_args()
    try:
        sys.exit(args.func(args))
    except (ValueError, OSError) as exc:
        print(f"Error de operación: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
