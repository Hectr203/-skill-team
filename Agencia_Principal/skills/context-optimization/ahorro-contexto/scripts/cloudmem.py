import argparse
import json
import os
from datetime import datetime, timezone


RUTA_CLOUDMEM = ".cloudmem.jsonl"


def _ahora_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _normalizar_lista(valor: str) -> list[str]:
    if not valor:
        return []
    return [item.strip() for item in valor.split(",") if item.strip()]


def agregar_entrada(
    resumen: str,
    archivos: list[str] | None = None,
    tipo: str = "operativo",
    decisiones: str = "",
    pendientes: str = "",
    riesgos: str = "",
) -> dict:
    entrada = {
        "fecha": _ahora_iso(),
        "tipo": tipo,
        "resumen": resumen.strip(),
        "archivos": archivos or [],
        "decisiones": decisiones.strip(),
        "pendientes": pendientes.strip(),
        "riesgos": riesgos.strip(),
    }
    with open(RUTA_CLOUDMEM, "a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(entrada, ensure_ascii=False) + "\n")
    return entrada


def leer_entradas(limite: int = 10, filtro: str = "") -> list[dict]:
    if not os.path.exists(RUTA_CLOUDMEM):
        return []

    entradas: list[dict] = []
    with open(RUTA_CLOUDMEM, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            try:
                entrada = json.loads(linea)
            except json.JSONDecodeError:
                continue
            texto = json.dumps(entrada, ensure_ascii=False).lower()
            if filtro and filtro.lower() not in texto:
                continue
            entradas.append(entrada)
    return entradas[-limite:]


def imprimir_entradas(entradas: list[dict]) -> None:
    if not entradas:
        print("[i] CloudMem local no tiene entradas para mostrar.")
        return

    print("--- HISTORIAL OPERATIVO CLOUDMEM LOCAL ---")
    for entrada in entradas:
        print(f"- Fecha: {entrada.get('fecha', 'sin fecha')}")
        print(f"  Tipo: {entrada.get('tipo', 'operativo')}")
        print(f"  Resumen: {entrada.get('resumen', '')}")
        archivos = entrada.get("archivos") or []
        if archivos:
            print(f"  Archivos: {', '.join(archivos)}")
        if entrada.get("decisiones"):
            print(f"  Decisiones: {entrada['decisiones']}")
        if entrada.get("pendientes"):
            print(f"  Pendientes: {entrada['pendientes']}")
        if entrada.get("riesgos"):
            print(f"  Riesgos: {entrada['riesgos']}")
    print("-----------------------------------------")


def main() -> None:
    parser = argparse.ArgumentParser(description="CloudMem local para historial operativo no sensible.")
    subparsers = parser.add_subparsers(dest="comando", required=True)

    agregar = subparsers.add_parser("add", help="Agregar una entrada al historial operativo.")
    agregar.add_argument("--resumen", required=True)
    agregar.add_argument("--archivos", default="")
    agregar.add_argument("--tipo", default="operativo")
    agregar.add_argument("--decisiones", default="")
    agregar.add_argument("--pendientes", default="")
    agregar.add_argument("--riesgos", default="")

    listar = subparsers.add_parser("list", help="Listar entradas recientes.")
    listar.add_argument("--limite", type=int, default=10)
    listar.add_argument("--filtro", default="")

    args = parser.parse_args()

    if args.comando == "add":
        entrada = agregar_entrada(
            resumen=args.resumen,
            archivos=_normalizar_lista(args.archivos),
            tipo=args.tipo,
            decisiones=args.decisiones,
            pendientes=args.pendientes,
            riesgos=args.riesgos,
        )
        print("[+] Entrada guardada en CloudMem local.")
        imprimir_entradas([entrada])
        return

    imprimir_entradas(leer_entradas(limite=args.limite, filtro=args.filtro))


if __name__ == "__main__":
    main()
