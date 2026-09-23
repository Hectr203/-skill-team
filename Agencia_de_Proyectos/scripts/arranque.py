#!/usr/bin/env python3
"""
Context Engine y Arranque de Memoria — Agencia de Proyectos.

Recupera el contexto, manifiesto, decisiones (ADRs), memoria y estado Git
de un proyecto antes de iniciar cualquier trabajo o responder sobre arquitectura.

Capacidades 11/10:
- Salida JSON estructurada para subagentes y herramientas MCP (--json)
- Generación automática de Prompt Primer para LLMs (--prime / --prompt)
- Medición de presupuesto de tokens (FinOps de contexto)
- Resolución difusa de proyectos (Fuzzy Matching)
- Detección de estado del repositorio Git en vivo

Uso:
    python3 scripts/arranque.py                           (lista proyectos disponibles)
    python3 scripts/arranque.py --proyecto <nombre>       (modo visual humano)
    python3 scripts/arranque.py --proyecto <nombre> --json (modo máquina para subagentes)
    python3 scripts/arranque.py --proyecto <nombre> --prime(genera system prompt / primer)
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

# Agregar directorio scripts al sys.path
SCRIPT_DIR = Path(__file__).parent.resolve()
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from memoria_proyecto import (
    imprimir_cloudmem,
    leer_cloudmem,
    leer_mem_palace,
    leer_memoria_markdown,
    resolver_proyecto,
    rutas_memoria,
)

# Colores ANSI
VERDE = "\033[92m"
AMARILLO = "\033[93m"
AZUL = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def estimar_tokens(texto: str) -> int:
    """Estima tokens con heurística cl100k/GPT (~3.8 caracteres por token en código/markdown)."""
    if not texto:
        return 0
    return max(1, int(len(texto) / 3.8))


def inspeccionar_git(ruta: Path) -> dict[str, str | bool]:
    """Detecta estado de Git en el proyecto o directorio padre de forma segura."""
    git_bin = shutil.which("git")
    if not git_bin:
        return {"disponible": False}

    # Buscar .git en el proyecto o hacia arriba
    repo_root: Path | None = None
    cur = ruta.resolve()
    while cur != cur.parent:
        if (cur / ".git").exists():
            repo_root = cur
            break
        cur = cur.parent

    if not repo_root:
        return {"disponible": False, "es_repo": False}

    info: dict[str, str | bool] = {"disponible": True, "es_repo": True, "raiz": str(repo_root)}
    try:
        # Rama activa
        res_branch = subprocess.run(
            [git_bin, "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=2,
        )
        if res_branch.returncode == 0:
            info["rama"] = res_branch.stdout.strip()

        # Último commit SHA
        res_sha = subprocess.run(
            [git_bin, "rev-parse", "--short", "HEAD"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=2,
        )
        if res_sha.returncode == 0:
            info["commit"] = res_sha.stdout.strip()

        # Estado del árbol de trabajo (limpio vs cambios pendientes)
        res_status = subprocess.run(
            [git_bin, "status", "--porcelain"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=2,
        )
        if res_status.returncode == 0:
            cambios = [l for l in res_status.stdout.splitlines() if l.strip()]
            info["limpio"] = len(cambios) == 0
            info["archivos_modificados"] = len(cambios)
    except Exception:
        pass

    return info


def resolver_proyecto_fuzzy(nombre_o_ruta: str, raiz_agencia: Path) -> Path | None:
    """Resuelve un proyecto admitiendo coincidencia exacta, nombres cortos o búsqueda difusa."""
    raiz_proyectos = raiz_agencia / "contexts" / "projects"

    # 1. Intento por ruta directa
    candidato = resolver_proyecto(nombre_o_ruta, raiz_agencia)
    if candidato.exists() and candidato.is_dir():
        return candidato

    if not raiz_proyectos.exists():
        return None

    proyectos_existentes = [p for p in raiz_proyectos.iterdir() if p.is_dir() and not p.name.startswith(".")]

    query = nombre_o_ruta.strip().lower()

    # 2. Coincidencia exacta sin importar mayúsculas
    for p in proyectos_existentes:
        if p.name.lower() == query:
            return p

    # 3. Coincidencia como prefijo o sufijo
    candidatos = [p for p in proyectos_existentes if p.name.lower().startswith(query) or p.name.lower().endswith(query)]
    if len(candidatos) == 1:
        return candidatos[0]
    if len(candidatos) > 1:
        return None

    # 4. Coincidencia como subcadena en nombre de carpeta
    candidatos = [p for p in proyectos_existentes if query in p.name.lower()]
    if len(candidatos) == 1:
        return candidatos[0]
    if len(candidatos) > 1:
        return None

    # 5. Coincidencia por ID o título dentro del manifiesto.md
    candidatos = []
    for p in proyectos_existentes:
        manifiesto_file = p / "manifiesto.md"
        if manifiesto_file.exists():
            try:
                txt = manifiesto_file.read_text(encoding="utf-8").lower()
                # Buscar patrón - id: <query> o mención en el título
                if f"id: {query}" in txt or f"id: `{query}" in txt or query in txt[:300]:
                    candidatos.append(p)
            except Exception:
                pass

    if len(candidatos) == 1:
        return candidatos[0]

    return None


def obtener_paquete_contexto(ruta_proyecto: Path) -> dict:
    """Extrae y estructura todos los datos del proyecto en un diccionario estándar."""
    rutas = rutas_memoria(ruta_proyecto)
    
    manifiesto_raw = rutas["manifiesto_md"].read_text(encoding="utf-8") if rutas["manifiesto_md"].exists() else ""
    memoria_raw = leer_memoria_markdown(ruta_proyecto) or leer_mem_palace(ruta_proyecto)
    
    adrs: list[dict[str, str]] = []
    if rutas["adrs"].exists():
        for adr_path in sorted(rutas["adrs"].glob("ADR-*.md")):
            adrs.append({
                "archivo": adr_path.name,
                "titulo": adr_path.name.replace(".md", ""),
                "contenido": adr_path.read_text(encoding="utf-8"),
            })

    timeline = leer_cloudmem(ruta_proyecto, limite=8)
    git_info = inspeccionar_git(ruta_proyecto)

    # Cálculo de FinOps de tokens
    texto_total = manifiesto_raw + "\n" + memoria_raw + "\n" + "\n".join(a["contenido"] for a in adrs)
    tokens_estimados = estimar_tokens(texto_total)

    return {
        "proyecto_id": ruta_proyecto.name,
        "ruta_absoluta": str(ruta_proyecto.resolve()),
        "finops": {
            "tokens_estimados": tokens_estimados,
            "caracteres_totales": len(texto_total),
            "nivel_peso": "ligero (<4k tokens)" if tokens_estimados < 4000 else "medio (<16k tokens)" if tokens_estimados < 16000 else "pesado (>16k tokens)",
        },
        "git": git_info,
        "manifiesto": {
            "existe": bool(manifiesto_raw),
            "contenido": manifiesto_raw,
        },
        "memoria": {
            "existe": bool(memoria_raw),
            "contenido": memoria_raw,
        },
        "adrs": adrs,
        "timeline_reciente": timeline,
    }


def generar_primer_prompt(ctx: dict) -> str:
    """Genera un bloque de System Primer de alta fidelidad para inicializar sesiones con LLMs."""
    adrs_titulos = "\n".join(f"- `{a['archivo']}`: {a['titulo']}" for a in ctx["adrs"]) if ctx["adrs"] else "- Ninguna decisión registrada aún."
    
    git_line = ""
    if ctx["git"].get("es_repo"):
        git_line = f"\n- **Estado Git:** Rama `{ctx['git'].get('rama', 'desconocida')}` @ `{ctx['git'].get('commit', '')}` | Árbol: {'Limpio ✓' if ctx['git'].get('limpio') else 'Cambios pendientes ⚠'}"

    primer = f"""<!-- INICIO CONTEXT PRIMER: {ctx['proyecto_id']} -->
