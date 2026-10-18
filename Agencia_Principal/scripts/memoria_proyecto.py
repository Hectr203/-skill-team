#!/usr/bin/env python3
"""
Memoria de Proyecto unificada — Agencia de Proyectos.

Combina persistencia transparente en Markdown (contexts/projects/<id>/memoria.md),
registro local de eventos estructurado en JSONL,
y compatibilidad retroactiva con proyectos existentes.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows fallback
    fcntl = None


def ahora_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def validar_identificador(valor: str) -> str:
    """Un ID explícito evita alias por nombre, traversal y diferencias de mayúsculas."""
    if not isinstance(valor, str) or not re.fullmatch(r"[a-z0-9_][a-z0-9_-]{0,79}", valor):
        raise ValueError("ID inválido: usa de 1 a 80 letras minúsculas, números, guiones o guiones bajos.")
    return valor


def resolver_proyecto(ruta: str | Path, raiz_agencia: Path | None = None) -> Path:
    """Acepta un ID o una ruta central; nunca convierte rutas externas en alias."""
    raiz = (raiz_agencia or Path(__file__).resolve().parents[1]).resolve()
    almacen = raiz / "contexts" / "projects"
    if almacen.resolve() != almacen:
        raise ValueError("El almacén central no puede redirigirse mediante enlaces simbólicos.")
    texto = str(ruta)
    if not texto or texto in (".", "..") or "\\" in texto:
        raise ValueError("Indica un ID de proyecto explícito.")
    entrada = Path(texto).expanduser()
    if len(entrada.parts) == 1 and not entrada.is_absolute():
        candidato = almacen / validar_identificador(texto)
    else:
        if ".." in entrada.parts:
            raise ValueError("No se permiten rutas con '..'.")
        candidato = entrada if entrada.is_absolute() else raiz / entrada
        if candidato.parent != almacen:
            raise ValueError("Ruta externa no registrada: utiliza el ID único de contexts/projects/.")
        validar_identificador(candidato.name)
    if candidato.resolve() != candidato:
        raise ValueError("La memoria del proyecto no puede redirigirse mediante enlaces simbólicos.")
    return candidato


def rutas_memoria(proyecto: Path) -> dict[str, Path]:
    proyecto = proyecto.resolve()
    base = proyecto / ".memoria"
    rutas = {
        "proyecto": proyecto,
        "base": base,
        "memoria_md": proyecto / "memoria.md",
        "manifiesto_md": proyecto / "manifiesto.md",
        "adrs": proyecto / "adrs",
        "evidencias": proyecto / "evidencias",
        "cloudmem": base / "cloudmem.jsonl",
        "timeline": base / "timeline.jsonl",
        "clave": base / "mem_palace.key",
        "mem_palace": base / "mem_palace.enc",
        "manifiesto_mem": base / "manifiesto_memoria.md",
    }
    if any(ruta.resolve() != ruta for ruta in rutas.values()):
        raise ValueError("Los archivos de memoria no pueden redirigirse mediante enlaces simbólicos.")
    return rutas


def _obtener_fernet_opcional(rutas: dict[str, Path], crear: bool = False):
    """Soporte legacy para proyectos cifrados con Fernet sin romper si falta cryptography."""
    try:
        from cryptography.fernet import Fernet  # type: ignore[import]
    except ImportError:
        return None

    if not rutas["clave"].exists():
        if rutas["mem_palace"].exists():
            raise ValueError("Memoria cifrada sin clave: restaurar la clave original antes de modificarla.")
        if not crear:
            return None
        rutas["base"].mkdir(parents=True, exist_ok=True)
        with rutas["clave"].open("xb") as archivo:
            os.chmod(rutas["clave"], 0o600)
            archivo.write(Fernet.generate_key())
    return Fernet(rutas["clave"].read_bytes())


def inicializar(proyecto: Path) -> dict[str, Path]:
    """Inicializa la estructura de memoria de un proyecto."""
    proyecto.mkdir(parents=True, exist_ok=True)
    rutas = rutas_memoria(proyecto)
    rutas["base"].mkdir(parents=True, exist_ok=True)
    rutas["adrs"].mkdir(parents=True, exist_ok=True)
    rutas["evidencias"].mkdir(parents=True, exist_ok=True)
    if rutas["mem_palace"].exists():
        fernet_existente = _obtener_fernet_opcional(rutas)
        if not rutas["memoria_md"].exists():
            if fernet_existente is None:
                raise ValueError("No se puede recuperar la memoria cifrada sin soporte cryptography.")
            # No sustituir el historial anterior por una plantilla vacía.
            texto_existente = fernet_existente.decrypt(rutas["mem_palace"].read_bytes()).decode("utf-8")
            rutas["memoria_md"].write_text(texto_existente, encoding="utf-8")

    # 1. Memoria Markdown principal (visible y versionable)
    if not rutas["memoria_md"].exists():
        rutas["memoria_md"].write_text(
            f"""# Memoria del Proyecto: {proyecto.name}

