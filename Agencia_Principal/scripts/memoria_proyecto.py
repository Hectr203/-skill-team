#!/usr/bin/env python3
"""
Memoria de Proyecto unificada — Agencia de Proyectos.

Combina persistencia transparente en Markdown (contexts/projects/<id>/memoria.md)
estructurada en 4 zonas (Estado Activo, Decisiones Vigentes, Ventana Deslizante
e Hitos Compactados), registro append-only de eventos en JSONL (.memoria/timeline.jsonl),
recuperación histórica puntual y compatibilidad retroactiva con proyectos existentes.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
import os
import re
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
import threading

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows fallback
    fcntl = None


def ahora_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def generar_evento_id(fecha_iso: str | None = None, agente: str = "", tareas: str = "") -> str:
    """Genera un identificador de evento único y reproducible."""
    dt_str = fecha_iso or ahora_iso()
    clean_dt = re.sub(r"[^0-9]", "", dt_str)[:14]
    semilla = f"{dt_str}:{agente}:{tareas}"
    digest = hashlib.sha256(semilla.encode("utf-8")).hexdigest()[:6]
    return f"ev_{clean_dt}_{digest}"


def estimar_tokens(texto: str) -> int:
    """Aproximación de ~3.8 caracteres por token."""
    if not texto:
        return 0
    return max(1, int(len(texto) / 3.8))


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
    """Inicializa la estructura de memoria de un proyecto con las 4 secciones estándar."""
    proyecto.mkdir(parents=True, exist_ok=True)
    rutas = rutas_memoria(proyecto)
    rutas["base"].mkdir(parents=True, exist_ok=True)
    rutas["adrs"].mkdir(parents=True, exist_ok=True)
    if not any(rutas["adrs"].iterdir()):
        (rutas["adrs"] / ".gitkeep").touch()
    rutas["evidencias"].mkdir(parents=True, exist_ok=True)
    if not any(rutas["evidencias"].iterdir()):
        (rutas["evidencias"] / ".gitkeep").touch()
    if rutas["mem_palace"].exists():
        fernet_existente = _obtener_fernet_opcional(rutas)
        if not rutas["memoria_md"].exists():
            if fernet_existente is None:
                raise ValueError("No se puede recuperar la memoria cifrada sin soporte cryptography.")
            texto_existente = fernet_existente.decrypt(rutas["mem_palace"].read_bytes()).decode("utf-8")
            rutas["memoria_md"].write_text(texto_existente, encoding="utf-8")

    # 1. Memoria Markdown principal (visible y versionable con estructura formal)
    if not rutas["memoria_md"].exists():
        ahora = ahora_iso()
        ev_init = generar_evento_id(ahora, "Asistente Principal", "Inicialización")
        contenido_inicial = f"""# Memoria del Proyecto: {proyecto.name}

- **ID de Proyecto:** `{proyecto.name}`
- **Fecha de creación:** {ahora}
- **Estado general:** Inicializado

---

## 1. Estado Activo y Criterios Vigentes
- **Objetivo actual:** Estructura de proyecto y memoria inicializadas con éxito.
- **Hito/Sprint:** Inicialización
- **Tarea en curso:** Ninguna
- **Restricciones y bloqueos:** Ninguno
- **Pendientes consolidados:**
  - [ ] Completar `manifiesto.md` y definir requerimientos iniciales.
- **Siguiente acción:** Completar manifiesto del proyecto.

---

## 2. Decisiones Técnicas y ADRs
- Ninguna decisión arquitectónica registrada aún.

---

## 3. Historial Reciente (Ventana Deslizante: Últimas 5 Sesiones)

### [{ahora}] Inicialización
- **ID Evento:** `{ev_init}`
- **Agente:** Director de Proyecto / Asistente Principal
- **Tareas completadas:** Estructura de proyecto y memoria inicializadas con éxito.
- **Archivos afectados:** Ninguno
- **Decisiones técnicas:** Ninguna
- **Pendientes:** Completar `manifiesto.md` y definir requerimientos iniciales.
- **Riesgos:** Ninguno.

---

## 4. Hitos Anteriores (Bitácora Compactada)
"""
        rutas["memoria_md"].write_text(contenido_inicial, encoding="utf-8")

    # 2. Timeline JSONL estructurado
    if not rutas["cloudmem"].exists():
        rutas["cloudmem"].write_text("", encoding="utf-8")
    if not rutas["timeline"].exists():
        rutas["timeline"].write_text("", encoding="utf-8")

    # 3. Soporte legacy opcional (si cryptography está disponible)
    fernet = _obtener_fernet_opcional(rutas, crear=True)
    if fernet and not rutas["mem_palace"].exists():
        contenido_legacy = f"""[MEMORIA DE PROYECTO: {proyecto.name}]
