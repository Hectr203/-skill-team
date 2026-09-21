#!/usr/bin/env python3
"""Non-destructive structural validator for Agencia de Proyectos."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "AGENTS.md", "asistente-principal.md", "opencode.json",
    "mcp/registro-mcp.md", "mcp/mcp_config.example.json",
    "flujos/proyecto-nuevo.md", "flujos/proyecto-existente.md",
    "flujos/auditoria-seguridad.md", "flujos/produccion-growth.md",
    "flujos/correccion-urgente.md", "reglas/human-in-the-loop.md",
    ".agents/rules/README.md", "mcp/registro-mcp.md",
]
errors: list[str] = []
for item in REQUIRED:
    if not (ROOT / item).is_file():
        errors.append(f"falta {item}")

try:
    json.loads((ROOT / "opencode.json").read_text())
    json.loads((ROOT / "mcp/mcp_config.example.json").read_text())
except (OSError, json.JSONDecodeError) as exc:
    errors.append(f"JSON invalido: {exc}")

skills = list(ROOT.glob("skills/**/SKILL.md"))
if not skills:
    errors.append("no hay SKILL.md")
for path in skills:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or not re.search(r"^name:\s*[a-z0-9-]+$", text, re.M):
        errors.append(f"frontmatter name invalido: {path.relative_to(ROOT)}")
    if not re.search(r"^description:\s*.+$", text, re.M):
        errors.append(f"frontmatter description ausente: {path.relative_to(ROOT)}")

agents = list((ROOT / "agentes").glob("*.md"))
if len(agents) < 12:
    errors.append("faltan agentes especializados")
for path in agents:
    text = path.read_text(encoding="utf-8").lower()
    if path.name != "contrato-agente.md" and not all(
        marker in text for marker in ("objetivo", "entradas", "entrega", "aceptación")
    ):
        errors.append(f"contrato incompleto: {path.relative_to(ROOT)}")

for path in ROOT.rglob("*.md"):
    if "http://" in path.read_text(encoding="utf-8"):
        errors.append(f"URL insegura http: {path.relative_to(ROOT)}")
    # Check only local Markdown links; external URLs are intentionally not
    # fetched by this deterministic validator.
    for target in re.findall(r"\]\(([^)#]+)(?:#[^)]+)?\)", path.read_text(encoding="utf-8")):
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

for directory in ROOT.rglob("*"):
    if directory.is_dir() and not any(directory.iterdir()):
        errors.append(f"directorio vacio: {directory.relative_to(ROOT)}")

for forbidden in (".env", ".mem_palace_key", ".memoria_palacio_cifrada"):
    if any(ROOT.rglob(forbidden)):
        errors.append(f"posible secreto/estado privado dentro de agencia: {forbidden}")

source_roots = [Path("Agencia_para_proyectos_desde_0"), Path("Agencia_Proyectos_Existentes")]
if any((ROOT / rel).exists() for rel in source_roots):
    errors.append("la agencia nueva contiene una ruta de fuente original")

print(f"skills={len(skills)} archivos_md={len(list(ROOT.rglob('*.md')))}")
if errors:
    print("VALIDACION FALLIDA")
    print("\n".join(f"- {error}" for error in errors))
    raise SystemExit(1)
print("VALIDACION OK")
