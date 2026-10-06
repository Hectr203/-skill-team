#!/usr/bin/env python3
"""
Servidor MCP Nativo — Agencia de Proyectos (Estándar Élite 11/10).

Implementa el protocolo Model Context Protocol (MCP) sobre JSON-RPC 2.0 (stdio)
utilizando únicamente la biblioteca estándar de Python (cero dependencias externas).

Expone 6 herramientas nativas para cualquier cliente MCP (Google Antigravity IDE,
Claude Code, Cursor, OpenCode):
- agencia_arranque: Context Engine y recuperación de memoria/ADRs/FinOps.
- agencia_cierre: Registro de tareas, decisiones y cierre de sesión.
- agencia_doctor: Diagnóstico integral preflight del entorno.
- agencia_estado: Dashboard de proyectos y control de tokens.
- agencia_nuevo: Inicialización de proyectos en contexts/projects/.
- agencia_validar: Suite de verificación de integridad formal.

Uso en configuración MCP:
    "agencia": {
      "command": "python3",
      "args": ["/mnt/nvme/skill-team/Agencia_de_Proyectos/scripts/agencia_mcp.py"]
    }
"""
from __future__ import annotations

import io
import json
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

# Agregar directorio scripts al sys.path
SCRIPT_DIR = Path(__file__).parent.resolve()
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# Definición de herramientas MCP
TOOLS_DEFINITIONS = [
    {
        "name": "agencia_arranque",
        "description": "Context Engine: Carga la memoria, manifiesto, decisiones de arquitectura (ADRs), estado Git y presupuesto de tokens de un proyecto. Retorna el System Primer formateado listo para inyectar al LLM o el paquete JSON estructurado.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "proyecto": {
                    "type": "string",
                    "description": "Nombre o ID del proyecto (admite búsqueda difusa, ej: 'vtp' o 'vtptransportes').",
                },
                "formato": {
                    "type": "string",
                    "enum": ["primer", "json", "visual"],
                    "default": "primer",
                    "description": "Formato de salida: 'primer' (System Prompt para LLM), 'json' (objeto estructurado), 'visual' (dashboard texto).",
                },
            },
            "required": ["proyecto"],
        },
    },
    {
        "name": "agencia_cierre",
        "description": "Registra el cierre de una tarea o sesión en contexts/projects/<id>/memoria.md y en el timeline estructurado, asociando agente, tareas, decisiones técnicas y riesgos.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "proyecto": {
                    "type": "string",
                    "description": "Nombre o ID del proyecto.",
                },
                "tareas": {
                    "type": "string",
                    "description": "Descripción detallada de las tareas completadas.",
                },
                "agente": {
                    "type": "string",
                    "default": "Asistente Principal",
                    "description": "Nombre del agente especialista que realizó el trabajo (ej: Backend, Frontend, Arquitecto).",
                },
                "archivos": {
                    "type": "string",
                    "default": "",
                    "description": "Lista de archivos modificados o creados separados por comas.",
                },
                "decisiones": {
                    "type": "string",
                    "default": "",
                    "description": "Decisiones técnicas o arquitectónicas adoptadas.",
                },
                "pendientes": {
                    "type": "string",
                    "default": "",
                    "description": "Siguientes pasos o tareas pendientes.",
                },
                "riesgos": {
                    "type": "string",
                    "default": "",
                    "description": "Riesgos detectados o mitigaciones requeridas.",
                },
                "tipo": {
                    "type": "string",
                    "enum": ["operativo", "feature", "bugfix", "auditoria", "arquitectura", "despliegue"],
                    "default": "operativo",
                    "description": "Tipo de actividad.",
                },
            },
            "required": ["proyecto", "tareas"],
        },
    },
    {
        "name": "agencia_doctor",
        "description": "Ejecuta un diagnóstico exhaustivo de salud del entorno de la agencia (Python, Node.js, Git, reproductores, MCPs, contextos, agentes y plantillas).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "verbose": {
                    "type": "boolean",
                    "default": False,
                    "description": "Si es True, incluye detalles exhaustivos de cada comprobación.",
                },
            },
        },
    },
    {
        "name": "agencia_estado",
        "description": "Devuelve el dashboard de todos los proyectos activos en contexts/projects/, incluyendo estado de manifiesto, número de ADRs, presupuesto de tokens estimados (FinOps) y estado Git.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "agencia_nuevo",
        "description": "Inicializa un nuevo proyecto estructurado en contexts/projects/<nombre> con manifiesto.md, memoria.md, directorio adrs/ y carpeta de evidencias.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "nombre": {
                    "type": "string",
                    "description": "Nombre o identificador único del proyecto (sin espacios ni caracteres especiales).",
                },
                "cliente": {
                    "type": "string",
                    "default": "",
                    "description": "Nombre del cliente o marca asociada.",
                },
                "tipo": {
                    "type": "string",
                    "enum": ["nuevo", "existente", "auditoria", "correccion", "produccion"],
                    "default": "nuevo",
                    "description": "Tipo de flujo o naturaleza del proyecto.",
                },
            },
            "required": ["nombre"],
        },
    },
    {
        "name": "agencia_validar",
        "description": "Ejecuta la suite de verificación formal de integridad de la agencia (78 skills, 16 agentes, scripts operativos, audios y enlaces sin roturas).",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
]


