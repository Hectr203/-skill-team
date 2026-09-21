import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def ahora_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def resolver_proyecto(ruta: str) -> Path:
    return Path(ruta).expanduser().resolve()


def rutas_memoria(proyecto: Path) -> dict[str, Path]:
    base = proyecto / ".memoria"
    return {
        "base": base,
        "clave": base / "mem_palace.key",
        "mem_palace": base / "mem_palace.enc",
        "cloudmem": base / "cloudmem.jsonl",
        "manifiesto": base / "manifiesto_memoria.md",
    }


def obtener_fernet(rutas: dict[str, Path]):
    try:
        from cryptography.fernet import Fernet
    except ImportError as exc:
        raise RuntimeError("Falta instalar cryptography: pip install cryptography") from exc

    rutas["base"].mkdir(parents=True, exist_ok=True)
    if not rutas["clave"].exists():
        rutas["clave"].write_bytes(Fernet.generate_key())
    return Fernet(rutas["clave"].read_bytes())


def inicializar(proyecto: Path) -> dict[str, Path]:
    rutas = rutas_memoria(proyecto)
    rutas["base"].mkdir(parents=True, exist_ok=True)
    obtener_fernet(rutas)
    if not rutas["cloudmem"].exists():
        rutas["cloudmem"].write_text("", encoding="utf-8")
    if not rutas["manifiesto"].exists():
        rutas["manifiesto"].write_text(
            f"""# Manifiesto de Memoria del Proyecto

## Proyecto
- Ruta: {proyecto}
- Creado: {ahora_iso()}

## Archivos de memoria
- Mem Palace local: `.memoria/mem_palace.enc`
- Clave local: `.memoria/mem_palace.key`
- CloudMem local: `.memoria/cloudmem.jsonl`

## Regla
Esta memoria pertenece unicamente a este proyecto. No debe copiar contexto desde otros proyectos salvo que el humano lo solicite de forma explicita y se documente la razon.
""",
            encoding="utf-8",
        )
    if not rutas["mem_palace"].exists():
        contenido_inicial = f"""[MEMORIA DE PROYECTO]
- Fecha: {ahora_iso()}
- Tareas completadas: Inicializacion de memoria independiente del proyecto.
- Pendientes: Registrar el primer contexto operativo del proyecto.
- Decisiones tecnicas: La memoria de este proyecto queda aislada en `.memoria/`.
- Riesgos: No copiar memoria desde otros proyectos sin autorizacion explicita.
"""
        rutas["mem_palace"].write_bytes(obtener_fernet(rutas).encrypt(contenido_inicial.encode("utf-8")))
    return rutas


def leer_mem_palace(proyecto: Path) -> str:
    rutas = inicializar(proyecto)
    if not rutas["mem_palace"].exists():
        return ""
    return obtener_fernet(rutas).decrypt(rutas["mem_palace"].read_bytes()).decode("utf-8")


def guardar_mem_palace(proyecto: Path, informe: str, acumular: bool = True) -> None:
    rutas = inicializar(proyecto)
    contenido = informe
    if acumular and rutas["mem_palace"].exists():
        previo = leer_mem_palace(proyecto).rstrip()
        contenido = f"{previo}\n\n{informe}" if previo else informe
    rutas["mem_palace"].write_bytes(obtener_fernet(rutas).encrypt(contenido.encode("utf-8")))


