#!/usr/bin/env python3
"""Notifica la finalizacion de tareas sin dependencias externas.

Uso basico:
    python3 scripts/notificar_tarea.py --tarea "Analisis Oaxaca" --estado completada

Uso para tarea 100% terminada (reproduccion total):
    python3 scripts/notificar_tarea.py --auto-completado --tarea "Implementar modulo X"

Integracion con automatizadores:
    comando_largo && python3 scripts/notificar_tarea.py --tarea "Build API"
"""

from __future__ import annotations

import argparse
import html
import os
import platform
import shutil
import subprocess
import sys
import textwrap
import time
import webbrowser
from pathlib import Path


HTML_NOTIFICACION = Path(__file__).with_name("notificacion_tarea.html")

AUDIO_COMPLETADO = "termine la tarea.mp3"

# Cache de reproductores disponibles para evitar escanear en cada llamada
_REPRODUCTORES_CACHE: list[list[str]] | None = None


def _detectar_reproductores(audio_path: Path, es_mp3: bool) -> list[list[str]]:
    """Detecta reproductores de audio disponibles en el sistema."""
    global _REPRODUCTORES_CACHE
    if _REPRODUCTORES_CACHE is not None:
        return _REPRODUCTORES_CACHE

    sistema = platform.system().lower()
    candidatos: list[list[str]] = []

    str_audio = str(audio_path)

    if sistema == "darwin":
        if es_mp3:
            candidatos.append(["afplay", str_audio])
        # Fallback macOS
        candidatos.append(["afplay", "/System/Library/Sounds/Glass.aiff"])

    elif sistema == "linux":
        if es_mp3:
            candidatos = [
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "error", str_audio],
                ["mpg123", "-q", str_audio],
                ["mpv", "--no-video", "--really-quiet", str_audio],
            ]
        candidatos += [
            ["paplay", str_audio],
            ["aplay", str_audio],
        ]
        # Fallbacks del sistema (sonidos cortos WAV/OGG)
        for fallback in [
            "/usr/share/sounds/freedesktop/stereo/complete.oga",
            "/usr/share/sounds/alsa/Front_Center.wav",
        ]:
            if Path(fallback).exists():
                candidatos.append(
                    ["paplay", fallback] if fallback.endswith(".oga")
                    else ["aplay", fallback]
                )

    elif sistema == "windows":
        if es_mp3:
            candidatos = [
                ["vlc", "-I", "dummy", "--play-and-exit", str_audio],
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "error", str_audio],
            ]
        candidatos.append(["powershell", "-NoProfile", "-Command", "[console]::beep(1200,500)"])

    # Cachear solo comandos que realmente existen
    _REPRODUCTORES_CACHE = [
        cmd for cmd in candidatos
        if cmd and shutil.which(cmd[0]) is not None
    ]
    return _REPRODUCTORES_CACHE


def mostrar_popup_topmost(titulo: str, mensaje: str) -> None:
    """Muestra una ventana emergente en primer plano absoluto usando Tkinter o fallbacks."""
    sistema = platform.system().lower()
    
    # 1. Intentar con tkinter
    try:
        import tkinter as tk
        root = tk.Tk()
        root.title(titulo)
        root.attributes("-topmost", True)
        
        # Configurar tamano y centrado
        ancho = 500
        alto = 250
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = int((ws/2) - (ancho/2))
        y = int((hs/2) - (alto/2))
        root.geometry(f'{ancho}x{alto}+{x}+{y}')
        
        root.configure(bg='#0f172a')
        
        lbl = tk.Label(root, text=mensaje, font=("Arial", 14, "bold"), fg="white", bg="#0f172a", wraplength=450, justify="center")
        lbl.pack(expand=True, fill="both", padx=20, pady=20)
        
        btn = tk.Button(root, text="ENTENDIDO", font=("Arial", 12, "bold"), bg="#f43f5e", fg="white", command=root.destroy, padx=20, pady=5)
        btn.pack(pady=20)
        
        # Forzar al frente
        root.lift()
        root.focus_force()
        root.mainloop()
        return
    except Exception:
        pass
        
    # 2. Fallbacks de sistema operativo
    try:
        if sistema == "linux":
            subprocess.run(["zenity", "--warning", "--title", titulo, "--text", mensaje, "--width=400"], check=False)
        elif sistema == "darwin":
            script = f'tell app "System Events" to display dialog "{mensaje}" with title "{titulo}" buttons {{"OK"}} default button 1 with icon caution'
            subprocess.run(["osascript", "-e", script], check=False)
        elif sistema == "windows":
            subprocess.run(["msg", "*", mensaje], check=False)
    except Exception:
        pass