- Fecha: {ahora_iso()}
- Tareas completadas: Inicialización de memoria del proyecto.
- Pendientes: Completar manifiesto del proyecto.
"""
        rutas["mem_palace"].write_bytes(fernet.encrypt(contenido_legacy.encode("utf-8")))

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
    if rutas["memoria_md"].exists():
        texto = rutas["memoria_md"].read_text(encoding="utf-8")
        if texto.strip():
            return texto

    if rutas["mem_palace"].exists():
        fernet = _obtener_fernet_opcional(rutas)
        if fernet:
            try:
                return fernet.decrypt(rutas["mem_palace"].read_bytes()).decode("utf-8")
            except Exception:
                pass
    return ""


# ─────────────────────────────────────────────────────────────────────────────
# PARSER ROBUSTO Y GESTIÓN DE SECCIONES
# ─────────────────────────────────────────────────────────────────────────────

def analizar_memoria(contenido: str) -> dict:
    """
    Parsea memoria.md respetando bloques de código (```).
    Separa cabecera, Estado Activo (Sección 1), Decisiones (Sección 2),
    Sesiones recientes (Sección 3) e Hitos compactados (Sección 4).
    """
    if not contenido or not contenido.strip():
        return {
            "cabecera": "",
            "estado_activo": "",
            "decisiones": "",
            "sesiones_recientes": [],
            "hitos_anteriores": [],
            "es_legacy": False,
        }

    lineas = contenido.splitlines()
    in_code_block = False

    # Estructura de secciones
    idx_s1 = -1
    idx_s2 = -1
    idx_s3 = -1
    idx_s4 = -1

    for i, linea in enumerate(lineas):
        strip_l = linea.strip()
        if strip_l.startswith("```") or strip_l.startswith("~~~"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Detectar encabezados de nivel 2 fuera de bloques de código
        if re.match(r"^##\s+1\.\s+", strip_l):
            idx_s1 = i
        elif re.match(r"^##\s+2\.\s+", strip_l):
            idx_s2 = i
        elif re.match(r"^##\s+3\.\s+", strip_l):
            idx_s3 = i
        elif re.match(r"^##\s+4\.\s+", strip_l):
            idx_s4 = i

    # Si no se detectan secciones estándar, tratar como memoria plana / legacy
    if idx_s1 == -1 and idx_s3 == -1:
        # Buscar si al menos hay sesiones ### [
        matches_sesion = []
        in_code_block = False
        for i, linea in enumerate(lineas):
            strip_l = linea.strip()
            if strip_l.startswith("```") or strip_l.startswith("~~~"):
                in_code_block = not in_code_block
                continue
            if not in_code_block and re.match(r"^###\s+\[", strip_l):
                matches_sesion.append(i)

        if not matches_sesion:
            return {
                "cabecera": contenido.strip(),
                "estado_activo": "",
                "decisiones": "",
                "sesiones_recientes": [],
                "hitos_anteriores": [],
                "es_legacy": True,
            }

    # Delimitar cabecera
    primer_corte = min([idx for idx in (idx_s1, idx_s2, idx_s3, idx_s4) if idx != -1] or [len(lineas)])
    cabecera = "\n".join(lineas[:primer_corte]).strip()
    cabecera = re.sub(r"\n+---\s*$", "", cabecera).strip()

    # Extraer secciones intermedias
    def _slice_clean(start: int, end: int) -> str:
        if start == -1 or start >= len(lineas):
            return ""
        s = "\n".join(lineas[start:end]).strip()
        return re.sub(r"\n+---\s*$", "", s).strip()

    fin_s1 = min([x for x in (idx_s2, idx_s3, idx_s4) if x > idx_s1] or [len(lineas)]) if idx_s1 != -1 else -1
    estado_activo = _slice_clean(idx_s1, fin_s1) if idx_s1 != -1 else ""

    fin_s2 = min([x for x in (idx_s3, idx_s4) if x > idx_s2] or [len(lineas)]) if idx_s2 != -1 else -1
    decisiones = _slice_clean(idx_s2, fin_s2) if idx_s2 != -1 else ""

    # Extraer Hitos Anteriores (Sección 4)
    hitos: list[str] = []
    if idx_s4 != -1:
        in_code_block = False
        for linea in lineas[idx_s4 + 1:]:
            strip_l = linea.strip()
            if strip_l.startswith("```") or strip_l.startswith("~~~"):
                in_code_block = not in_code_block
                continue
            if not in_code_block and strip_l.startswith("- ["):
                hitos.append(strip_l)

    # Extraer Sesiones Recientes (Sección 3)
    sesiones: list[str] = []
    rango_s3_inicio = idx_s3 + 1 if idx_s3 != -1 else primer_corte
    rango_s3_fin = idx_s4 if idx_s4 != -1 else len(lineas)

    in_code_block = False
    puntos_corte_sesiones = []
    for i in range(rango_s3_inicio, rango_s3_fin):
        strip_l = lineas[i].strip()
        if strip_l.startswith("```") or strip_l.startswith("~~~"):
            in_code_block = not in_code_block
            continue
        if not in_code_block and re.match(r"^###\s+\[", strip_l):
            puntos_corte_sesiones.append(i)

    for idx_match, pos in enumerate(puntos_corte_sesiones):
        pos_sig = puntos_corte_sesiones[idx_match + 1] if idx_match + 1 < len(puntos_corte_sesiones) else rango_s3_fin
        bloque = "\n".join(lineas[pos:pos_sig]).strip()
        bloque = re.sub(r"\n+---\s*$", "", bloque).strip()
        if bloque:
            sesiones.append(bloque)

    return {
        "cabecera": cabecera,
        "estado_activo": estado_activo,
        "decisiones": decisiones,
        "sesiones_recientes": sesiones,
        "hitos_anteriores": hitos,
        "es_legacy": False,
    }


def compactar_sesion_a_hito(bloque_sesion: str, evento_id: str = "") -> str:
    """Convierte un bloque de sesión detallada en un hito sintético de una línea con referencia."""
    m_fecha = re.search(r"###\s+\[([^\]]+)\]", bloque_sesion)
    fecha = m_fecha.group(1) if m_fecha else ahora_iso()

    m_ev = re.search(r"-\s+\*\*ID Evento:\*\*\s*`?([a-zA-Z0-9_-]+)`?", bloque_sesion)
    ev_id = evento_id or (m_ev.group(1).strip() if m_ev else generar_evento_id(fecha))

    m_agente = re.search(r"-\s+\*\*Agente:\*\*\s*(.*)", bloque_sesion)
    agente = m_agente.group(1).strip() if m_agente else "Agente"

    m_tareas = re.search(r"-\s+\*\*Tareas(?: completadas)?:\*\*\s*(.*)", bloque_sesion)
    tareas = m_tareas.group(1).strip() if m_tareas else "Tarea realizada"
    if len(tareas) > 120:
        tareas = tareas[:117] + "..."

    m_archivos = re.search(r"-\s+\*\*Archivos afectados:\*\*\s*(.*)", bloque_sesion)
    archivos_str = m_archivos.group(1).strip() if m_archivos else ""
    if archivos_str and archivos_str.lower() != "ninguno":
        num_archivos = len([a for a in archivos_str.split(",") if a.strip()])
        arch_info = f" ({num_archivos} archivo{'s' if num_archivos != 1 else ''})"
    else:
        arch_info = ""

    return f"- [{fecha}] [{ev_id}] ({agente}) {tareas}{arch_info} — Ref: timeline#{ev_id}"


def _extraer_campos_sesion(bloque_sesion: str) -> dict:
    """Extrae campos estructurados de un bloque Markdown de sesión."""
    m_fecha = re.search(r"###\s+\[([^\]]+)\]", bloque_sesion)
    fecha = m_fecha.group(1) if m_fecha else ahora_iso()

    m_ev = re.search(r"-\s+\*\*ID Evento:\*\*\s*`?([a-zA-Z0-9_-]+)`?", bloque_sesion)
    ev_id = m_ev.group(1).strip() if m_ev else generar_evento_id(fecha)

    m_agente = re.search(r"-\s+\*\*Agente:\*\*\s*(.*)", bloque_sesion)
    agente = m_agente.group(1).strip() if m_agente else "Agente"

    m_tareas = re.search(r"-\s+\*\*Tareas(?: completadas)?:\*\*\s*(.*)", bloque_sesion)
    tareas = m_tareas.group(1).strip() if m_tareas else ""

    m_archivos = re.search(r"-\s+\*\*Archivos afectados:\*\*\s*(.*)", bloque_sesion)
    archivos_raw = m_archivos.group(1).strip() if m_archivos else ""
    archivos = [a.strip(" `") for a in archivos_raw.split(",") if a.strip() and a.lower() != "ninguno"]

    m_dec = re.search(r"-\s+\*\*Decisiones(?: técnicas)?:\*\*\s*(.*)", bloque_sesion)
    decisiones = m_dec.group(1).strip() if m_dec else ""
    if decisiones.lower() in ("ninguna", "ninguno"):
        decisiones = ""

    m_pend = re.search(r"-\s+\*\*Pendientes(?:\s+generados)?:\*\*\s*(.*)", bloque_sesion)
    pendientes = m_pend.group(1).strip() if m_pend else ""
    if pendientes.lower() in ("ninguno", "ninguna"):
        pendientes = ""

    m_riesgos = re.search(r"-\s+\*\*Riesgos(?: identificados)?:\*\*\s*(.*)", bloque_sesion)
    riesgos = m_riesgos.group(1).strip() if m_riesgos else ""
    if riesgos.lower() in ("ninguno", "ninguna"):
        riesgos = ""

    return {
        "evento_id": ev_id,
        "fecha": fecha,
        "agente": agente,
        "resumen": tareas,
        "archivos": archivos,
        "decisiones": decisiones,
        "pendientes": pendientes,
        "riesgos": riesgos,
    }


def consolidar_estado_activo(
    estado_previo: str,
    nuevas_sesiones: list[str],
    pendientes_resueltos: list[str] | None = None,
) -> str:
    """
    Consolida el bloque de Estado Activo garantizando que los pendientes
    abiertos y restricciones no se pierdan, marcando los resueltos.
    """
    pendientes_resueltos_set = {p.strip().lower() for p in (pendientes_resueltos or []) if p.strip()}
    
    # Extraer pendientes existentes
    pendientes_abiertos: list[str] = []
    if estado_previo:
        for linea in estado_previo.splitlines():
            m_pend = re.match(r"^\s*-\s*\[([ xX])\]\s*(.*)", linea)
            if m_pend:
                marcado = m_pend.group(1).strip().lower() == "x"
                texto_p = m_pend.group(2).strip()
                if not marcado and texto_p.lower() not in pendientes_resueltos_set:
                    if texto_p not in pendientes_abiertos:
                        pendientes_abiertos.append(texto_p)

    # Extraer nuevos pendientes de las sesiones
    for s in nuevas_sesiones:
        datos = _extraer_campos_sesion(s)
        if datos["pendientes"]:
            for item in re.split(r"[;\n]", datos["pendientes"]):
                item_limpio = item.strip().lstrip("-* ").strip()
                if item_limpio and item_limpio.lower() not in ("ninguno", "ninguna"):
                    if item_limpio.lower() not in pendientes_resueltos_set and item_limpio not in pendientes_abiertos:
                        pendientes_abiertos.append(item_limpio)

    # Reconstruir bloque de Estado Activo
    lineas_salida = ["## 1. Estado Activo y Criterios Vigentes"]
    m_obj = re.search(r"-\s+\*\*Objetivo actual:\*\*\s*(.*)", estado_previo) if estado_previo else None
    obj = m_obj.group(1).strip() if m_obj else "Alcance activo en progreso."
    lineas_salida.append(f"- **Objetivo actual:** {obj}")

    m_hito = re.search(r"-\s+\*\*Hito/Sprint:\*\*\s*(.*)", estado_previo) if estado_previo else None
    hito = m_hito.group(1).strip() if m_hito else "En curso"
    lineas_salida.append(f"- **Hito/Sprint:** {hito}")

    m_tarea = re.search(r"-\s+\*\*Tarea en curso:\*\*\s*(.*)", estado_previo) if estado_previo else None
    tarea = m_tarea.group(1).strip() if m_tarea else "Ninguna"
    lineas_salida.append(f"- **Tarea en curso:** {tarea}")

    m_restr = re.search(r"-\s+\*\*Restricciones y bloqueos:\*\*\s*(.*)", estado_previo) if estado_previo else None
    restr = m_restr.group(1).strip() if m_restr else "Ninguno"
    lineas_salida.append(f"- **Restricciones y bloqueos:** {restr}")

    lineas_salida.append("- **Pendientes consolidados:**")
    if pendientes_abiertos:
        for p in pendientes_abiertos:
            lineas_salida.append(f"  - [ ] {p}")
    else:
        lineas_salida.append("  - Ninguno")

    m_sig = re.search(r"-\s+\*\*Siguiente acción:\*\*\s*(.*)", estado_previo) if estado_previo else None
    sig = m_sig.group(1).strip() if m_sig else (pendientes_abiertos[0] if pendientes_abiertos else "Continuar según plan.")
    lineas_salida.append(f"- **Siguiente acción:** {sig}")

    return "\n".join(lineas_salida)


def consolidar_decisiones(
    decisiones_previas: str,
    nuevas_sesiones: list[str],
    decisiones_sustituidas: list[str] | None = None,
) -> str:
    """
    Consolida las decisiones vigentes para que no desaparezcan al rotar sesiones.
    Soporta ciclo de vida de ADRs: las decisiones sustituidas explícitamente se retiran
    de las decisiones activas para prevenir directivas contradictorias al LLM.
    """
    sustituidas_set = {s.strip().lower() for s in (decisiones_sustituidas or []) if s.strip()}
    lineas_existentes = []
    if decisiones_previas:
        for l in decisiones_previas.splitlines():
            s = l.strip()
            if s and not s.startswith("##") and s.lower() != "- ninguna decisión arquitectónica registrada aún.":
                es_sustituida = any(sust in s.lower() for sust in sustituidas_set)
                if not es_sustituida and s not in lineas_existentes:
                    lineas_existentes.append(s)

    for s in nuevas_sesiones:
        datos = _extraer_campos_sesion(s)
        if datos["decisiones"]:
            for item in re.split(r"[;\n]", datos["decisiones"]):
                item_limpio = item.strip()
                if item_limpio and item_limpio.lower() not in ("ninguna", "ninguno"):
                    formateado = f"- {item_limpio}" if not item_limpio.startswith("-") else item_limpio
                    es_sustituida = any(sust in formateado.lower() for sust in sustituidas_set)
                    if not es_sustituida and formateado not in lineas_existentes:
                        lineas_existentes.append(formateado)

    lineas_salida = ["## 2. Decisiones Técnicas y ADRs"]
    if lineas_existentes:
        lineas_salida.extend(lineas_existentes)
    else:
        lineas_salida.append("- Ninguna decisión arquitectónica registrada aún.")
    return "\n".join(lineas_salida)


def _compactar_hitos_en_epocas(hitos: list[str], max_hitos: int = 8) -> list[str]:
    """
    Compresión jerárquica multinivel (L3 Épocas / Fases):
    Si la lista de hitos de una línea supera max_hitos, compacta los hitos más antiguos
    en una entrada consolidada de época para mantener acotado el crecimiento del contexto a O(1).
    """
    if len(hitos) <= max_hitos:
        return hitos

    exceso = len(hitos) - (max_hitos - 1)
    a_consolidar = hitos[:exceso]
    recientes = hitos[exceso:]

    eventos = re.findall(r"\[(ev_[a-zA-Z0-9_]+)\]", "\n".join(a_consolidar))
    rango_ev = f"{eventos[0]} a {eventos[-1]}" if len(eventos) >= 2 else (eventos[0] if eventos else "historial consolidado")

    resumenes = []
    for h in a_consolidar:
        limpio = re.sub(r"^\s*-\s*\[.*?\]\s*", "", h).strip()
        limpio = re.sub(r"—\s*Ref:.*", "", limpio).strip()
        if limpio and limpio not in resumenes:
            resumenes.append(limpio)

    sintesis = "; ".join(resumenes[:3])
    if len(resumenes) > 3:
        sintesis += f" (+{len(resumenes) - 3} tareas previas)"

    hito_epoca = f"- **[Época Consolidada: {len(a_consolidar)} sesiones]** {sintesis} — Ref: {rango_ev}"
    return [hito_epoca] + recientes


def _respaldar_sesion_en_timeline(proyecto: Path, datos_sesion: dict) -> None:
    """Comprueba si la sesión existe en timeline.jsonl; si no, la archiva de forma durable."""
    rutas = rutas_memoria(proyecto)
    ev_id = datos_sesion["evento_id"]
    
    # Comprobar presencia en timeline
    encontrado = False
    if rutas["timeline"].exists():
        for linea in rutas["timeline"].read_text(encoding="utf-8").splitlines():
            if not linea.strip():
                continue
            try:
                e = json.loads(linea)
                if e.get("evento_id") == ev_id or (e.get("fecha") == datos_sesion["fecha"] and e.get("resumen") == datos_sesion["resumen"]):
                    encontrado = True
                    break
            except json.JSONDecodeError:
                continue

    if not encontrado:
        entrada = {
            "evento_id": ev_id,
            "version": 2,
            "fecha": datos_sesion["fecha"],
            "agente": datos_sesion["agente"],
            "tipo": "historico_respaldado",
            "resumen": datos_sesion["resumen"],
            "archivos": datos_sesion["archivos"],
            "decisiones": datos_sesion["decisiones"],
            "pendientes": datos_sesion["pendientes"],
            "riesgos": datos_sesion["riesgos"],
        }
        linea_json = json.dumps(entrada, ensure_ascii=False) + "\n"
        with rutas["timeline"].open("a", encoding="utf-8") as f:
            f.write(linea_json)
            f.flush()
            os.fsync(f.fileno())
        if rutas["cloudmem"].exists():
            with rutas["cloudmem"].open("a", encoding="utf-8") as f:
                f.write(linea_json)
                f.flush()
                os.fsync(f.fileno())


def rotar_memoria(
    proyecto: Path,
    max_sesiones: int = 5,
    presupuesto_tokens: int | None = None,
    pendientes_resueltos: list[str] | None = None,
    decisiones_sustituidas: list[str] | None = None,
) -> None:
    """
    Mantiene la ventana deslizante compactando sesiones excedentes a hitos de 1 línea.
    Garantiza:
    1. Respaldo previo íntegro en timeline.jsonl antes de compactar (cero pérdida de datos).
    2. Idempotencia total: ejecuciones repetidas producen exactamente el mismo contenido.
    3. Preservación del Estado Activo y Decisiones vigentes con ciclo de vida de ADRs.
    4. Compresión jerárquica multinivel de hitos en épocas acotadas.
    """
    rutas = inicializar(proyecto)
    with bloqueo_proyecto(rutas["base"]):
        if not rutas["memoria_md"].exists():
            return
        contenido = rutas["memoria_md"].read_text(encoding="utf-8")
        parsed = analizar_memoria(contenido)

        sesiones = parsed["sesiones_recientes"]
        hitos = parsed["hitos_anteriores"]

        # Recopilar todos los pendientes resueltos y decisiones sustituidas de timeline.jsonl
        resueltos_acumulados = set()
        sustituidas_acumuladas = set()
        if pendientes_resueltos:
            resueltos_acumulados.update(p.strip().lower() for p in pendientes_resueltos if p.strip())
        if decisiones_sustituidas:
            sustituidas_acumuladas.update(d.strip().lower() for d in decisiones_sustituidas if d.strip())

        if rutas["timeline"].exists():
            try:
                for linea in rutas["timeline"].read_text(encoding="utf-8").splitlines():
                    if not linea.strip():
                        continue
                    try:
                        obj = json.loads(linea)
                        for pr in obj.get("pendientes_resueltos", []):
                            if pr and pr.strip():
                                resueltos_acumulados.add(pr.strip().lower())
                        for ds in obj.get("decisiones_sustituidas", []):
                            if ds and ds.strip():
                                sustituidas_acumuladas.add(ds.strip().lower())
                    except Exception:
                        continue
            except Exception:
                pass

        if len(sesiones) <= max_sesiones:
            for s in sesiones:
                d = _extraer_campos_sesion(s)
                _respaldar_sesion_en_timeline(proyecto, d)
            sesiones_conservadas = sesiones
            hitos_finales = _compactar_hitos_en_epocas(hitos)
        else:
            exceso = len(sesiones) - max_sesiones
            sesiones_a_compactar = sesiones[:exceso]
            sesiones_conservadas = sesiones[exceso:]

            nuevos_hitos = []
            for s in sesiones_a_compactar:
                d = _extraer_campos_sesion(s)
                _respaldar_sesion_en_timeline(proyecto, d)
                hito = compactar_sesion_a_hito(s, evento_id=d["evento_id"])
                if hito not in hitos and not any(f"[{d['evento_id']}]" in h for h in hitos):
                    nuevos_hitos.append(hito)
            hitos_finales = _compactar_hitos_en_epocas(hitos + nuevos_hitos)

        # Consolidar estado activo y decisiones con el historial completo
        estado_activo = consolidar_estado_activo(
            parsed["estado_activo"], sesiones, pendientes_resueltos=list(resueltos_acumulados)
        )
        decisiones = consolidar_decisiones(
            parsed["decisiones"], sesiones, decisiones_sustituidas=list(sustituidas_acumuladas)
        )

        cabecera = parsed["cabecera"]
        if not cabecera:
            cabecera = f"# Memoria del Proyecto: {proyecto.name}\n\n- **ID de Proyecto:** `{proyecto.name}`\n- **Estado general:** Activo"

        nuevo_texto = f"{cabecera}\n\n---\n\n{estado_activo}\n\n---\n\n{decisiones}\n\n---\n\n"
        nuevo_texto += f"## 3. Historial Reciente (Ventana Deslizante: Últimas {max_sesiones} Sesiones)\n\n"
        nuevo_texto += "\n\n---\n\n".join(sesiones_conservadas)
        nuevo_texto += "\n\n---\n\n## 4. Hitos Anteriores (Bitácora Compactada)\n"
        if hitos_finales:
            nuevo_texto += "\n".join(hitos_finales) + "\n"

        if nuevo_texto.strip() != contenido.strip():
            _escritura_atomica(rutas["memoria_md"], nuevo_texto)

            # Actualizar legacy Fernet si aplica
            fernet = _obtener_fernet_opcional(rutas)
            if fernet:
                try:
                    rutas["mem_palace"].write_bytes(fernet.encrypt(nuevo_texto.encode("utf-8")))
                except Exception:
                    pass



def leer_memoria_enfocada(proyecto: Path, presupuesto_tokens: int = 4000) -> str:
    """
    Devuelve la memoria optimizada para LLM (omitiendo la bitácora histórica extensa).
    Aplica política de selección y acota el contenido al presupuesto configurado sin truncar requisitos críticos.
    """
    rutas = rutas_memoria(proyecto)
    if not rutas["memoria_md"].exists():
        return ""
    contenido = rutas["memoria_md"].read_text(encoding="utf-8")
    parsed = analizar_memoria(contenido)

    # Si es formato legacy plano o sin sesiones, devolver contenido completo
    if parsed["es_legacy"] or not parsed["sesiones_recientes"]:
        return contenido

    cabecera = parsed["cabecera"]
    estado = parsed["estado_activo"] or "## 1. Estado Activo\n- **Objetivo actual:** Trabajo en curso."
    decs = parsed["decisiones"] or "## 2. Decisiones Técnicas\n- Ninguna decisión registrada aún."
    sesiones = list(parsed["sesiones_recientes"])

    base_texto = f"{cabecera}\n\n---\n\n{estado}\n\n---\n\n{decs}\n\n---\n\n## 3. Historial Reciente (Últimas sesiones)\n\n"
    
    texto_completo = base_texto + "\n\n---\n\n".join(sesiones)
    if estimar_tokens(texto_completo) <= presupuesto_tokens:
        return texto_completo.strip()

    # Si excede el presupuesto, comprimir las sesiones más antiguas dentro de la ventana
    # manteniendo la más reciente completa
    for i in range(len(sesiones) - 1):
        d = _extraer_campos_sesion(sesiones[i])
        resumen_comprimido = (
            f"### [{d['fecha']}] Sesión: `{d['evento_id']}` | Agente: {d['agente']}\n"
            f"- **ID Evento:** `{d['evento_id']}`\n"
            f"- **Tareas:** {d['resumen'][:80]}...\n"
            f"- **Ref:** timeline#{d['evento_id']}"
        )
        sesiones[i] = resumen_comprimido
        candidato = base_texto + "\n\n---\n\n".join(sesiones)
        if estimar_tokens(candidato) <= presupuesto_tokens:
            return candidato.strip()

    return (base_texto + "\n\n---\n\n".join(sesiones)).strip()


def guardar_mem_palace(proyecto: Path, informe_texto: str, acumular: bool = True) -> None:
    """Actualiza memoria.md integrando la sesión en la estructura jerárquica."""
    rutas = inicializar(proyecto)
    with bloqueo_proyecto(rutas["base"]):
        if rutas["memoria_md"].exists() and acumular:
            previo = rutas["memoria_md"].read_text(encoding="utf-8")
            parsed = analizar_memoria(previo)
            if not parsed["es_legacy"] and (parsed["sesiones_recientes"] or parsed["estado_activo"]):
                # Integrar nueva sesión en Sección 3
                parsed["sesiones_recientes"].append(informe_texto.strip())
                # Consolidar estado activo y decisiones
                estado_activo = consolidar_estado_activo(parsed["estado_activo"], [informe_texto])
                decisiones = consolidar_decisiones(parsed["decisiones"], [informe_texto])

                cabecera = parsed["cabecera"]
                if not cabecera:
                    cabecera = f"# Memoria del Proyecto: {proyecto.name}\n\n- **ID de Proyecto:** `{proyecto.name}`\n- **Estado general:** Activo"

                nuevo = f"{cabecera}\n\n---\n\n{estado_activo}\n\n---\n\n{decisiones}\n\n---\n\n"
                nuevo += "## 3. Historial Reciente (Ventana Deslizante: Últimas sesiones)\n\n"
                nuevo += "\n\n---\n\n".join(parsed["sesiones_recientes"])
                if parsed["hitos_anteriores"]:
                    nuevo += "\n\n---\n\n## 4. Hitos Anteriores (Bitácora Compactada)\n"
                    nuevo += "\n".join(parsed["hitos_anteriores"])
                nuevo += "\n"
            else:
                nuevo = f"{previo.rstrip()}\n\n---\n\n{informe_texto}\n"
        else:
            nuevo = informe_texto
        _escritura_atomica(rutas["memoria_md"], nuevo)

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
    evento_id: str = "",
    pendientes_resueltos: list[str] | None = None,
    decisiones_sustituidas: list[str] | None = None,
) -> str:
    """Registra una entrada estructurada en cloudmem.jsonl y timeline.jsonl."""
    rutas = inicializar(proyecto)
    fecha = ahora_iso()
    ev_id = evento_id or generar_evento_id(fecha, agente, resumen)

    entrada = {
        "evento_id": ev_id,
        "version": 2,
        "fecha": fecha,
        "agente": agente,
        "tipo": tipo,
        "resumen": resumen,
        "archivos": archivos,
        "decisiones": decisiones,
        "pendientes": pendientes,
        "pendientes_resueltos": pendientes_resueltos or [],
        "decisiones_sustituidas": decisiones_sustituidas or [],
        "riesgos": riesgos,
    }
    linea = json.dumps(entrada, ensure_ascii=False) + "\n"
    with bloqueo_proyecto(rutas["base"]):
        with rutas["timeline"].open("a", encoding="utf-8") as f:
            f.write(linea)
            f.flush()
            os.fsync(f.fileno())
        with rutas["cloudmem"].open("a", encoding="utf-8") as f:
            f.write(linea)
            f.flush()
            os.fsync(f.fileno())

    return ev_id