def ejecutar_herramienta(name: str, args: dict) -> tuple[str, bool]:
    """Despacha la ejecución de cada herramienta capturando la salida de forma segura."""
    f_out = io.StringIO()
    f_err = io.StringIO()

    try:
        with redirect_stdout(f_out), redirect_stderr(f_err):
            if name == "agencia_arranque":
                from arranque import ejecutar_arranque
                formato = args.get("formato", "primer")
                ejecutar_arranque(
                    proyecto_arg=args.get("proyecto"),
                    formato_json=(formato == "json"),
                    formato_prime=(formato == "primer"),
                )

            elif name == "agencia_cierre":
                from cierre import ejecutar_cierre
                import argparse
                ns = argparse.Namespace(
                    proyecto=args.get("proyecto"),
                    tareas=args.get("tareas"),
                    agente=args.get("agente", "Asistente Principal"),
                    archivos=args.get("archivos", ""),
                    decisiones=args.get("decisiones", ""),
                    pendientes=args.get("pendientes", ""),
                    riesgos=args.get("riesgos", ""),
                    cloud_resumen=args.get("cloud_resumen", ""),
                    tipo=args.get("tipo", "operativo"),
                    notificar=False,
                )
                ejecutar_cierre(ns)

            elif name == "agencia_doctor":
                from doctor import Doctor
                doc = Doctor(verbose=args.get("verbose", False))
                doc.ejecutar()

            elif name == "agencia_estado":
                from agencia import cmd_estado
                import argparse
                cmd_estado(argparse.Namespace())

            elif name == "agencia_nuevo":
                from nuevo_proyecto import crear_proyecto
                crear_proyecto(
                    nombre=args.get("nombre"),
                    cliente=args.get("cliente", ""),
                    tipo=args.get("tipo", "nuevo"),
                )

            elif name == "agencia_validar":
                from agencia import cmd_validar
                import argparse
                cmd_validar(argparse.Namespace())

            else:
                return f"Error: Herramienta desconocida '{name}'.", True

    except (Exception, SystemExit) as exc:
        return f"Error al ejecutar {name}: {exc}\n{f_err.getvalue()}".strip(), True

    res = f_out.getvalue().strip()
    err = f_err.getvalue().strip()
    if err and not res:
        return f"Aviso/Error: {err}", True
    return res, False


def responder_jsonrpc(id_req, result=None, error=None):
    resp = {"jsonrpc": "2.0", "id": id_req}
    if error is not None:
        resp["error"] = error
    else:
        resp["result"] = result
    linea = json.dumps(resp, ensure_ascii=False)
    sys.stdout.write(linea + "\n")
    sys.stdout.flush()


def procesar_mensaje(msg: dict):
    method = msg.get("method")
    req_id = msg.get("id")

    # 1. initialize
    if method == "initialize":
        responder_jsonrpc(
            req_id,
            result={
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {"listChanged": False},
                },
                "serverInfo": {
                    "name": "agencia-mcp",
                    "version": "1.0.0",
                },
            },
        )
        return

    # 2. notifications/initialized
    if method == "notifications/initialized":
        # Las notificaciones no requieren respuesta
        return

    # 3. ping
    if method == "ping":
        responder_jsonrpc(req_id, result={})
        return

    # 4. tools/list
    if method == "tools/list":
        responder_jsonrpc(req_id, result={"tools": TOOLS_DEFINITIONS})
        return

    # 5. tools/call
    if method == "tools/call":
        params = msg.get("params", {})
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})
        if not isinstance(tool_args, dict):
            responder_jsonrpc(req_id, error={"code": -32602, "message": "arguments debe ser un objeto"})
            return
        texto_resultado, is_error = ejecutar_herramienta(tool_name, tool_args)
        responder_jsonrpc(
            req_id,
            result={
                "isError": is_error,
                "content": [
                    {
                        "type": "text",
                        "text": texto_resultado,
                    }
                ]
            },
        )
        return

    # Método no soportado
    if req_id is not None:
        responder_jsonrpc(
            req_id,
            error={"code": -32601, "message": f"Método no soportado: {method}"},
        )


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Servidor MCP Nativo para la Agencia de Proyectos (JSON-RPC 2.0 stdio).")
        print("Uso: python3 scripts/agencia_mcp.py")
        sys.exit(0)

    # Bucle principal de lectura JSON-RPC línea a línea por stdin
    for linea in sys.stdin:
        linea = linea.strip()
        if not linea:
            continue
        try:
            msg = json.loads(linea)
            procesar_mensaje(msg)
        except json.JSONDecodeError as exc:
            # Enviar error de parseo si es posible
            sys.stderr.write(f"[agencia_mcp] Error decodificando JSON: {exc}\n")
            sys.stderr.flush()


if __name__ == "__main__":
    main()
