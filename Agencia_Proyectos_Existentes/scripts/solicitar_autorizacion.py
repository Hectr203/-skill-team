#!/usr/bin/env python3
"""Notifica que el agente requiere autorizacion por parte del usuario.

Uso normal:
    python3 scripts/solicitar_autorizacion.py --recurso "leer archivo .env"

Uso sin interfaz grafica (entorno automatico/headless):
    python3 scripts/solicitar_autorizacion.py --recurso "leer archivo" --sin-interfaz
"""

from __future__ import annotations

import argparse
import html
import sys
import textwrap
import time
import webbrowser
from pathlib import Path

# Importar funciones de notificar_tarea.py
from notificar_tarea import reproducir_sonido_sistema, enviar_notificacion_escritorio, mostrar_popup_topmost, reproducir_sonido_terminal

HTML_NOTIFICACION = Path(__file__).with_name("solicitud_autorizacion.html")

AUDIO_AUTORIZACION = "Aprobación urgente..mp3"


def crear_html_autorizacion(recurso: str) -> Path:
    titulo = "Autorizacion Requerida"
    
    # Convertir a HTML
    recurso_html = html.escape(recurso).replace("\n", "<br>")

    contenido = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>{titulo}</title>
      <style>
        body {{
          margin: 0;
          min-height: 100vh;
          display: grid;
          place-items: center;
          font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          background: linear-gradient(135deg, #1e3a8a, #9a3412, #ea580c);
          color: white;
        }}
        main {{
          width: min(880px, calc(100vw - 32px));
          padding: 42px;
          border-radius: 28px;
          background: rgba(15, 23, 42, 0.85);
          box-shadow: 0 24px 80px rgba(0, 0, 0, 0.4);
          text-align: center;
        }}
        .alerta {{
          display: inline-block;
          margin-bottom: 18px;
          padding: 10px 16px;
          border-radius: 999px;
          background: #f97316;
          color: white;
          font-weight: 800;
          letter-spacing: 0.08em;
          text-transform: uppercase;
        }}
        h1 {{ font-size: clamp(32px, 6vw, 72px); margin: 0 0 18px; }}
        .recurso {{ 
            font-size: clamp(18px, 3vw, 24px); 
            line-height: 1.5; 
            margin: 20px 0; 
            text-align: center;
            background: rgba(0,0,0,0.3);
            padding: 24px;
            border-radius: 16px;
            border-left: 4px solid #f97316;
            word-wrap: break-word;
        }}
        .instruccion {{
            font-size: 18px;
            color: #fdba74;
            margin-top: 20px;
            font-weight: bold;
        }}
        .hora {{ margin-top: 26px; color: #cbd5e1; font-size: 16px; }}
      </style>
    </head>
    <body>
      <main>
        <div class="alerta">Permiso Requerido</div>
        <h1>Necesito Autorizacion</h1>
        
        <p class="instruccion">Para continuar, el agente necesita acceso al siguiente recurso o accion:</p>
        
        <div class="recurso">
            {recurso_html}
        </div>

        <p class="instruccion">Revisa tu editor de codigo o chat para Aceptar (Allow) o Rechazar (Reject).</p>
        <div class="hora" id="hora"></div>
      </main>
      <script>
        document.getElementById('hora').textContent = new Date().toLocaleString('es-MX');
        function beep() {{
          const contexto = new (window.AudioContext || window.webkitAudioContext)();
          for (let i = 0; i < 2; i++) {{
            const oscilador = contexto.createOscillator();
            const ganancia = contexto.createGain();
            oscilador.type = 'square';
            oscilador.frequency.value = 600 + (i * 100);
            ganancia.gain.setValueAtTime(0.0001, contexto.currentTime + i * 0.45);
            ganancia.gain.exponentialRampToValueAtTime(0.35, contexto.currentTime + i * 0.45 + 0.02);
            ganancia.gain.exponentialRampToValueAtTime(0.0001, contexto.currentTime + i * 0.45 + 0.32);
            oscilador.connect(ganancia);
            oscilador.connect(contexto.destination);
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Notifica que el agente necesita autorizacion de permisos.")
    parser.add_argument("--recurso", required=True, help="El recurso, archivo o comando para el cual se requiere autorizacion.")
    parser.add_argument("--sin-navegador", action="store_true", help="No abre una pestana visual.")
    parser.add_argument("--sin-sonido", action="store_true", help="No emite sonido audible.")
    parser.add_argument("--sin-escritorio", action="store_true", help="No intenta notificacion de escritorio.")
    parser.add_argument("--sin-interfaz", action="store_true",
                        help="Modo automatico para entornos sin interfaz grafica (headless/CI). "
                             "Solo emite sonido de terminal y mensaje en consola, sin navegador ni popups.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    titulo = "Autorizacion Requerida"

    # --sin-interfaz: desactiva todo lo visual
    if args.sin_interfaz:
        args.sin_navegador = True
        args.sin_escritorio = True
        args.sin_sonido = True

    if not args.sin_escritorio:
        enviar_notificacion_escritorio(titulo, f"Permiso necesario para: {args.recurso}")

    if not args.sin_navegador:
        archivo = crear_html_autorizacion(args.recurso)
        try:
            webbrowser.open_new_tab(archivo.as_uri())
        except Exception:
            print(f"  [solicitar_autorizacion] No se pudo abrir el navegador. HTML generado en: {archivo}", file=sys.stderr)

    if not args.sin_sonido:
        reproducir_sonido_sistema(1, audio_filename=AUDIO_AUTORIZACION)

    if not args.sin_interfaz:
        mostrar_popup_topmost(titulo, f"El agente requiere autorizacion para:\n\n{args.recurso}\n\nRevisa tu editor (Ej: VS Code) para Aceptar o Rechazar.")

    # En modo --sin-interfaz, solo pitido de terminal
    if args.sin_interfaz:
        for _ in range(3):
            print("\a", end="", flush=True)
            time.sleep(0.25)

    print(f"  [solicitar_autorizacion] Notificacion enviada.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