def leer_cloudmem(proyecto: Path, limite: int = 8, filtro: str = "") -> list[dict]:
    """Lee las últimas entradas de cloudmem/timeline tolerando líneas incompletas o corruptas."""
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


def _tokenizar_bm25(texto: str) -> list[str]:
    """Tokeniza texto para búsqueda semántica/léxica eliminando puntuación y stopwords comunes."""
    texto_split = re.sub(r"([a-z])([A-Z])", r"\1 \2", texto)
    tokens = re.findall(r"\b[\w\-#]{2,}\b", texto_split.lower())
    stopwords = {
        "de", "la", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un", "para", "con", "no", "una",
        "su", "al", "lo", "como", "mas", "pero", "sus", "le", "ya", "o", "fue", "este", "ha", "si", "porque",
        "esta", "son", "entre", "esta", "cuando", "muy", "sin", "sobre", "ser", "tiene", "tambien", "me", "hasta",
        "hay", "donde", "quien", "desde", "todo", "nos", "durante", "todos", "uno", "les", "ni", "contra", "otros",
        "ese", "eso", "ante", "ellos", "e", "esto", "mi", "antes", "algunos", "que", "the", "and", "is", "in", "to",
        "of", "for", "with", "on", "at", "by", "from", "an", "be", "as", "it"
    }
    return [t for t in tokens if t not in stopwords]