def agregar_cloudmem(
    proyecto: Path,
    resumen: str,
    archivos: list[str],
    tipo: str,
    decisiones: str = "",
    pendientes: str = "",
    riesgos: str = "",
) -> None:
    rutas = inicializar(proyecto)
    entrada = {
        "fecha": ahora_iso(),
        "tipo": tipo,
        "resumen": resumen,
        "archivos": archivos,
        "decisiones": decisiones,
        "pendientes": pendientes,
        "riesgos": riesgos,
    }
    with rutas["cloudmem"].open("a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(entrada, ensure_ascii=False) + "\n")


def leer_cloudmem(proyecto: Path, limite: int = 8, filtro: str = "") -> list[dict]:
    rutas = inicializar(proyecto)
    entradas: list[dict] = []
    for linea in rutas["cloudmem"].read_text(encoding="utf-8").splitlines():
        try:
            entrada = json.loads(linea)
        except json.JSONDecodeError:
            continue
        texto = json.dumps(entrada, ensure_ascii=False).lower()
        if filtro and filtro.lower() not in texto:
            continue
        entradas.append(entrada)
    return entradas[-limite:]


def imprimir_cloudmem(entradas: list[dict]) -> None:
    if not entradas:
        print("[i] CloudMem del proyecto no tiene entradas.")
        return
    print("--- CLOUDMEM DEL PROYECTO ---")
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
    print("-----------------------------")


def informe(tareas: str, pendientes: str, decisiones: str, riesgos: str) -> str:
    return f"""[MEMORIA DE PROYECTO]
- Fecha: {ahora_iso()}
- Tareas completadas: {tareas}
- Pendientes: {pendientes}
- Decisiones tecnicas: {decisiones}
- Riesgos: {riesgos}
"""


def lista_archivos(valor: str) -> list[str]:
    return [item.strip() for item in valor.split(",") if item.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Memoria independiente por proyecto.")
    parser.add_argument("--proyecto", default=".", help="Ruta raiz del proyecto.")
    subparsers = parser.add_subparsers(dest="comando", required=True)

    subparsers.add_parser("init", help="Inicializa la memoria del proyecto.")

    consultar = subparsers.add_parser("start", help="Consulta memoria del proyecto.")
    consultar.add_argument("--limite", type=int, default=8)
    consultar.add_argument("--filtro", default="")

    cerrar = subparsers.add_parser("close", help="Registra cierre en memoria del proyecto.")
    cerrar.add_argument("--tareas", required=True)
    cerrar.add_argument("--pendientes", default="")
    cerrar.add_argument("--decisiones", default="")
    cerrar.add_argument("--riesgos", default="")
    cerrar.add_argument("--cloud-resumen", default="")
    cerrar.add_argument("--archivos", default="")
    cerrar.add_argument("--tipo", default="operativo")

    agregar = subparsers.add_parser("add", help="Agrega solo una entrada operativa CloudMem.")
    agregar.add_argument("--resumen", required=True)
    agregar.add_argument("--archivos", default="")
    agregar.add_argument("--tipo", default="operativo")
    agregar.add_argument("--decisiones", default="")
    agregar.add_argument("--pendientes", default="")
    agregar.add_argument("--riesgos", default="")

    args = parser.parse_args()
    proyecto = resolver_proyecto(args.proyecto)

    if args.comando == "init":
        rutas = inicializar(proyecto)
        print(f"[+] Memoria de proyecto inicializada: {rutas['base']}")
        return

    if args.comando == "start":
        inicializar(proyecto)
        print(f"=== MEMORIA DEL PROYECTO: {proyecto} ===")
        contexto = leer_mem_palace(proyecto)
        if contexto:
            print("--- MEM PALACE DEL PROYECTO ---")
            print(contexto)
            print("--------------------------------")
        else:
            print("[i] Mem Palace del proyecto no tiene entradas.")
        imprimir_cloudmem(leer_cloudmem(proyecto, limite=args.limite, filtro=args.filtro))
        return

    if args.comando == "close":
        inicializar(proyecto)
        guardar_mem_palace(proyecto, informe(args.tareas, args.pendientes, args.decisiones, args.riesgos))
        if args.cloud_resumen:
            agregar_cloudmem(
                proyecto,
                args.cloud_resumen,
                lista_archivos(args.archivos),
                args.tipo,
                args.decisiones,
                args.pendientes,
                args.riesgos,
            )
        print(f"[+] Memoria del proyecto actualizada: {proyecto / '.memoria'}")
        return

    agregar_cloudmem(
        proyecto,
        args.resumen,
        lista_archivos(args.archivos),
        args.tipo,
        args.decisiones,
        args.pendientes,
        args.riesgos,
    )
    print(f"[+] Entrada CloudMem guardada en: {proyecto / '.memoria'}")


if __name__ == "__main__":
    main()
