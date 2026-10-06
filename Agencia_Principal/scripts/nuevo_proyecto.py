#!/usr/bin/env python3
"""
Crea un nuevo proyecto en contexts/projects/ a partir de las plantillas oficiales
e inicializa su memoria estructurada independiente.

Uso:
    python3 scripts/nuevo_proyecto.py <nombre-proyecto> [--cliente CLIENTE] [--tipo TIPO]

Ejemplo:
    python3 scripts/nuevo_proyecto.py vtptransportes --cliente "Transportes del Norte" --tipo "existente"
    python3 scripts/nuevo_proyecto.py mi-api-clientes --tipo "nuevo"
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

# Agregar directorio scripts al sys.path
SCRIPT_DIR = Path(__file__).parent.resolve()
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from memoria_proyecto import ahora_iso, inicializar, resolver_proyecto


def crear_proyecto(nombre: str, cliente: str = "", tipo: str = "nuevo", stack: str = "estandar") -> Path:
    raiz_agencia = Path(__file__).resolve().parents[1]
    raiz_proyectos = raiz_agencia / "contexts" / "projects"
    plantillas_dir = raiz_agencia / "plantillas"
    stacks_dir = raiz_agencia / "stacks"

    # Validar caracteres del nombre
    caracteres_invalidos = set(' /\\:*?"<>|')
    if caracteres_invalidos.intersection(set(nombre)):
        print(f"[!] Error: El nombre '{nombre}' contiene caracteres no permitidos.")
        sys.exit(1)

    destino = raiz_proyectos / nombre

    if destino.exists():
        print(f"[!] El proyecto '{nombre}' ya existe en: {destino}")
        print("    Elige un nombre diferente o consulta el proyecto con:")
        print(f"    python3 scripts/arranque.py --proyecto contexts/projects/{nombre}")
        sys.exit(1)

    print("=== AGENCIA PRINCIPAL — NUEVO PROYECTO ===")
    print(f"\n[+] ID del Proyecto: {nombre}")
    print(f"    Ubicación:       {destino}")
    print(f"    Tipo:            {tipo}")
    print(f"    Stack:           {stack}")
    if cliente:
        print(f"    Cliente:         {cliente}")

    # Verificar o auto-generar perfil de stack si es alternativo
    ruta_stack = stacks_dir / "estandar"
    if stack != "estandar":
        ruta_stack = stacks_dir / "alternativos" / stack
        if not ruta_stack.exists():
            print(f"[i] El stack alternativo '{stack}' no existe. Auto-generando perfil en stacks/alternativos/{stack}...")
            ruta_stack.mkdir(parents=True, exist_ok=True)
            plantilla_stack = stacks_dir / "plantillas" / "nuevo-stack.md"
            contenido_stack = plantilla_stack.read_text(encoding="utf-8") if plantilla_stack.exists() else "# Nuevo Stack\n"
            contenido_stack = contenido_stack.replace("[ejemplo: laravel-livewire-alpine]", stack)
            contenido_stack = contenido_stack.replace("[Ejemplo: Laravel + Livewire + Alpine.js]", stack.replace("-", " ").title())
            (ruta_stack / "stack.md").write_text(contenido_stack, encoding="utf-8")
            print(f"    ✓ Perfil creado: stacks/alternativos/{stack}/stack.md")

    destino.mkdir(parents=True, exist_ok=True)

    # 1. Crear Manifiesto del proyecto
    manifiesto_path = destino / "manifiesto.md"
    plantilla_manifiesto = plantillas_dir / "manifiesto-proyecto.md"
    contenido_manifiesto = ""
    if plantilla_manifiesto.exists():
        contenido_manifiesto = plantilla_manifiesto.read_text(encoding="utf-8")
        # Personalizar cabecera
        contenido_manifiesto = contenido_manifiesto.replace("- ID:", f"- ID: {nombre}")
        contenido_manifiesto = contenido_manifiesto.replace("- Cliente y marca:", f"- Cliente y marca: {cliente or 'Por definir'}")
        contenido_manifiesto = contenido_manifiesto.replace("- Tipo: nuevo | existente | auditoria | correccion | produccion", f"- Tipo: {tipo}")
        contenido_manifiesto += f"\n- Stack Tecnológico Asignado: stacks/{'estandar' if stack == 'estandar' else f'alternativos/{stack}'}\n"
    else:
        contenido_manifiesto = f"""# Manifiesto del proyecto: {nombre}