- **ID de Proyecto:** `{proyecto.name}`
- **Fecha de creación:** {ahora_iso()}
- **Estado general:** Inicializado

---

## 1. Resumen Ejecutivo
Proyecto administrado bajo la Agencia de Proyectos. Memoria estructurada en Markdown con trazabilidad de decisiones, estado y handoffs.

---

## 2. Decisiones Técnicas y ADRs
- Ninguna decisión arquitectónica registrada aún.

---

## 3. Historial de Sesiones y Tareas

### [{ahora_iso()}] Inicialización
- **Agente:** Director de Proyecto / Asistente Principal
- **Tareas:** Estructura de proyecto y memoria inicializadas con éxito.
- **Riesgos:** Ninguno.
- **Siguiente paso:** Completar `manifiesto.md` y definir requerimientos iniciales.
""",
            encoding="utf-8",
        )

    # 2. Timeline JSONL estructurado
    if not rutas["cloudmem"].exists():
        rutas["cloudmem"].write_text("", encoding="utf-8")
    if not rutas["timeline"].exists():
        rutas["timeline"].write_text("", encoding="utf-8")

    # 3. Soporte legacy opcional (si cryptography está disponible)
    fernet = _obtener_fernet_opcional(rutas, crear=True)
    if fernet and not rutas["mem_palace"].exists():
        contenido_inicial = f"""[MEMORIA DE PROYECTO: {proyecto.name}]
