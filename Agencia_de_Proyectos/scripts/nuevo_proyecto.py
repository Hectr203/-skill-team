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


def crear_proyecto(nombre: str, cliente: str = "", tipo: str = "nuevo") -> Path:
    raiz_agencia = Path(__file__).resolve().parents[1]
    raiz_proyectos = raiz_agencia / "contexts" / "projects"
    plantillas_dir = raiz_agencia / "plantillas"

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

    print("=== AGENCIA DE PROYECTOS — NUEVO PROYECTO ===")
    print(f"\n[+] ID del Proyecto: {nombre}")
    print(f"    Ubicación:       {destino}")
    print(f"    Tipo:            {tipo}")
    if cliente:
        print(f"    Cliente:         {cliente}")

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
    else:
        contenido_manifiesto = f"""# Manifiesto del proyecto: {nombre}

- ID: {nombre}
- Cliente y marca: {cliente or 'Por definir'}
- Tipo: {tipo}
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
    args = parser.parse_args()
    crear_proyecto(args.nombre, args.cliente, args.tipo)


if __name__ == "__main__":
    main()