def _calcular_bm25(corpus: list[str], consulta: str, k1: float = 1.5, b: float = 0.75) -> list[float]:
    """Calcula la relevancia probabilística BM25 para cada documento del corpus ante una consulta."""
    tokens_consulta = _tokenizar_bm25(consulta)
    if not tokens_consulta:
        return [0.0] * len(corpus)

    corpus_tokens = [_tokenizar_bm25(doc) for doc in corpus]
    n_docs = len(corpus_tokens)
    if n_docs == 0:
        return []

    doc_lens = [len(doc) for doc in corpus_tokens]
    avgdl = sum(doc_lens) / n_docs if n_docs > 0 else 1.0

    df = Counter()
    for doc in corpus_tokens:
        unique_tokens = set(doc)
        for t in tokens_consulta:
            if t in unique_tokens:
                df[t] += 1

    idf = {}
    for t in tokens_consulta:
        n_q = df.get(t, 0)
        idf[t] = math.log(1.0 + (n_docs - n_q + 0.5) / (n_q + 0.5))

    scores = []
    for i, doc in enumerate(corpus_tokens):
        score = 0.0
        doc_len = doc_lens[i]
        tf_counter = Counter(doc)
        for t in tokens_consulta:
            tf = tf_counter.get(t, 0)
            if tf > 0:
                denominador = tf + k1 * (1.0 - b + b * (doc_len / avgdl))
                score += idf[t] * ((tf * (k1 + 1.0)) / denominador)
        scores.append(score)
    return scores


