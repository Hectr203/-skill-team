"""
Crea un nuevo proyecto a partir de la plantilla base e inicializa su memoria independiente.

Uso:
    python3 scripts/nuevo_proyecto.py <nombre-proyecto>

Ejemplo:
    python3 scripts/nuevo_proyecto.py mi-nuevo-proyecto

El script:
    1. Verifica que el nombre no exista en proyectos/.
    2. Copia proyectos/_plantilla_proyecto -> proyectos/<nombre>.
    3. Ejecuta memoria_proyecto.py de la skill ahorro-contexto para generar .memoria/.
"""

import argparse
import shutil
import sys
from pathlib import Path

def _agregar_ruta_scripts() -> None:
    # Agrega la ruta de los scripts de la skill ahorro-contexto
    raiz_agencia = Path(__file__).parent.parent.resolve()
    ruta_memoria = raiz_agencia / "skills" / "ahorro-contexto" / "scripts"
    ruta_str = str(ruta_memoria)
    if ruta_str not in sys.path:
        sys.path.insert(0, ruta_str)

def crear_proyecto(nombre: str) -> None:
    raiz_agencia = Path(__file__).parent.parent.resolve()
    raiz_proyectos = raiz_agencia / "proyectos"
    plantilla = raiz_proyectos / "_plantilla_proyecto"
    destino = raiz_proyectos / nombre

    # Validaciones
    if not plantilla.exists():
        print(f"[!] Plantilla no encontrada: {plantilla}")
        sys.exit(1)

    if destino.exists():
        print(f"[!] El proyecto '{nombre}' ya existe en: {destino}")
        sys.exit(1)

    caracteres_invalidos = set(' /\\:*?"<>|')
    invalidos_encontrados = caracteres_invalidos.intersection(set(nombre))
    if invalidos_encontrados:
        print(f"[!] Nombre inválido. Caracteres no permitidos: {invalidos_encontrados}")
        sys.exit(1)

    print(f"=== AGENCIA PROYECTOS DESDE CERO — NUEVO PROYECTO ===")
    print(f"\n[+] Nombre: {nombre}")
    print(f"    Destino: {destino}")

    # Paso 1: Copiar plantilla
    print("\n[1/2] Copiando estructura base...")
    shutil.copytree(str(plantilla), str(destino))
    print(f"      ✓ Carpeta creada: proyectos/{nombre}/")

    # Paso 2: Inicializar memoria independiente usando la skill ahorro-contexto
    print("\n[2/2] Inicializando memoria del proyecto...")
    _agregar_ruta_scripts()
    try:
        from memoria_proyecto import inicializar  # type: ignore[import]

        rutas = inicializar(destino)
        print(f"      ✓ Memoria inicializada en: proyectos/{nombre}/.memoria/")
    except Exception as exc:
        print(f"[!] Error al inicializar memoria: {exc}")
        print("    Verifica que la skill ahorro-contexto esté presente y configurada.")
        sys.exit(1)

    print(f"\n✅ Proyecto '{nombre}' creado con éxito.\n")
    print("── Siguientes pasos ──────────────────────────────────────────")
    print(f"  1. Define la arquitectura y contexto en:")
    print(f"       proyectos/{nombre}/context/manifiesto-proyecto.md")
    print(f"  2. Inicia tu sesión de desarrollo (ahorro-contexto):")
    print(f"       python3 skills/ahorro-contexto/scripts/arranque.py --proyecto proyectos/{nombre}")
    print("──────────────────────────────────────────────────────────────")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crea un nuevo proyecto desde la plantilla.")
    parser.add_argument("nombre", help="Nombre del proyecto (sin espacios).")
    args = parser.parse_args()
    crear_proyecto(args.nombre)
