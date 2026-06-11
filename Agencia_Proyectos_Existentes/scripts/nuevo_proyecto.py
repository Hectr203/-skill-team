"""
Crea un nuevo proyecto a partir de la plantilla base e inicializa su memoria independiente.

Uso:
    python3 scripts/nuevo_proyecto.py <nombre-proyecto>

Ejemplo:
    python3 scripts/nuevo_proyecto.py vtptransportes
    python3 scripts/nuevo_proyecto.py mi-api-clientes

El script:
    1. Verifica que el nombre no exista en proyectos/.
    2. Copia proyectos/_plantilla_proyecto -> proyectos/<nombre>.
    3. Ejecuta memoria_proyecto.py init para generar .memoria/ independiente.
    4. Imprime los siguientes pasos recomendados.
"""

import argparse
import shutil
import sys
from pathlib import Path


def _agregar_ruta_scripts() -> None:
    directorio = Path(__file__).parent.resolve()
    ruta = str(directorio)
    if ruta not in sys.path:
        sys.path.insert(0, ruta)


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
        print("    Elige un nombre diferente o trabaja en el proyecto existente.")
        sys.exit(1)

    # Caracteres no permitidos en nombres de proyecto
    caracteres_invalidos = set(' /\\:*?"<>|')
    invalidos_encontrados = caracteres_invalidos.intersection(set(nombre))
    if invalidos_encontrados:
        print(f"[!] Nombre inválido. Caracteres no permitidos: {invalidos_encontrados}")
        sys.exit(1)

    print(f"=== AGENCIA PROYECTOS EXISTENTES — NUEVO PROYECTO ===")
    print(f"\n[+] Nombre: {nombre}")
    print(f"    Origen:  {plantilla}")
    print(f"    Destino: {destino}")

    # Paso 1: Copiar plantilla
    print("\n[1/2] Copiando plantilla...")
    shutil.copytree(str(plantilla), str(destino))
    print(f"      ✓ Carpeta creada: proyectos/{nombre}/")

    # Paso 2: Inicializar memoria independiente
    print("\n[2/2] Inicializando memoria independiente...")
    _agregar_ruta_scripts()
    try:
        from memoria_proyecto import inicializar, resolver_proyecto  # type: ignore[import]

        rutas = inicializar(destino)
        print(f"      ✓ Memoria creada: proyectos/{nombre}/.memoria/")
        print(f"        - {rutas['mem_palace'].name}")
        print(f"        - {rutas['clave'].name}")
        print(f"        - {rutas['cloudmem'].name}")
        print(f"        - {rutas['manifiesto'].name}")
    except Exception as exc:
        print(f"[!] Error al inicializar memoria: {exc}")
        print("    Intenta manualmente:")
        print(f"    python3 scripts/memoria_proyecto.py --proyecto proyectos/{nombre} init")
        sys.exit(1)

    print(f"\n✅ Proyecto '{nombre}' creado con éxito.\n")
    print("── Siguientes pasos ──────────────────────────────────────────")
    print(f"  1. Completa el manifiesto del proyecto:")
    print(f"       proyectos/{nombre}/context/manifiesto-proyecto.md")
    print(f"  2. Consulta la memoria al inicio de cada sesión:")
    print(f"       python3 scripts/arranque.py --proyecto proyectos/{nombre}")
    print(f"  3. Registra el cierre después de cada cambio importante:")
    print(f"       python3 scripts/cierre.py --proyecto proyectos/{nombre} \\")
    print(f'           --tareas "Primera sesion de contexto" \\')
    print(f'           --cloud-resumen "Proyecto inicializado desde plantilla"')
    print("──────────────────────────────────────────────────────────────")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Crea un nuevo proyecto desde la plantilla e inicializa su memoria."
    )
    parser.add_argument(
        "nombre",
        help="Nombre del proyecto (sin espacios ni caracteres especiales). "
             "Ejemplo: vtptransportes, mi-api-clientes",
    )
    args = parser.parse_args()
    crear_proyecto(args.nombre)