- Fecha: {ahora_iso()}
- Tareas completadas: Inicialización de memoria del proyecto.
- Pendientes: Completar manifiesto del proyecto.
"""
        rutas["mem_palace"].write_bytes(fernet.encrypt(contenido_inicial.encode("utf-8")))

    return rutas


def leer_memoria_markdown(proyecto: Path) -> str:
    """Lee el archivo memoria.md del proyecto."""
    rutas = rutas_memoria(proyecto)
    if rutas["memoria_md"].exists():
        return rutas["memoria_md"].read_text(encoding="utf-8")
    return ""


def leer_mem_palace(proyecto: Path) -> str:
    """Lee memoria legacy o hace fallback a memoria.md."""
    rutas = rutas_memoria(proyecto)
    # No inicializar durante una lectura: podría ocultar un historial legacy.
    if rutas["memoria_md"].exists():
        texto = rutas["memoria_md"].read_text(encoding="utf-8")
        if texto.strip():
            return texto

    # Si hay mem_palace.enc cifrado legacy
    if rutas["mem_palace"].exists():
        fernet = _obtener_fernet_opcional(rutas)
        if fernet:
            try:
                return fernet.decrypt(rutas["mem_palace"].read_bytes()).decode("utf-8")
            except Exception:
                pass
    return ""


def guardar_mem_palace(proyecto: Path, informe_texto: str, acumular: bool = True) -> None:
    """Actualiza memoria.md y mantiene compatibilidad con mem_palace si aplica."""
    rutas = inicializar(proyecto)
    with bloqueo_proyecto(rutas["base"]):
        if rutas["memoria_md"].exists() and acumular:
            previo = rutas["memoria_md"].read_text(encoding="utf-8")
            nuevo = f"{previo.rstrip()}\n\n---\n\n{informe_texto}\n"
        else:
            nuevo = informe_texto
        _escritura_atomica(rutas["memoria_md"], nuevo)

    # Actualizar legacy si fernet disponible
    fernet = _obtener_fernet_opcional(rutas)
    if fernet:
        try:
            rutas["mem_palace"].write_bytes(fernet.encrypt(nuevo.encode("utf-8")))
        except Exception:
            pass


def agregar_cloudmem(
    proyecto: Path,
    resumen: str,
    archivos: list[str],
    tipo: str = "operativo",
    decisiones: str = "",
    pendientes: str = "",
    riesgos: str = "",
    agente: str = "agente",
) -> None:
    """Registra una entrada estructurada en cloudmem.jsonl y timeline.jsonl."""
    rutas = inicializar(proyecto)
    entrada = {
        "fecha": ahora_iso(),
        "agente": agente,
        "tipo": tipo,
        "resumen": resumen,
        "archivos": archivos,
        "decisiones": decisiones,
        "pendientes": pendientes,
        "riesgos": riesgos,
    }
    linea = json.dumps(entrada, ensure_ascii=False) + "\n"
    with bloqueo_proyecto(rutas["base"]):
        with rutas["cloudmem"].open("a", encoding="utf-8") as f:
            f.write(linea)
        with rutas["timeline"].open("a", encoding="utf-8") as f:
            f.write(linea)

    # La memoria local no envía datos a herramientas externas automáticamente.


def leer_cloudmem(proyecto: Path, limite: int = 8, filtro: str = "") -> list[dict]:
    """Lee las últimas entradas de cloudmem/timeline."""
    rutas = rutas_memoria(proyecto)
    entradas: list[dict] = []
    fuente = rutas["timeline"] if rutas["timeline"].exists() and rutas["timeline"].stat().st_size else rutas["cloudmem"]
    if not fuente.exists():
        return []

    for linea in fuente.read_text(encoding="utf-8").splitlines():
        if not linea.strip():
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


@contextmanager
def bloqueo_proyecto(base: Path):
    """Serializa cierres por proyecto sin añadir dependencias externas."""
    base.mkdir(parents=True, exist_ok=True)
    lock_path = base / ".lock"
    if lock_path.is_symlink():
        raise ValueError("El bloqueo de memoria no puede redirigirse.")
    with lock_path.open("a+", encoding="utf-8") as lock:
        if fcntl is not None:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            if fcntl is not None:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def _escritura_atomica(path: Path, contenido: str) -> None:
    """Escribe un archivo mediante reemplazo atómico en el mismo directorio."""
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as tmp:
            tmp.write(contenido)
            tmp.flush()
            os.fsync(tmp.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def imprimir_cloudmem(entradas: list[dict]) -> None:
    if not entradas:
        print("[i] Historial estructurado (Timeline/CloudMem) sin entradas recientes.")
        return
    print("--- TIMELINE ESTRUCTURADO DEL PROYECTO ---")
    for entrada in entradas:
        print(f"- [{entrada.get('fecha', 'sin fecha')}] ({entrada.get('agente', 'agente')}) {entrada.get('tipo', 'operativo')}")
        print(f"  Resumen:    {entrada.get('resumen', '')}")
        archivos = entrada.get("archivos") or []
        if archivos:
            print(f"  Archivos:   {', '.join(archivos)}")
        if entrada.get("decisiones"):
            print(f"  Decisiones: {entrada['decisiones']}")
        if entrada.get("pendientes"):
            print(f"  Pendientes: {entrada['pendientes']}")
        if entrada.get("riesgos"):
            print(f"  Riesgos:    {entrada['riesgos']}")
    print("------------------------------------------")


def informe(
    tareas: str,
    pendientes: str = "",
    decisiones: str = "",
    riesgos: str = "",
    agente: str = "agente",
    archivos: list[str] | None = None,
) -> str:
    """Genera un bloque de informe Markdown para memoria.md."""
    archivos_str = ", ".join(f"`{a}`" for a in (archivos or [])) if archivos else "Ninguno"
    return f"""### [{ahora_iso()}] Sesión / Tarea
