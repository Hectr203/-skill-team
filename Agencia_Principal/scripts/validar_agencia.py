#!/usr/bin/env python3
"""
Validador estructural y operativo integral para la Agencia de Proyectos.

Verifica:
1. Documentos y contratos raíz requeridos.
2. Integridad de JSON en opencode.json y configuraciones MCP.
3. Interfaz de catálogo y resolución de skills, sin auditar su contenido.
4. Contrato formal completo en las fichas de agentes.
5. Invocabilidad y sintaxis de todos los scripts operativos en scripts/ (--help).
6. Presencia de assets oficiales de alerta de escritorio en audios/.
7. Existencia y completitud del proyecto golden de referencia en contexts/projects/_ejemplo_golden/.
8. Enlaces locales de Markdown sin roturas y ausencia de secretos o carpetas vacías.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "AGENTS.md", "asistente-principal.md", "opencode.json",
    "mcp/registro-mcp.md", "mcp/mcp_config.example.json",
    "flujos/proyecto-nuevo.md", "flujos/proyecto-existente.md",
    "flujos/auditoria-seguridad.md", "flujos/produccion-growth.md",
    "flujos/correccion-urgente.md", "reglas/human-in-the-loop.md",
    "stacks/README.md", "stacks/estandar/backend.md", "stacks/estandar/frontend.md",
    "stacks/estandar/base-datos.md",
    "scripts/doctor.py", "scripts/agencia.py", "scripts/agencia_mcp.py",
]
errors: list[str] = []

# 1. Comprobación de archivos requeridos
for item in REQUIRED:
    if not (ROOT / item).is_file():
        errors.append(f"falta {item}")

# 2. Validación de JSONs de configuración
def secretos_configuracion(valor, ruta=""):
    """Señala ubicaciones de credenciales literales sin imprimir su contenido."""
    hallazgos = []
    if isinstance(valor, dict):
        for clave, contenido in valor.items():
            ubicacion = f"{ruta}.{clave}" if ruta else clave
            sensible = re.search(r"api.?key|authorization|password|secret|token", clave, re.I)
            referencia = isinstance(contenido, str) and re.fullmatch(r"\{(?:env|file):[^}]+\}|\$\{[^}]+\}", contenido)
            if sensible and contenido and not referencia and not isinstance(contenido, dict):
                hallazgos.append(ubicacion)
            hallazgos.extend(secretos_configuracion(contenido, ubicacion))
    elif isinstance(valor, list):
        for indice, contenido in enumerate(valor):
            hallazgos.extend(secretos_configuracion(contenido, f"{ruta}[{indice}]"))
    return hallazgos


for relativa in ("opencode.json", "mcp_config.json", "mcp/mcp_config.json", "mcp/mcp_config.example.json"):
    try:
        configuracion = json.loads((ROOT / relativa).read_text(encoding="utf-8"))
        for campo in secretos_configuracion(configuracion):
            errors.append(f"credencial literal: {relativa} -> {campo}")
    except (OSError, json.JSONDecodeError):
        errors.append(f"JSON ausente o inválido: {relativa}")

from catalogo_skills import comprobar
try:
    errors.extend(comprobar(ROOT))
except ValueError as exc:
    errors.append(str(exc))

# 3. El catálogo comprueba la interfaz de descubrimiento; contenido de skills fuera de alcance.
skills = list((ROOT / ".agencia/skills-activos").glob("*/SKILL.md"))

from validar_rutas_agentes import comprobar_rutas
try:
    errors.extend(comprobar_rutas(ROOT))
except (ValueError, OSError, TypeError) as exc:
    errors.append(f"rutas de agentes inválidas: {exc}")

# 4. Comprobación de agentes
agents = list((ROOT / "agentes").glob("*.md"))
if len(agents) < 12:
    errors.append("faltan agentes especializados")
for path in agents:
    text = path.read_text(encoding="utf-8").lower()
    if path.name != "contrato-agente.md" and not all(
        marker in text for marker in ("objetivo", "entradas", "entrega", "aceptación")
    ):
        errors.append(f"contrato incompleto: {path.relative_to(ROOT)}")

if "--help" in sys.argv or "-h" in sys.argv:
    print("Validador integral para Agencia de Proyectos.")
    sys.exit(0)

# 5. Comprobación de ejecución de scripts operativos con --help
scripts_py = [s for s in (ROOT / "scripts").glob("*.py") if s.name != "validar_agencia.py"]
for script in scripts_py:
    try:
        res = subprocess.run(
            [sys.executable, str(script), "--help"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if res.returncode != 0:
            errors.append(f"script falla al ejecutar --help ({script.name}): {res.stderr.strip()[:100]}")
    except Exception as exc:
        errors.append(f"error al invocar script {script.name}: {exc}")

# 6. Comprobación de audios requeridos
audios_dir = ROOT / "audios"
audios_esperados = ["Aprobación urgente..mp3", "Necesito Validación.mp3", "noti.mp3", "termine la tarea.mp3"]
for a in audios_esperados:
    if not (audios_dir / a).is_file():
        errors.append(f"audio faltante en audios/: {a}")

# 7. Comprobación de proyecto de referencia golden
golden_dir = ROOT / "contexts" / "projects" / "_ejemplo_golden"
if not (golden_dir / "manifiesto.md").is_file():
    errors.append("falta _ejemplo_golden/manifiesto.md")
if not (golden_dir / "memoria.md").is_file():
    errors.append("falta _ejemplo_golden/memoria.md")

# 8. Verificación de enlaces Markdown locales
EXCLUIDOS_VALIDACION = {"skills", "skills-activos", "mcp", "vphone-cli"}
for path in ROOT.rglob("*.md"):
    partes = path.relative_to(ROOT).parts
    if partes[0] in EXCLUIDOS_VALIDACION or "skills-activos" in partes:
        continue
    texto_md = path.read_text(encoding="utf-8")
    if "http://" in texto_md:
        errors.append(f"URL insegura http: {path.relative_to(ROOT)}")
    for target in re.findall(r"\]\(([^)#]+)(?:#[^)]+)?\)", texto_md):
        if target.startswith(("https://", "mailto:")):
            continue
        if target.startswith("file://"):
            target_path = Path(target.replace("file://", ""))
            if not target_path.exists():
                errors.append(f"enlace local inexistente: {path.relative_to(ROOT)} -> {target}")
            continue
        candidate = (path.parent / target).resolve()
        if not candidate.exists():
            errors.append(f"enlace local inexistente: {path.relative_to(ROOT)} -> {target}")

# 9. Carpetas vacías
for directory in ROOT.rglob("*"):
    partes = directory.relative_to(ROOT).parts
    if partes[0] in EXCLUIDOS_VALIDACION or "skills-activos" in partes:
        continue
    if directory.is_dir() and not any(directory.iterdir()):
        errors.append(f"directorio vacio: {directory.relative_to(ROOT)}")

# 10. Archivos prohibidos o secretos
for forbidden in (".env", ".mem_palace_key", ".memoria_palacio_cifrada"):
    if any(ROOT.rglob(forbidden)):
        errors.append(f"posible secreto/estado privado dentro de agencia: {forbidden}")

source_roots = [Path("Agencia_para_proyectos_desde_0"), Path("Agencia_Proyectos_Existentes")]
if any((ROOT / rel).exists() for rel in source_roots):
    errors.append("la agencia nueva contiene una ruta de fuente original")

total_md = sum(1 for p in ROOT.rglob("*.md") if p.relative_to(ROOT).parts[0] not in EXCLUIDOS_VALIDACION and "skills-activos" not in p.parts)
print(f"skills={len(skills)} agentes={len(agents)} scripts={len(scripts_py)} audios={len(audios_esperados)} archivos_md={total_md}")

if errors:
    print("VALIDACION FALLIDA")
    print("\n".join(f"- {error}" for error in errors))
    raise SystemExit(1)

print("VALIDACION OK (integridad local; no certifica servicios externos ni calidad de proyectos)")