def recuperar_historia(
    proyecto: Path,
    query: str = "",
    evento_id: str = "",
    archivo: str = "",
    desde: str = "",
    hasta: str = "",
    limite: int = 10,
) -> list[dict]:
    """
    Recupera eventos específicos del historial completo sin cargar la memoria entera.
    Filtra por ID de evento, palabra clave (con ranking probabilístico BM25), archivo o rango de fechas.
    """
    rutas = rutas_memoria(proyecto)
    fuente = rutas["timeline"] if rutas["timeline"].exists() and rutas["timeline"].stat().st_size else rutas["cloudmem"]
    if not fuente.exists():
        return []

    candidatos: list[dict] = []
    query_lower = query.lower().strip()
    archivo_lower = archivo.lower().strip()

    for linea in fuente.read_text(encoding="utf-8").splitlines():
        if not linea.strip():
            continue
        try:
            e = json.loads(linea)
        except json.JSONDecodeError:
            continue

        if evento_id and e.get("evento_id") != evento_id:
            continue

        if archivo_lower:
            archivos_e = [str(a).lower() for a in e.get("archivos", [])]
            if not any(archivo_lower in a for a in archivos_e):
                continue

        if desde and e.get("fecha", "") < desde:
            continue
        if hasta and e.get("fecha", "") > hasta:
            continue

        candidatos.append(e)

    if not candidatos:
        return []

    # Si hay consulta textual, aplicar ranking BM25 + coincidencia de subcadena exacta
    if query_lower:
        exact_matches = [e for e in candidatos if query_lower in json.dumps(e, ensure_ascii=False).lower()]
        pool = exact_matches if exact_matches else candidatos

        corpus = []
        for e in pool:
            archs = " ".join(e.get("archivos", []))
            doc = f"{e.get('evento_id', '')} {e.get('agente', '')} {e.get('resumen', '')} {e.get('decisiones', '')} {e.get('pendientes', '')} {e.get('riesgos', '')} {archs}"
            corpus.append(doc)

        scores = _calcular_bm25(corpus, query_lower)
        parejas = []
        for idx, e in enumerate(pool):
            sc = scores[idx] if idx < len(scores) else 0.0
            dump_e = json.dumps(e, ensure_ascii=False).lower()
            if query_lower in dump_e:
                sc += 10.0  # Boost para coincidencia textual exacta
            if sc > 0 or exact_matches:
                parejas.append((sc, e))

        parejas.sort(key=lambda x: x[0], reverse=True)
        res = []
        for sc, e in parejas[:limite]:
            e_res = dict(e)
            e_res["score_relevancia"] = round(sc, 4)
            res.append(e_res)
        return res

    return candidatos[-limite:]