def reproducir_sonido_terminal(repeticiones: int) -> None:
    """Emite campanas de terminal como respaldo multiplataforma."""
    for _ in range(max(1, repeticiones)):
        print("\a", end="", flush=True)
        time.sleep(0.25)


def reproducir_sonido_sistema(repeticiones: int, audio_filename: str = AUDIO_COMPLETADO) -> None:
    """Reproduce un archivo de audio. Busca reproductores disponibles, con fallback a pitido de terminal."""
    sistema = platform.system().lower()

    script_dir = Path(__file__).parent
    audio_path = script_dir.parent / "audios" / audio_filename
    es_mp3 = audio_filename.lower().endswith(".mp3")

    # Diagnosticar estado del archivo de audio
    if not audio_path.exists():
        print(f"  [audio] AVISO: Archivo no encontrado: {audio_path}", file=sys.stderr)
        print(f"  [audio] Usando pitido de terminal como fallback.", file=sys.stderr)
        for _ in range(max(1, repeticiones)):
            reproducir_sonido_terminal(1)
            time.sleep(0.25)
        return

    print(f"  [audio] Reproduciendo: {audio_filename} ({audio_path.stat().st_size} bytes, x{repeticiones})", file=sys.stderr, flush=True)

    comandos = _detectar_reproductores(audio_path, es_mp3)

    if not comandos:
        print(f"  [audio] No se encontraron reproductores de audio en el sistema.", file=sys.stderr)
        print(f"  [audio] Usando pitido de terminal como fallback.", file=sys.stderr)
        for _ in range(max(1, repeticiones)):
            reproducir_sonido_terminal(1)
            time.sleep(0.25)
        return

    for i in range(max(1, repeticiones)):
        if repeticiones > 1:
            print(f"  [audio] Reproduccion {i+1}/{repeticiones}...", file=sys.stderr, flush=True)
        ejecutado = False
        for comando in comandos:
            try:
                subprocess.run(
                    comando,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=30,
                )
                ejecutado = True
                break
            except (OSError, subprocess.TimeoutExpired):
                continue
        if not ejecutado:
            print(f"  [audio] Todos los reproductores fallaron. Usando pitido de terminal.", file=sys.stderr)
            reproducir_sonido_terminal(1)
        if i < repeticiones - 1:
            time.sleep(0.5)


