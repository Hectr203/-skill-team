#!/usr/bin/env python3
"""
Doctor y Preflight Health Check — Agencia de Proyectos.

Diagnostica el entorno operativo:
- Intérprete Python y módulos clave
- Entorno Node.js y gestores de paquetes
- Herramientas CLI y reproductores de audio
- Servidores MCP y configuraciones declaradas
- Integridad de carpetas de contexto, plantillas, agentes y skills
- Recomendaciones de remediación accionables

Uso:
    python3 scripts/doctor.py [--verbose]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

# Códigos ANSI para salida con colores
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
AZUL = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


class Doctor:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.raiz = Path(__file__).resolve().parents[1]
        self.oks = 0
        self.warns = 0
        self.fails = 0
        self.sugerencias: list[str] = []

    def ok(self, mensaje: str, detalle: str = "") -> None:
        self.oks += 1
        d_str = f" {CYAN}({detalle}){RESET}" if detalle else ""
        print(f"  {VERDE}[✓ OK]{RESET} {mensaje}{d_str}")

    def warn(self, mensaje: str, sugerencia: str = "") -> None:
        self.warns += 1
        print(f"  {AMARILLO}[⚠ WARN]{RESET} {mensaje}")
        if sugerencia:
            self.sugerencias.append(f"[WARN] {mensaje} -> {sugerencia}")
            if self.verbose:
                print(f"         {AMARILLO}└─ Sugerencia: {sugerencia}{RESET}")

    def fail(self, mensaje: str, sugerencia: str = "") -> None:
        self.fails += 1
        print(f"  {ROJO}[✗ FAIL]{RESET} {mensaje}")
        if sugerencia:
            self.sugerencias.append(f"[FAIL] {mensaje} -> {sugerencia}")
            print(f"         {ROJO}└─ Remediación: {sugerencia}{RESET}")

    def info(self, mensaje: str) -> None:
        print(f"  {AZUL}[ℹ INFO]{RESET} {mensaje}")

    def seccion(self, titulo: str) -> None:
        print(f"\n{BOLD}{AZUL}── {titulo} ──────────────────────────────────────{RESET}")

    def verificar_python(self) -> None:
        self.seccion("1. Entorno Python")
        v = sys.version_info
        if v.major >= 3 and v.minor >= 9:
            self.ok(f"Python {v.major}.{v.minor}.{v.micro}", sys.executable)
        else:
            self.fail(f"Python {v.major}.{v.minor} es antiguo", "Se recomienda Python 3.10 o superior.")

        modulos_core = ["json", "pathlib", "sqlite3", "subprocess", "shutil", "argparse"]
        for m in modulos_core:
            if importlib.util.find_spec(m):
                if self.verbose:
                    self.ok(f"Módulo estándar: {m}")
            else:
                self.fail(f"Falta módulo estándar: {m}", f"Instalar Python con soporte de {m}")

        # Módulos opcionales pero recomendados
        for m, pkg in [("cryptography", "cryptography"), ("requests", "requests")]:
            if importlib.util.find_spec(m):
                self.ok(f"Módulo opcional: {m}")
            else:
                self.warn(f"Módulo opcional '{m}' no instalado", f"pip install {pkg}")

    def verificar_node(self) -> None:
        self.seccion("2. Entorno Node.js y JavaScript")
        node = shutil.which("node")
        if node:
            try:
                res = subprocess.run([node, "--version"], capture_output=True, text=True, timeout=2)
                self.ok(f"Node.js instalado: {res.stdout.strip()}", node)
            except Exception:
                self.ok("Node.js instalado", node)
        else:
            self.warn("Node.js no encontrado en PATH", "Instalar Node.js LTS para soporte completo de MCPs y tooling frontend.")

        for tool in ["npm", "npx"]:
            p = shutil.which(tool)
            if p:
                self.ok(f"Herramienta '{tool}' disponible", p)
            else:
                self.warn(f"'{tool}' no disponible en PATH")

    def verificar_herramientas_cli(self) -> None:
        self.seccion("3. Herramientas CLI y Reproductores de Audio")
        # Git
        git = shutil.which("git")
        if git:
            self.ok("Git disponible", git)
        else:
            self.fail("Git no encontrado", "Instala git para versionar proyectos y calcular diffs.")

        # Audio players en Linux / macOS / Windows
        reproductores = ["paplay", "aplay", "ffplay", "pw-cat", "afplay", "powershell.exe"]
        encontrados = [r for r in reproductores if shutil.which(r)]
        if encontrados:
            self.ok(f"Reproductores de sonido del sistema: {', '.join(encontrados)}")
        else:
            self.warn(
                "Sin reproductor de audio instalado (paplay, aplay, etc.)",
                "Las alertas usarán pitido de campana en terminal. Instala 'pulseaudio-utils' o 'alsa-utils' para soporte mp3."
            )

        # Archivos de audio en audios/
        audios_dir = self.raiz / "audios"
        if not audios_dir.exists():
            self.fail("Directorio audios/ ausente", "Crea la carpeta audios/ y copia los archivos de alerta.")
        else:
            requeridos = ["Aprobación urgente..mp3", "Necesito Validación.mp3", "noti.mp3", "termine la tarea.mp3"]
            presentes = [a for a in requeridos if (audios_dir / a).exists()]
            if len(presentes) == len(requeridos):
                self.ok(f"Todos los archivos de audio oficiales presentes ({len(presentes)}/4)")
            else:
                faltantes = set(requeridos) - set(presentes)
                self.warn(f"Faltan audios: {', '.join(faltantes)}", "Copia los audios desde Agencia_para_proyectos_desde_0/audios/")

    def verificar_mcps(self) -> None:
        self.seccion("4. Servidores MCP y Tooling Especializado")
        # Registro MCP
        registro = self.raiz / "mcp" / "registro-mcp.md"
        if registro.exists():
            self.ok("Registro de servidores MCP presente (mcp/registro-mcp.md)")
        else:
            self.fail("Falta mcp/registro-mcp.md")

        # Configuración opencode
        opencode = self.raiz / "opencode.json"
        if opencode.exists():
            try:
                data = json.loads(opencode.read_text(encoding="utf-8"))
                mcps = data.get("mcp", {})
                self.ok(f"opencode.json válido ({len(mcps)} MCPs declarados)")
            except Exception as e:
                self.fail(f"opencode.json con JSON inválido: {e}")
        else:
            self.warn("Falta opencode.json")

        # CLI tools opcionales de memoria y compresión
        for cli, desc in [("claude-mem", "Memoria persistente universal"), ("headroom", "Compresión semántica")]:
            p = shutil.which(cli)
            if p:
                self.ok(f"CLI '{cli}' activo en sistema ({desc})", p)
            else:
                self.info(f"CLI '{cli}' no en PATH (opera mediante fallback transparente en Markdown y logs locales)")

    def verificar_estructura_agencia(self) -> None:
        self.seccion("5. Integridad Estructural y Contextos")
        # Contextos
        contexts = self.raiz / "contexts"
        subdirs_context = ["projects", "brands", "clients", "agency", "campaigns"]
        for s in subdirs_context:
            p = contexts / s
            if p.exists() and p.is_dir():
                archivos_cuenta = len(list(p.glob("*")))
                self.ok(f"Contexto 'contexts/{s}/' ({archivos_cuenta} elementos)")
            else:
                self.fail(f"Falta directorio context: contexts/{s}/")

        # Plantillas
        plantillas = self.raiz / "plantillas"
        for pl in ["manifiesto-proyecto.md", "adr.md"]:
            if (plantillas / pl).exists():
                self.ok(f"Plantilla presente: plantillas/{pl}")
            else:
                self.fail(f"Falta plantilla: plantillas/{pl}")

        # Agentes
        agentes = list((self.raiz / "agentes").glob("*.md"))
        if len(agentes) >= 12:
            self.ok(f"Catálogo de agentes completo ({len(agentes)} agentes)")
        else:
            self.fail(f"Catálogo de agentes incompleto ({len(agentes)} encontrados)")

        # Skills
        skills = list(self.raiz.glob("skills/**/SKILL.md"))
        if len(skills) >= 50:
            self.ok(f"Catálogo de skills amplio ({len(skills)} skills con SKILL.md)")
        else:
            self.warn(f"Pocos skills encontrados ({len(skills)})")

    def ejecutar(self) -> int:
        print(f"\n{BOLD}======================================================={RESET}")
        print(f"{BOLD}🩺 AGENCIA DE PROYECTOS — DIAGNÓSTICO Y PREFLIGHT CHECK{RESET}")
        print(f"{BOLD}======================================================={RESET}")
        print(f"Directorio raíz: {self.raiz}")
        print(f"Sistema Operativo: {platform.system()} {platform.release()} ({platform.machine()})")

        self.verificar_python()
        self.verificar_node()
        self.verificar_herramientas_cli()
        self.verificar_mcps()
        self.verificar_estructura_agencia()

        print(f"\n{BOLD}── Resumen del Diagnóstico ────────────────────────────{RESET}")
        print(f"  {VERDE}✓ Pruebas superadas (OK): {self.oks}{RESET}")
        if self.warns:
            print(f"  {AMARILLO}⚠ Advertencias (WARN):    {self.warns}{RESET}")
        if self.fails:
            print(f"  {ROJO}✗ Fallos críticos (FAIL): {self.fails}{RESET}")

        if self.sugerencias:
            print(f"\n{BOLD}Recomendaciones y Acciones Sugeridas:{RESET}")
            for s in self.sugerencias:
                print(f"  • {s}")

        if self.fails == 0:
            print(f"\n{BOLD}{VERDE}✨ ESTADO DEL SISTEMA: 100% OPERATIVO (NIVEL ÉLITE){RESET}\n")
            return 0
        else:
            print(f"\n{BOLD}{ROJO}❌ SE REQUIERE ATENCIÓN EN {self.fails} COMPONENTE(S){RESET}\n")
            return 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Diagnóstico de salud de la Agencia de Proyectos.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Muestra detalles exhaustivos de cada prueba.")
    args = parser.parse_args()
    doc = Doctor(verbose=args.verbose)
    sys.exit(doc.ejecutar())


if __name__ == "__main__":
    main()
