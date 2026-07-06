#!/usr/bin/env python3
"""Notifica la finalizacion de tareas sin dependencias externas.

Uso basico:
    python3 scripts/notificar_tarea.py --tarea "Analisis Oaxaca" --estado completada

Integracion con automatizadores:
    comando_largo && python3 scripts/notificar_tarea.py --tarea "Build API"
"""

from __future__ import annotations

import argparse
import html
import os
import platform
import subprocess
import sys
import textwrap
import time
import webbrowser
from pathlib import Path


HTML_NOTIFICACION = Path(__file__).with_name("notificacion_tarea.html")


def reproducir_sonido_terminal(repeticiones: int) -> None:
    """Emite campanas de terminal como respaldo multiplataforma."""
    for _ in range(max(1, repeticiones)):
        print("\a", end="", flush=True)
        time.sleep(0.25)


def reproducir_sonido_sistema(repeticiones: int) -> None:
    sistema = platform.system().lower()
    comandos: list[list[str]] = []

    script_dir = Path(__file__).parent
    audio_path = script_dir.parent / "audios" / "noti.mp3"
    str_audio = str(audio_path)

    if audio_path.exists():
        if sistema == "darwin":
            comandos = [["afplay", str_audio]]
        elif sistema == "linux":
            comandos = [
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", str_audio],
                ["paplay", str_audio],
                ["mpg123", "-q", str_audio],
                ["mpv", "--no-video", "--really-quiet", str_audio]
            ]
        elif sistema == "windows":
            comandos = [
                ["vlc", "-I", "dummy", "--play-and-exit", str_audio],
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", str_audio]
            ]

    # Fallbacks si no existe el audio o fallan los reproductores de mp3
    if not comandos:
        if sistema == "darwin":
            comandos = [["afplay", "/System/Library/Sounds/Glass.aiff"]]
        elif sistema == "linux":
            comandos = [
                ["paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"],
                ["aplay", "/usr/share/sounds/alsa/Front_Center.wav"],
            ]
        elif sistema == "windows":
            comandos = [["powershell", "-NoProfile", "-Command", "[console]::beep(1200,500)"]]

    for _ in range(max(1, repeticiones)):
        ejecutado = False
        for comando in comandos:
            try:
                subprocess.run(
                    comando,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                ejecutado = True
                break
            except OSError:
                continue
        if not ejecutado:
            reproducir_sonido_terminal(1)
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    titulo = f"Tarea {args.estado}: {args.tarea}"

    if not args.sin_escritorio:
        enviar_notificacion_escritorio(titulo, args.mensaje)

    if not args.sin_navegador:
        archivo = crear_html_notificacion(args.tarea, args.estado, args.mensaje, args.repeticiones)
        webbrowser.open_new_tab(archivo.as_uri())

    if not args.sin_sonido:
        reproducir_sonido_sistema(args.repeticiones)

    print(f"Notificacion enviada: {titulo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