def reconstruir_memoria(proyecto: Path, reparar_archivo: bool = False) -> str:
    """
    Reconstruye memoria.md desde timeline.jsonl garantizando la continuidad de
    decisiones vigentes, pendientes abiertos y las últimas sesiones detalladas.
    """
    rutas = rutas_memoria(proyecto)
    if not rutas["timeline"].exists():
        return ""

    entradas = []
    for l in rutas["timeline"].read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        try:
            entradas.append(json.loads(l))
        except json.JSONDecodeError:
            continue

    if not entradas:
        return ""

    # Reconstruir estado activo y decisiones
    sesiones_markdown = []
    for e in entradas:
        ev_id = e.get("evento_id") or generar_evento_id(e.get("fecha"))
        archs_str = ", ".join(f"`{a}`" for a in e.get("archivos", [])) if e.get("archivos") else "Ninguno"
        bloque = f"""### [{e.get('fecha', ahora_iso())}] {e.get('tipo', 'operativo').capitalize()}: `{ev_id}`
- **ID Evento:** `{ev_id}`
- **Agente:** {e.get('agente', 'Asistente Principal')}
- **Tareas completadas:** {e.get('resumen', '')}
- **Archivos afectados:** {archs_str}
- **Decisiones técnicas:** {e.get('decisiones') or 'Ninguna'}
- **Pendientes:** {e.get('pendientes') or 'Ninguno'}
- **Riesgos:** {e.get('riesgos') or 'Ninguno'}
"""
        sesiones_markdown.append(bloque.strip())

    estado_activo = consolidar_estado_activo("", sesiones_markdown)
    decisiones = consolidar_decisiones("", sesiones_markdown)

    max_sesiones = 5
    if len(sesiones_markdown) > max_sesiones:
        sesiones_recientes = sesiones_markdown[-max_sesiones:]
        hitos = [compactar_sesion_a_hito(s) for s in sesiones_markdown[:-max_sesiones]]
    else:
        sesiones_recientes = sesiones_markdown
        hitos = []

    cabecera = f"""# Memoria del Proyecto: {proyecto.name}

- **ID de Proyecto:** `{proyecto.name}`
- **Fecha de creación:** {entradas[0].get('fecha', ahora_iso())}
- **Estado general:** Activo (Reconstruido)
"""
    nuevo_texto = f"{cabecera}\n\n---\n\n{estado_activo}\n\n---\n\n{decisiones}\n\n---\n\n"
    nuevo_texto += f"## 3. Historial Reciente (Ventana Deslizante: Últimas {max_sesiones} Sesiones)\n\n"
    nuevo_texto += "\n\n---\n\n".join(sesiones_recientes)
    if hitos:
        nuevo_texto += "\n\n---\n\n## 4. Hitos Anteriores (Bitácora Compactada)\n"
        nuevo_texto += "\n".join(hitos) + "\n"

    if reparar_archivo:
        with bloqueo_proyecto(rutas["base"]):
            _escritura_atomica(rutas["memoria_md"], nuevo_texto)

    return nuevo_texto