- ID: {nombre}
- Cliente y marca: {cliente or 'Por definir'}
- Tipo: {tipo}
- Stack Tecnológico Asignado: stacks/{'estandar' if stack == 'estandar' else f'alternativos/{stack}'}
- Objetivo y problema:
- Alcance / fuera de alcance:
- Usuarios:
- Requisitos funcionales y no funcionales:
- Restricciones y aprobaciones:
- Arquitectura y stack detectado:
- Frontend / backend / datos:
- Memoria y grafo:
- Criterios de aceptacion:
- Pruebas y evidencias:
- Riesgos, decisiones y pendientes:
- Proximo paso:
"""
    manifiesto_path.write_text(contenido_manifiesto, encoding="utf-8")
    print("      ✓ Manifiesto creado: manifiesto.md")

    # 2. Inicializar memoria estructurada (memoria.md + .memoria/)
    rutas_mem = inicializar(destino)
    print("      ✓ Memoria inicializada: memoria.md y .memoria/")

    # 3. Crear directorio de ADRs con plantilla de referencia
    adrs_dir = destino / "adrs"
    adrs_dir.mkdir(parents=True, exist_ok=True)
    plantilla_adr = plantillas_dir / "adr.md"
    plantilla_adr_contenido = plantilla_adr.read_text(encoding="utf-8") if plantilla_adr.exists() else "# Plantilla ADR\n"
    (adrs_dir / "README.md").write_text(
        f"""# Decisiones de Arquitectura (ADRs) - {nombre}

Guarda aquí cada Architectural Decision Record con el formato `ADR-001-<slug>.md`.

---
## Plantilla de Referencia:
{plantilla_adr_contenido}
""",
        encoding="utf-8",
    )
    print("      ✓ Directorio de ADRs creado: adrs/")

    # 4. Crear directorio de evidencias
    evidencias_dir = destino / "evidencias"
    evidencias_dir.mkdir(parents=True, exist_ok=True)
    (evidencias_dir / "README.md").write_text(
        f"""# Evidencias de Validación - {nombre}

Almacena aquí logs de pruebas, capturas de pantalla, reportes de linter y recibos de auditoría.
""",
        encoding="utf-8",
    )
    print("      ✓ Directorio de evidencias creado: evidencias/")

    # 5. Crear .gitignore con política Zero-Leakage
    gitignore_path = destino / ".gitignore"
    gitignore_path.write_text(
        """# Secretos del proyecto y memoria cifrada (Zero-Leakage Policy)
.memoria/*.key
.memoria/*.enc
.mem_palace.key
.mem_palace_key
.env
.env.*
!.env.example

# Cachés y temporales
__pycache__/
*.py[cod]
node_modules/
dist/
build/
*.log
""",
        encoding="utf-8",
    )
    print("      ✓ Archivo de protección de secretos creado: .gitignore")

    print(f"\n✅ Proyecto '{nombre}' creado con éxito en contexts/projects/{nombre}.\n")
    print("── Siguientes pasos recomendados ────────────────────────────────")
    print(f"  1. Completa el manifiesto del proyecto:")
    print(f"       {manifiesto_path}")
    print(f"  2. Consulta la memoria al inicio de cada sesión:")
    print(f"       python3 scripts/arranque.py --proyecto {nombre}")
    print(f"  3. Registra el cierre de sesión o tarea tras cada cambio:")
    print(f"       python3 scripts/cierre.py --proyecto {nombre} \\")
    print(f'           --tareas "Definición inicial de alcance" \\')
    print(f'           --decisiones "Arquitectura inicial acordada"')
    print("────────────────────────────────────────────────────────────────\n")

    return destino


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Crea un nuevo proyecto en contexts/projects/ e inicializa su memoria."
    )
    parser.add_argument(
        "nombre",
        help="Nombre/ID del proyecto (ej: mi-sistema, vtptransportes).",
    )
    parser.add_argument(
        "--cliente",
        default="",
        help="Nombre del cliente o marca asociada.",
    )
    parser.add_argument(
        "--tipo",
        default="nuevo",
        choices=["nuevo", "existente", "auditoria", "correccion", "produccion"],
        help="Tipo de proyecto (default: nuevo).",
    )
    parser.add_argument(
        "--stack",
        default="estandar",
        help="Identificador del stack tecnológico (default: estandar, o nombre en stacks/alternativos/).",
    )
    args = parser.parse_args()
    crear_proyecto(args.nombre, args.cliente, args.tipo, args.stack)


if __name__ == "__main__":
    main()