def crear_html_notificacion(tarea: str, estado: str, mensaje: str, repeticiones: int) -> Path:
    titulo = f"Tarea {estado}: {tarea}"
    contenido = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>{html.escape(titulo)}</title>
      <style>
        body {{
          margin: 0;
          min-height: 100vh;
          display: grid;
          place-items: center;
          font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          background: linear-gradient(135deg, #0f172a, #1d4ed8 55%, #16a34a);
          color: white;
        }}
        main {{
          width: min(880px, calc(100vw - 32px));
          padding: 42px;
          border-radius: 28px;
          background: rgba(15, 23, 42, 0.82);
          box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
          text-align: center;
        }}
        .estado {{
          display: inline-block;
          margin-bottom: 18px;
          padding: 10px 16px;
          border-radius: 999px;
          background: #22c55e;
          color: #052e16;
          font-weight: 800;
          letter-spacing: 0.08em;
          text-transform: uppercase;
        }}
        h1 {{ font-size: clamp(32px, 6vw, 72px); margin: 0 0 18px; }}
        p {{ font-size: clamp(18px, 3vw, 26px); line-height: 1.4; margin: 0; }}
        .hora {{ margin-top: 26px; color: #bfdbfe; font-size: 18px; }}
      </style>
    </head>
    <body>
      <main>
        <div class="estado">{html.escape(estado)}</div>
        <h1>{html.escape(tarea)}</h1>
        <p>{html.escape(mensaje)}</p>
        <div class="hora" id="hora"></div>
      </main>
      <script>
        const repeticiones = {max(1, repeticiones)};
        document.getElementById('hora').textContent = new Date().toLocaleString('es-MX');
        function beep() {{
          const contexto = new (window.AudioContext || window.webkitAudioContext)();
          for (let i = 0; i < repeticiones; i++) {{
            const oscilador = contexto.createOscillator();
            const ganancia = contexto.createGain();
            oscilador.type = 'square';
            oscilador.frequency.value = 880 + (i * 120);
            ganancia.gain.setValueAtTime(0.0001, contexto.currentTime + i * 0.45);
            ganancia.gain.exponentialRampToValueAtTime(0.35, contexto.currentTime + i * 0.45 + 0.02);
            ganancia.gain.exponentialRampToValueAtTime(0.0001, contexto.currentTime + i * 0.45 + 0.32);
            oscilador.connect(ganancia);
            ganancia.connect(contexto.destination);
            oscilador.start(contexto.currentTime + i * 0.45);
            oscilador.stop(contexto.currentTime + i * 0.45 + 0.34);
          }}
        }}
        beep();
      </script>
    </body>
    </html>
    """
    HTML_NOTIFICACION.write_text(textwrap.dedent(contenido).strip(), encoding="utf-8")
    return HTML_NOTIFICACION


def enviar_notificacion_escritorio(titulo: str, mensaje: str) -> None:
    sistema = platform.system().lower()
    try:
        if sistema == "darwin":
            subprocess.Popen([
                "osascript",
                "-e",
                f'display notification "{mensaje}" with title "{titulo}"',
            ])
        elif sistema == "linux":
            subprocess.Popen(["notify-send", titulo, mensaje])
        elif sistema == "windows":
            subprocess.Popen([
                "powershell",
                "-NoProfile",
                "-Command",
                "New-BurntToastNotification -Text @($args[0], $args[1])",
                titulo,
                mensaje,
            ])
    except OSError:
        return


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Notifica en tiempo real que una tarea termino.")
    parser.add_argument("--tarea", default=os.getenv("TAREA", "Tarea"), help="Nombre de la tarea.")
    parser.add_argument("--estado", default=os.getenv("ESTADO", "completada"), help="Estado a mostrar.")
    parser.add_argument(
        "--mensaje",
        default=os.getenv("MENSAJE", "La tarea fue completada correctamente."),
        help="Mensaje visual de la notificacion.",
    )
    parser.add_argument("--repeticiones", type=int, default=1, help="Cantidad de sonidos a emitir.")
    parser.add_argument("--sin-navegador", action="store_true", help="No abre una pestana visual.")
    parser.add_argument("--sin-sonido", action="store_true", help="No emite sonido audible.")
    parser.add_argument("--sin-escritorio", action="store_true", help="No intenta notificacion de escritorio.")
    parser.add_argument("--urgente", action="store_true", help="Muestra una ventana popup forzosa (siempre encima).")
    parser.add_argument("--auto-completado", action="store_true",
                        help="Modo tarea 100%% terminada: usa audio pre-establecido (termine la tarea.mp3), "
                             "3 repeticiones, mensaje de finalizacion, navegador y escritorio activados.")
    parser.add_argument("--sin-interfaz", action="store_true",
                        help="Modo automatico para entornos sin interfaz grafica (headless/CI). "
                             "Solo emite sonido de terminal y mensaje en consola, sin navegador ni popups.")
    parser.add_argument("--diagnostico", action="store_true",
                        help="Ejecuta diagnostico de audio: verifica archivos, reproductores y reproduccion de prueba.")
    return parser.parse_args()


def ejecutar_diagnostico() -> int:
    """Ejecuta diagnostico completo del sistema de audio."""
    print("\n=== DIAGNOSTICO DE AUDIO ===")
    print()
    
    # 1. Archivos de audio
    audios_dir = Path(__file__).parent.parent / "audios"
    print(f"Directorio de audios: {audios_dir}")
    print(f"Existe: {audios_dir.exists()}")
    if audios_dir.exists():
        print(f"Archivos:")
        for f in sorted(audios_dir.iterdir()):
            if f.suffix.lower() in (".mp3", ".wav", ".ogg", ".aiff"):
                print(f"  - {f.name} ({f.stat().st_size} bytes)")
    print()
    
    # 2. Reproductores disponibles
    print("Reproductores disponibles:")
    for cmd in ["ffplay", "paplay", "mpg123", "mpv", "aplay", "afplay", "vlc", "play", "sox"]:
        path = shutil.which(cmd)
        print(f"  {cmd}: {'OK' if path else 'NO ENCONTRADO'}")
    print()
    
    # 3. Prueba de cada audio
    for audio_file in sorted(audios_dir.iterdir()):
        if audio_file.suffix.lower() != ".mp3":
            continue
        print(f"Probando: {audio_file.name}...", end=" ", flush=True)
        try:
            reproducir_sonido_sistema(1, audio_file.name)
            print("OK")
        except Exception as e:
            print(f"ERROR: {e}")
    
    # 4. Prueba de pitido de terminal
    print()
    print("Probando pitido de terminal (x3)...", end=" ", flush=True)
    for _ in range(3):
        print("\a", end="", flush=True)
        time.sleep(0.25)
    print("OK")
    print()
    print("=== DIAGNOSTICO COMPLETADO ===")
    return 0


def main() -> int:
    args = parse_args()

    # --diagnostico: prueba de audio
    if args.diagnostico:
        return ejecutar_diagnostico()

    # --auto-completado: configuracion predefinida para tareas 100% terminadas
    if args.auto_completado:
        args.estado = "completada"
        if not args.mensaje or args.mensaje == "La tarea fue completada correctamente.":
            args.mensaje = "La ejecucion termino y el agente esta por responder."
        args.repeticiones = 3
        # --auto-completado siempre activa navegador y escritorio, salvo que se use --sin-interfaz

    # --sin-interfaz: modo headless, desactiva todo lo visual
    if args.sin_interfaz:
        args.sin_navegador = True
        args.sin_escritorio = True
        args.sin_sonido = True  # sin audio del sistema, solo terminal

    titulo = f"Tarea {args.estado}: {args.tarea}"

    if not args.sin_escritorio:
        enviar_notificacion_escritorio(titulo, args.mensaje)

    if not args.sin_navegador:
        archivo = crear_html_notificacion(args.tarea, args.estado, args.mensaje, args.repeticiones)
        try:
            webbrowser.open_new_tab(archivo.as_uri())
        except Exception:
            print(f"  [notificar_tarea] No se pudo abrir el navegador. HTML generado en: {archivo}", file=sys.stderr)

    if not args.sin_sonido:
        reproducir_sonido_sistema(args.repeticiones)

    if args.urgente:
        mostrar_popup_topmost(titulo, args.mensaje)

    # En modo --sin-interfaz, reproducir sonido de terminal como fallback
    if args.sin_interfaz:
        for _ in range(args.repeticiones):
            print("\a", end="", flush=True)
            time.sleep(0.25)

    print(f"  [notificar_tarea] Notificacion enviada: {titulo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