_LOCKS_HELD = threading.local()


@contextmanager
def bloqueo_proyecto(base: Path):
    """Serializa operaciones de lectura/escritura por proyecto sin dependencias externas.
    Soporta reentrancia dentro del mismo proceso/hilo para evitar interbloqueos anidados."""
    base.mkdir(parents=True, exist_ok=True)
    lock_path = (base / ".lock").resolve()
    if lock_path.is_symlink():
        raise ValueError("El bloqueo de memoria no puede redirigirse.")

    if not hasattr(_LOCKS_HELD, "paths"):
        _LOCKS_HELD.paths = {}

    lock_key = str(lock_path)
    count = _LOCKS_HELD.paths.get(lock_key, 0)
    if count > 0:
        _LOCKS_HELD.paths[lock_key] = count + 1
        try:
            yield
        finally:
            _LOCKS_HELD.paths[lock_key] -= 1
            if _LOCKS_HELD.paths[lock_key] <= 0:
                del _LOCKS_HELD.paths[lock_key]
        return

    with lock_path.open("a+", encoding="utf-8") as lock:
        if fcntl is not None:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        _LOCKS_HELD.paths[lock_key] = 1
        try:
            yield
        finally:
            try:
                if fcntl is not None:
                    fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
            finally:
                _LOCKS_HELD.paths[lock_key] -= 1
                if _LOCKS_HELD.paths[lock_key] <= 0:
                    del _LOCKS_HELD.paths[lock_key]


