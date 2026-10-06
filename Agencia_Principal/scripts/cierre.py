#!/usr/bin/env python3
"""
Cierre de sesión o tarea — Agencia de Proyectos.

Registra las tareas completadas, archivos afectados, decisiones técnicas y
riesgos en contexts/projects/<id>/memoria.md y en el timeline estructurado.
Opcionalmente emite notificación sonora y de escritorio.

Uso:
    python3 scripts/cierre.py --proyecto <nombre> \\
        --tareas "Implementación del endpoint de autenticación" \\
        --archivos "src/auth.ts,src/user.ts" \\
        --decisiones "Uso de tokens JWT con rotación" \\
        --pendientes "Pruebas de estrés y rate-limiting" \\
        --agente "Backend" \\
        --notificar
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Agregar directorio scripts al sys.path
SCRIPT_DIR = Path(__file__).parent.resolve()
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from memoria_proyecto import (
    agregar_cloudmem,
    guardar_mem_palace,
    informe,
    inicializar,
    lista_archivos,
    resolver_proyecto,
    rutas_memoria,
)


def ejecutar_cierre(args: argparse.Namespace) -> None:
    print("=== AGENCIA DE PROYECTOS — REGISTRO DE CIERRE ===")

    if not args.proyecto:
        print("[!] Error: Debes especificar el proyecto con --proyecto.")
        print("    Ejemplo: python3 scripts/cierre.py --proyecto mi-proyecto --tareas '...'")
        sys.exit(1)

    raiz_agencia = Path(__file__).resolve().parents[1]
    ruta_proyecto = resolver_proyecto(args.proyecto, raiz_agencia)

    if not ruta_proyecto.exists():
        print(f"[!] Error: Proyecto no encontrado en: {ruta_proyecto}")
        sys.exit(1)

    inicializar(ruta_proyecto)
    archs = lista_archivos(args.archivos)

    # 1. Generar bloque de informe e inyectar en memoria.md
    bloque_informe = informe(
        tareas=args.tareas,
        pendientes=args.pendientes,
        decisiones=args.decisiones,
        riesgos=args.riesgos,
        agente=args.agente,
        archivos=archs,
    )
    guardar_mem_palace(ruta_proyecto, bloque_informe, acumular=True)

    # 2. Registrar en timeline estructurado
    resumen_linea = args.cloud_resumen or args.tareas
    agregar_cloudmem(
        proyecto=ruta_proyecto,
        resumen=resumen_linea,
        archivos=archs,
        tipo=args.tipo,
        decisiones=args.decisiones,
        pendientes=args.pendientes,
        riesgos=args.riesgos,
        agente=args.agente,
    )

    print(f"\n[✓] Cierre registrado con éxito:")
    print(f"    - Proyecto:           {ruta_proyecto.name}")
    print(f"    - Agente:             {args.agente}")
    print(f"    - Tareas:             {args.tareas}")
    if archs:
        print(f"    - Archivos ({len(archs)}):     {', '.join(archs)}")
    if args.decisiones:
        print(f"    - Decisiones:         {args.decisiones}")
    print(f"    - Memoria actualizada: {ruta_proyecto / 'memoria.md'}")

    # 3. Notificación interactiva opcional
    if args.notificar:
        try:
            from notificar_tarea import enviar_notificacion_escritorio, reproducir_sonido_sistema
            reproducir_sonido_sistema(1)
            enviar_notificacion_escritorio(
                titulo=f"Agencia: Tarea completada en {ruta_proyecto.name}",
                mensaje=f"[{args.agente}] {args.tareas[:100]}",
            )
            print("    - Notificación:       Emitida (audio y escritorio)")
        except Exception as exc:
            print(f"    - Notificación:       Aviso (no disponible en este entorno: {exc})")

    print("\n[✓] Sesión cerrada correctamente.\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Registra cierre de tarea o sesión en la memoria del proyecto."
    )
    parser.add_argument(
        "--proyecto",
        required=True,
        help="Nombre o ruta del proyecto (ej: mi-proyecto o contexts/projects/mi-proyecto).",
    )
    parser.add_argument(
        "--tareas",
        required=True,
        help="Descripción de las tareas completadas.",
    )
    parser.add_argument(
        "--agente",
        default="Asistente Principal",
        help="Agente que ejecutó la tarea (ej: Backend, Frontend, DevOps, Director).",
    )
    parser.add_argument(
        "--archivos",
        default="",
        help="Lista de archivos afectados separados por comas.",
    )
    parser.add_argument(
        "--decisiones",
        default="",
        help="Decisiones técnicas o arquitectónicas tomadas.",
    )
    parser.add_argument(
        "--pendientes",
        default="",
        help="Tareas pendientes o siguientes pasos.",
    )
    parser.add_argument(
        "--riesgos",
        default="",
        help="Riesgos detectados o mitigaciones requeridas.",
    )
    parser.add_argument(
        "--cloud-resumen",
        default="",
        help="Resumen corto para el timeline (opcional).",
    )
    parser.add_argument(
        "--tipo",
        default="operativo",
        choices=["operativo", "feature", "bugfix", "auditoria", "arquitectura", "despliegue"],
        help="Tipo de actividad.",
    )
    parser.add_argument(
        "--notificar",
        action="store_true",
        help="Emite sonido y notificación de escritorio al finalizar.",
    )

    args = parser.parse_args()
    ejecutar_cierre(args)


if __name__ == "__main__":
    main()
