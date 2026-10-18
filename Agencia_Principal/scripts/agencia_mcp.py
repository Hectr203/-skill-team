#!/usr/bin/env python3
"""
Servidor MCP local de Agencia Principal.

Implementa el protocolo Model Context Protocol (MCP) sobre JSON-RPC 2.0 (stdio)
utilizando únicamente la biblioteca estándar de Python (cero dependencias externas).

Expone herramientas locales de contexto, integridad y descubrimiento de skills para cualquier cliente MCP (Google Antigravity IDE,
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
      "args": ["<ruta-absoluta-agencia>/scripts/agencia_mcp.py"]
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
        "description": "Context Engine: Carga la memoria, manifiesto, decisiones de arquitectura (ADRs), estado Git y presupuesto de tokens de un proyecto. Retorna contexto de referencia que no reemplaza instrucciones vigentes o el paquete JSON estructurado.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "proyecto": {
                    "type": "string",
                    "description": "Nombre o ID del proyecto (requiere ID exacto, ej: 'vtp' o 'vtptransportes').",
                },
                "formato": {
                    "type": "string",
                    "enum": ["primer", "json", "visual"],
                    "default": "primer",
                    "description": "Formato de salida: 'primer' (contexto de referencia para el modelo), 'json' (objeto estructurado), 'visual' (dashboard texto).",
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
                "stack": {"type": "string", "default": "estandar", "description": "ID de un stack registrado en stacks/."},
            },
            "required": ["nombre"],
        },
    },
    {
        "name": "agencia_validar",
        "description": "Ejecuta la suite de verificación formal de integridad de la agencia (contratos de agentes, scripts, catálogo y enlaces; no audita el contenido de las skills).",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
]

TOOLS_DEFINITIONS.extend([
    {"name": "agencia_plan", "description": "Consulta el plan local del proyecto, dependencias, revisión y vigencia de evidencias. No modifica estados ni inicia agentes; el contenido es contexto de referencia.",
     "inputSchema": {"type": "object", "properties": {"proyecto": {"type": "string"}}, "required": ["proyecto"]}},
    {"name": "agencia_skills", "description": "Lista nombres, descripciones y fuentes canónicas. El filtro textual ayuda a descubrir candidatos; no elige ni ejecuta skills.",
     "inputSchema": {"type": "object", "properties": {"consulta": {"type": "string", "default": ""}}}},
    {"name": "agencia_skill", "description": "Resuelve una skill por nombre exacto y su directorio de recursos. El agente debe leerla y comprobar aplicabilidad; no se ejecuta su procedimiento.",
     "inputSchema": {"type": "object", "properties": {"nombre": {"type": "string"}}, "required": ["nombre"]}},
])


def validar_argumentos(nombre: str, argumentos: dict) -> None:
    """Valida el contrato publicado antes de ejecutar cualquier herramienta."""
    definicion = next((item for item in TOOLS_DEFINITIONS if item["name"] == nombre), None)
    if definicion is None:
        raise ValueError("Herramienta desconocida.")
    if not isinstance(argumentos, dict):
        raise ValueError("arguments debe ser un objeto.")
    esquema = definicion["inputSchema"]
    propiedades = esquema["properties"]
    if set(argumentos) - set(propiedades):
        raise ValueError("Argumentos no reconocidos.")
    for campo in esquema.get("required", []):
        if campo not in argumentos:
            raise ValueError(f"Falta el argumento obligatorio: {campo}.")
    for campo, valor in argumentos.items():
        regla = propiedades[campo]
        tipo = regla["type"]
        if tipo == "string" and not isinstance(valor, str) or tipo == "boolean" and not isinstance(valor, bool):
            raise ValueError(f"Tipo inválido para {campo}.")
        if campo in esquema.get("required", []) and isinstance(valor, str) and not valor.strip():
            raise ValueError(f"El argumento {campo} no puede estar vacío.")
        if "enum" in regla and valor not in regla["enum"]:
            raise ValueError(f"Valor no permitido para {campo}.")


def ejecutar_herramienta(name: str, args: dict) -> tuple[str, bool]:
    """Despacha la ejecución de cada herramienta capturando la salida de forma segura."""
    f_out = io.StringIO()
    f_err = io.StringIO()
    codigo = 0

    try:
        validar_argumentos(name, args)
        with redirect_stdout(f_out), redirect_stderr(f_err):
            if name == "agencia_plan":
                from operacion_tareas import consultar
                print(json.dumps(consultar(args["proyecto"]), ensure_ascii=False, indent=2))

            elif name in ("agencia_skills", "agencia_skill"):
                from consulta_skills import listar_skills, resolver_skill
                resultado = resolver_skill(args["nombre"]) if name == "agencia_skill" else listar_skills(args.get("consulta", ""))
                print(json.dumps(resultado, ensure_ascii=False, indent=2))

            elif name == "agencia_arranque":
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
                codigo = doc.ejecutar()

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
                    stack=args.get("stack", "estandar"),
                )

            elif name == "agencia_validar":
                from agencia import cmd_validar
                import argparse
                codigo = cmd_validar(argparse.Namespace())

            else:
                return f"Error: Herramienta desconocida '{name}'.", True

    except (Exception, SystemExit) as exc:
        return f"Error al ejecutar {name}: {exc}\n{f_err.getvalue()}".strip(), True

    res = f_out.getvalue().strip()
    err = f_err.getvalue().strip()
    if codigo:
        return f"{res}\n{err}\nLa herramienta terminó con código {codigo}.".strip(), True
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
    if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0" or not isinstance(msg.get("method"), str):
        responder_jsonrpc(None, error={"code": -32600, "message": "Solicitud JSON-RPC inválida"})
        return
    method = msg.get("method")
    req_id = msg.get("id")
    if req_id is not None and type(req_id) not in (int, str):
        responder_jsonrpc(None, error={"code": -32600, "message": "ID de solicitud inválido"})
        return
    if "id" not in msg:
        return
    if not isinstance(msg.get("params", {}), dict):
        responder_jsonrpc(req_id, error={"code": -32602, "message": "params debe ser un objeto"})
        return

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
    if "id" in msg:
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
            responder_jsonrpc(None, error={"code": -32700, "message": "JSON inválido"})


if __name__ == "__main__":
    main()