def _escritura_atomica(path: Path, contenido: str) -> None:
    """Escribe un archivo mediante reemplazo atómico en el mismo directorio con fsync."""
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
        ev_info = f" [{entrada.get('evento_id')}]" if entrada.get("evento_id") else ""
        print(f"- [{entrada.get('fecha', 'sin fecha')}]{ev_info} ({entrada.get('agente', 'agente')}) {entrada.get('tipo', 'operativo')}")
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
    evento_id: str = "",
) -> str:
    """Genera un bloque de informe Markdown para memoria.md con ID de evento."""
    fecha = ahora_iso()
    ev_id = evento_id or generar_evento_id(fecha, agente, tareas)
    archivos_str = ", ".join(f"`{a}`" for a in (archivos or [])) if archivos else "Ninguno"
    return f"""### [{fecha}] Sesión: `{ev_id}` | Agente: {agente}
- **ID Evento:** `{ev_id}`
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
    consultar.add_argument("--completo", action="store_true", help="Muestra memoria completa sin recortar.")

    cerrar = subparsers.add_parser("close", help="Registra cierre en memoria del proyecto.")
    cerrar.add_argument("--tareas", required=True)
    cerrar.add_argument("--pendientes", default="")
    cerrar.add_argument("--decisiones", default="")
    cerrar.add_argument("--riesgos", default="")
    cerrar.add_argument("--cloud-resumen", default="")
    cerrar.add_argument("--archivos", default="")
    cerrar.add_argument("--tipo", default="operativo")
    cerrar.add_argument("--agente", default="agente")
    cerrar.add_argument("--resolver-pendientes", default="", help="Pendientes resueltos separados por comas.")

    rotar = subparsers.add_parser("rotate", help="Ejecuta rotación de ventana deslizante.")
    rotar.add_argument("--max-sesiones", type=int, default=5)

    hist = subparsers.add_parser("historia", help="Consulta el historial completo por filtros.")
    hist.add_argument("--query", default="")
    hist.add_argument("--evento", default="")
    hist.add_argument("--archivo", default="")
    hist.add_argument("--limite", type=int, default=10)

    reconst = subparsers.add_parser("reconstruir", help="Reconstruye memoria.md a partir de timeline.jsonl.")
    reconst.add_argument("--reparar", action="store_true", help="Sobrescribe memoria.md con la reconstrucción.")

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
        contexto = leer_mem_palace(proyecto) if args.completo else leer_memoria_enfocada(proyecto)
        if contexto:
            print("--- MEMORIA (Markdown) ---")
            print(contexto)
            print("--------------------------")
        imprimir_cloudmem(leer_cloudmem(proyecto, limite=args.limite, filtro=args.filtro))
        return

    if args.comando == "close":
        inicializar(proyecto)
        archs = lista_archivos(args.archivos)
        resueltos = lista_archivos(args.resolver_pendientes) if hasattr(args, "resolver_pendientes") else []
        resumen_linea = args.cloud_resumen or args.tareas
        
        # Anexar a timeline estructurado primero (orden transaccional seguro)
        ev_id = agregar_cloudmem(
            proyecto=proyecto,
            resumen=resumen_linea,
            archivos=archs,
            tipo=args.tipo,
            decisiones=args.decisiones,
            pendientes=args.pendientes,
            riesgos=args.riesgos,
            agente=args.agente,
            pendientes_resueltos=resueltos,
        )

        inf = informe(
            tareas=args.tareas,
            pendientes=args.pendientes,
            decisiones=args.decisiones,
            riesgos=args.riesgos,
            agente=args.agente,
            archivos=archs,
            evento_id=ev_id,
        )
        guardar_mem_palace(proyecto, inf, acumular=True)
        rotar_memoria(proyecto, max_sesiones=5)
        print(f"[✓] Cierre registrado ({ev_id}): {proyecto / 'memoria.md'}")
        return

    if args.comando == "rotate":
        rotar_memoria(proyecto, max_sesiones=args.max_sesiones)
        print(f"[✓] Ventana deslizante rotada a {args.max_sesiones} sesiones.")
        return

    if args.comando == "historia":
        eventos = recuperar_historia(
            proyecto=proyecto,
            query=args.query,
            evento_id=args.evento,
            archivo=args.archivo,
            limite=args.limite,
        )
        print(json.dumps(eventos, ensure_ascii=False, indent=2))
        return

    if args.comando == "reconstruir":
        res = reconstruir_memoria(proyecto, reparar_archivo=args.reparar)
        if args.reparar:
            print(f"[✓] Memoria reparada y reescrita en {proyecto / 'memoria.md'}")
        else:
            print(res)
        return


if __name__ == "__main__":
    main()