- **Agente:** {agente}
- **Tareas completadas:** {tareas}
- **Archivos afectados:** {archivos_str}
- **Decisiones técnicas:** {decisiones or 'Ninguna'}
- **Pendientes:** {pendientes or 'Ninguno'}
- **Riesgos identificados:** {riesgos or 'Ninguno'}
"""


def lista_archivos(valor: str) -> list[str]:
    return [item.strip() for item in valor.split(",") if item.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Memoria independiente por proyecto.")
    parser.add_argument("--proyecto", default=".", help="Ruta o ID del proyecto.")
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
    cerrar.add_argument("--agente", default="agente")

    agregar = subparsers.add_parser("add", help="Agrega una entrada estructurada al timeline.")
    agregar.add_argument("--resumen", required=True)
    agregar.add_argument("--archivos", default="")
    agregar.add_argument("--tipo", default="operativo")
    agregar.add_argument("--decisiones", default="")
    agregar.add_argument("--pendientes", default="")
    agregar.add_argument("--riesgos", default="")
    agregar.add_argument("--agente", default="agente")

    args = parser.parse_args()
    proyecto = resolver_proyecto(args.proyecto)

    if args.comando == "init":
        rutas = inicializar(proyecto)
        print(f"[+] Memoria de proyecto inicializada con éxito:")
        print(f"    - Memoria Markdown: {rutas['memoria_md']}")
        print(f"    - Directorio base:  {rutas['base']}")
        return

    if args.comando == "start":
        inicializar(proyecto)
        print(f"=== MEMORIA DEL PROYECTO: {proyecto.name} ===")
        contexto = leer_mem_palace(proyecto)
        if contexto:
            print("--- MEMORIA (Markdown) ---")
            print(contexto)
            print("--------------------------")
        imprimir_cloudmem(leer_cloudmem(proyecto, limite=args.limite, filtro=args.filtro))
        return

    if args.comando == "close":
        inicializar(proyecto)
        archs = lista_archivos(args.archivos)
        inf = informe(
            tareas=args.tareas,
            pendientes=args.pendientes,
            decisiones=args.decisiones,
            riesgos=args.riesgos,
            agente=args.agente,
            archivos=archs,
        )
        guardar_mem_palace(proyecto, inf, acumular=True)
        resumen_linea = args.cloud_resumen or args.tareas
        agregar_cloudmem(
            proyecto=proyecto,
            resumen=resumen_linea,
            archivos=archs,
            tipo=args.tipo,
            decisiones=args.decisiones,
            pendientes=args.pendientes,
            riesgos=args.riesgos,
            agente=args.agente,
        )
        print(f"[+] Memoria del proyecto actualizada: {proyecto / 'memoria.md'}")
        return

    if args.comando == "add":
        archs = lista_archivos(args.archivos)
        agregar_cloudmem(
            proyecto=proyecto,
            resumen=args.resumen,
            archivos=archs,
            tipo=args.tipo,
            decisiones=args.decisiones,
            pendientes=args.pendientes,
            riesgos=args.riesgos,
            agente=args.agente,
        )
        print(f"[+] Entrada registrada en el timeline: {proyecto / '.memoria/timeline.jsonl'}")


if __name__ == "__main__":
    main()
