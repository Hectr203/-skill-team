#!/usr/bin/env python3
"""
Cierre de sesión o tarea — Agencia de Proyectos.

Registra las tareas completadas, archivos afectados, decisiones técnicas y
riesgos en contexts/projects/<id>/memoria.md y en el timeline estructurado.
Opcionalmente emite notificación sonora y de escritorio.

Uso:
    python3 scripts/cierre.py --proyecto <nombre> \\
        --tareas "Implementación del endpoint de autenticación" \\
        --archivos "archivos/del/proyecto" \\
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
    bloqueo_proyecto,
    generar_evento_id,
    guardar_mem_palace,
    informe,
    inicializar,
    lista_archivos,
    resolver_proyecto,
    rotar_memoria,
    rutas_memoria,
)


def ejecutar_cierre(args: argparse.Namespace, raiz_agencia: Path | None = None) -> None:
    print("=== AGENCIA DE PROYECTOS — REGISTRO DE CIERRE ===")

    if not args.proyecto:
        print("[!] Error: Debes especificar el proyecto con --proyecto.")
        print("    Ejemplo: python3 scripts/cierre.py --proyecto mi-proyecto --tareas '...'")
        sys.exit(1)

    raiz = raiz_agencia or Path(__file__).resolve().parents[1]
    ruta_proyecto = resolver_proyecto(args.proyecto, raiz)

    if not ruta_proyecto.exists():
        print(f"[!] Error: Proyecto no encontrado en: {ruta_proyecto}")
        sys.exit(1)

    rutas = inicializar(ruta_proyecto)
    archs = lista_archivos(args.archivos)
    resueltos = lista_archivos(getattr(args, "resolver_pendientes", ""))
    max_ses = getattr(args, "max_sesiones", 5)

    ev_id = generar_evento_id(agente=args.agente, tareas=args.tareas)

    # Transacción atómica unificada bajo bloqueo exclusivo
    with bloqueo_proyecto(rutas["base"]):
        # 1. Registrar primero de forma durable en el timeline estructurado
        resumen_linea = getattr(args, "cloud_resumen", "") or args.tareas
        agregar_cloudmem(
            proyecto=ruta_proyecto,
            resumen=resumen_linea,
            archivos=archs,
            tipo=getattr(args, "tipo", "operativo"),
            decisiones=args.decisiones,
            pendientes=args.pendientes,
            riesgos=args.riesgos,
            agente=args.agente,
            evento_id=ev_id,
            pendientes_resueltos=resueltos,
        )

        # 2. Generar bloque de informe e inyectar en memoria.md
        bloque_informe = informe(
            tareas=args.tareas,
            pendientes=args.pendientes,
            decisiones=args.decisiones,
            riesgos=args.riesgos,
            agente=args.agente,
            archivos=archs,
            evento_id=ev_id,
        )
        guardar_mem_palace(ruta_proyecto, bloque_informe, acumular=True)

        # 3. Compactar sesiones excedentes manteniendo ventana deslizante
        rotar_memoria(ruta_proyecto, max_sesiones=max_ses, pendientes_resueltos=resueltos)

    print(f"\n[✓] Cierre registrado con éxito:")
    print(f"    - ID Evento:          {ev_id}")
    print(f"    - Proyecto:           {ruta_proyecto.name}")
    print(f"    - Agente:             {args.agente}")
    print(f"    - Tareas:             {args.tareas}")
    if archs:
        print(f"    - Archivos ({len(archs)}):     {', '.join(archs)}")
    if args.decisiones:
        print(f"    - Decisiones:         {args.decisiones}")
    if resueltos:
        print(f"    - Pendientes resueltos: {', '.join(resueltos)}")
    print(f"    - Memoria actualizada: {ruta_proyecto / 'memoria.md'}")

    # 4. Notificación interactiva opcional
    if getattr(args, "notificar", False):
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
    parser.add_argument(
        "--resolver-pendientes",
        default="",
        help="Lista de pendientes resueltos en esta sesión separados por comas.",
    )
    parser.add_argument(
        "--max-sesiones",
        type=int,
        default=5,
        help="Límite de sesiones detalladas en la ventana deslizante (default: 5).",
    )

    args = parser.parse_args()
    ejecutar_cierre(args)


if __name__ == "__main__":
    main()