# CONTEXTO DEL PROYECTO: {ctx['proyecto_id']}
- **Ruta de Trabajo:** `{ctx['ruta_absoluta']}`
- **Presupuesto de Contexto:** ~{ctx['finops']['tokens_estimados']} tokens ({ctx['finops']['nivel_peso']}){git_line}

## Directivas Globales
1. **Regla Ponytail:** Implementa la menor solución correcta posible sin sacrificar seguridad, accesibilidad (a11y), pruebas ni manejo de errores.
2. **Brownfield First:** En código existente, preserva los patrones, convenciones y dependencias activas; no impongas reescrituras sin plan y ADR previo.
3. **Human-in-the-Loop (HITL):** Requiere confirmación humana antes de mutar producción, desplegar, usar credenciales o alterar esquemas irreversibles.
4. **Cierre Trazable:** Al terminar la tarea, registra el avance con `python3 scripts/cierre.py`.

## Manifiesto del Proyecto
```markdown
{ctx['manifiesto']['contenido'].strip() or 'Manifiesto pendiente de definición.'}
```

## Decisiones de Arquitectura Activas (ADRs)
{adrs_titulos}

## Memoria Reciente y Estado Actual
```markdown
{ctx['memoria']['contenido'].strip() or 'Sin historial previo.'}
```
<!-- FIN CONTEXT PRIMER: {ctx['proyecto_id']} -->
"""
    return primer


def ejecutar_arranque(
    proyecto_arg: str | None = None,
    formato_json: bool = False,
    formato_prime: bool = False,
) -> None:
    raiz_agencia = Path(__file__).resolve().parents[1]
    raiz_proyectos = raiz_agencia / "contexts" / "projects"

    if not proyecto_arg:
        proyectos = [p for p in raiz_proyectos.iterdir() if p.is_dir() and not p.name.startswith(".")] if raiz_proyectos.exists() else []
        if formato_json:
            salida = [
                {
                    "id": p.name,
                    "ruta": str(p),
                    "manifiesto": (p / "manifiesto.md").exists(),
                    "memoria": (p / "memoria.md").exists(),
                    "adrs_count": len(list((p / "adrs").glob("ADR-*.md"))) if (p / "adrs").exists() else 0,
                }
                for p in sorted(proyectos, key=lambda x: x.name)
            ]
            print(json.dumps({"proyectos": salida}, ensure_ascii=False, indent=2))
            return

        print("=== AGENCIA DE PROYECTOS — ARRANQUE Y MEMORIA ===")
        if proyectos:
            print("\n[i] Proyectos disponibles en contexts/projects/:")
            for p in sorted(proyectos, key=lambda x: x.name):
                tiene_manifiesto = (p / "manifiesto.md").exists()
                tiene_memoria = (p / "memoria.md").exists() or (p / ".memoria" / "timeline.jsonl").exists()
                adrs_count = len(list((p / "adrs").glob("ADR-*.md"))) if (p / "adrs").exists() else 0
                
                estado_bits = []
                if tiene_manifiesto:
                    estado_bits.append("manifiesto ✓")
                if tiene_memoria:
                    estado_bits.append("memoria ✓")
                if adrs_count:
                    estado_bits.append(f"{adrs_count} ADRs")
                
                estado_str = ", ".join(estado_bits) if estado_bits else "sin inicializar"
                print(f"    - {p.name:<25} [{estado_str}]")
        else:
            print("\n[i] No hay proyectos aún en contexts/projects/.")
            print("    Crea uno con: python3 scripts/nuevo_proyecto.py <nombre>")

        print("\n[!] Opciones de uso avanzado:")
        print("    python3 scripts/arranque.py --proyecto <nombre>          (modo visual)")
        print("    python3 scripts/arranque.py --proyecto <nombre> --json   (modo estructurado máquina)")
        print("    python3 scripts/arranque.py --proyecto <nombre> --prime  (system primer para LLM)")
        return

    # Resolución con Fuzzy Matching
    ruta_proyecto = resolver_proyecto_fuzzy(proyecto_arg, raiz_agencia)

    if not ruta_proyecto or not ruta_proyecto.exists():
        if formato_json:
            print(json.dumps({"error": f"Proyecto '{proyecto_arg}' no encontrado."}, ensure_ascii=False))
            sys.exit(1)
        print(f"\n[!] Error: Proyecto '{proyecto_arg}' no encontrado.")
        print("    Usa 'python3 scripts/arranque.py' para ver los proyectos existentes.")
        sys.exit(1)

    ctx = obtener_paquete_contexto(ruta_proyecto)

    # 1. Modo JSON estructurado (para subagentes o herramientas)
    if formato_json:
        print(json.dumps(ctx, ensure_ascii=False, indent=2))
        return

    # 2. Modo Prompt Primer (para inyección de contexto en LLMs)
    if formato_prime:
        print(generar_primer_prompt(ctx))
        return

    # 3. Modo Visual Humano / Terminal
    print("=== AGENCIA DE PROYECTOS — ARRANQUE Y MEMORIA ===")
    print(f"\n[+] Proyecto activo: {BOLD}{ctx['proyecto_id']}{RESET}")
    print(f"    Ubicación:       {ctx['ruta_absoluta']}")
    print(f"    FinOps Tokens:   ~{ctx['finops']['tokens_estimados']} tokens {CYAN}({ctx['finops']['nivel_peso']}){RESET}")
    
    if ctx["git"].get("es_repo"):
        git_clean = f"{VERDE}Limpio ✓{RESET}" if ctx["git"].get("limpio") else f"{AMARILLO}{ctx['git'].get('archivos_modificados')} archivos modificados ⚠{RESET}"
        print(f"    Git:             Rama '{ctx['git'].get('rama')}' @ {ctx['git'].get('commit')} | {git_clean}")

    # Manifiesto
    if ctx["manifiesto"]["existe"]:
        print(f"\n{BOLD}--- MANIFIESTO DEL PROYECTO ---{RESET}")
        lineas = ctx["manifiesto"]["contenido"].splitlines()
        for linea in lineas[:15]:
            print(linea)
        if len(lineas) > 15:
            print(f"... [{len(lineas) - 15} líneas adicionales en manifiesto.md]")
        print("-------------------------------")

    # ADRs
    if ctx["adrs"]:
        print(f"\n{BOLD}--- DECISIONES DE ARQUITECTURA (ADRs) ---{RESET}")
        for adr in ctx["adrs"]:
            print(f"  • {adr['archivo']}")
        print("------------------------------------------")

    # Memoria estructurada
    if ctx["memoria"]["existe"]:
        print(f"\n{BOLD}--- MEMORIA ESTRUCTURADA (memoria.md) ---{RESET}")
        print(ctx["memoria"]["contenido"])
        print("-----------------------------------------")
    else:
        print("\n[i] El proyecto no tiene historial de memoria aún.")

    # Timeline estructurado
    imprimir_cloudmem(ctx["timeline_reciente"])
    print(f"\n{VERDE}[✓] Arranque completado. Contexto listo para la tarea.{RESET}\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Context Engine y arranque de memoria persistente por proyecto."
    )
    parser.add_argument(
        "--proyecto",
        default="",
        help="Nombre o coincidencia difusa del proyecto (ej: vtptransportes, vtp, _ejemplo_golden).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emite salida en formato JSON estructurado para herramientas y subagentes.",
    )
    parser.add_argument(
        "--prime", "--prompt",
        action="store_true",
        dest="prime",
        help="Genera un System Primer de alta fidelidad listo para inicializar un LLM.",
    )
    args = parser.parse_args()
    ejecutar_arranque(
        proyecto_arg=args.proyecto or None,
        formato_json=args.json,
        formato_prime=args.prime,
    )


if __name__ == "__main__":
    main()
