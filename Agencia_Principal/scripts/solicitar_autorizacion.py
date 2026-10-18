#!/usr/bin/env python3
"""Notifica que el agente requiere autorizacion por parte del usuario.

Uso normal:
    python3 scripts/solicitar_autorizacion.py --recurso "leer archivo .env"

Uso normal forzado:
    python3 scripts/solicitar_autorizacion.py --recurso "leer archivo"
"""

from __future__ import annotations

import argparse
import html
import json
import sys
import textwrap
import tempfile
import webbrowser
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Importar funciones de notificar_tarea.py
from notificar_tarea import reproducir_sonido_sistema, enviar_notificacion_escritorio

HTML_NOTIFICACION = Path("agencia-solicitud-autorizacion.html")

AUDIO_AUTORIZACION = "Aprobación urgente..mp3"
ARCHIVO_AUDITORIA = Path(__file__).resolve().parents[1] / ".hitl_audit.jsonl"


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
    destino = HTML_NOTIFICACION
    if not destino.is_absolute():
        destino = Path(tempfile.mkdtemp(prefix="agencia-avisos-")) / destino.name
    with destino.open("w", encoding="utf-8") as archivo:
        archivo.write(textwrap.dedent(contenido).strip())
    return destino


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Notifica y solicita autorización de permisos.")
    parser.add_argument("--recurso", required=True, help="El recurso, archivo o comando para el cual se requiere autorizacion.")
    parser.add_argument("--sin-navegador", action="store_true", help="No abre una pestana visual.")
    parser.add_argument("--sin-sonido", action="store_true", help="No emite sonido audible.")
    parser.add_argument("--sin-escritorio", action="store_true", help="No intenta notificacion de escritorio.")
    parser.add_argument("--sin-interfaz", action="store_true",
                        help="Omite avisos visuales y sonoros; no concede autorización.")
    parser.add_argument("--esperar", action="store_true", help="Espera confirmación interactiva en terminal [s/N].")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    titulo = "Autorizacion Requerida"
    solicitud_id = str(uuid.uuid4())

    if args.sin_interfaz:
        args.sin_navegador = args.sin_sonido = args.sin_escritorio = True

    if not args.sin_escritorio:
        enviar_notificacion_escritorio(titulo, f"Permiso necesario para: {args.recurso}")

    if not args.sin_navegador:
        archivo = crear_html_autorizacion(args.recurso)
        try:
            webbrowser.open_new_tab(archivo.as_uri())
        except Exception:
            print(f"  [solicitar_autorizacion] No se pudo abrir el navegador. HTML generado en: {archivo}", file=sys.stderr)

    if not args.sin_sonido:
        reproducir_sonido_sistema(2, audio_filename=AUDIO_AUTORIZACION)

    print(f"  [solicitar_autorizacion] Notificación emitida para recurso: {args.recurso}")

    # Registro de auditoría HITL
    audit_file = ARCHIVO_AUDITORIA
    try:
        entry = {
            "id": solicitud_id,
            "fecha": datetime.now(timezone.utc).isoformat(),
            "tipo": "autorizacion",
            "recurso": args.recurso,
            "esperar": args.esperar,
            "resultado": "pendiente",
        }
        with audit_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        print("No se pudo registrar la solicitud de autorización.", file=sys.stderr)
        return 1

    # Modo interactivo si se pasa --esperar o si es TTY interactivo
    resultado = "pendiente"
    if args.esperar or sys.stdin.isatty():
        try:
            resp = input(f"\n[HITL] ¿Autorizas la ejecución sobre '{args.recurso}'? [s/N]: ").strip().lower()
            if resp in ("s", "si", "sí", "y", "yes"):
                resultado = "aprobada"
                print("  [solicitar_autorizacion] [✓] Autorización concedida por el operador.")
            else:
                resultado = "rechazada"
                print("  [solicitar_autorizacion] [✗] Acción rechazada por el operador.")
        except (KeyboardInterrupt, EOFError):
            resultado = "cancelada"
            print("\n  [solicitar_autorizacion] [✗] Solicitud cancelada.")
    if resultado != "pendiente":
        try:
            with audit_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"id": solicitud_id, "tipo": "autorizacion_resultado",
                                    "fecha": datetime.now(timezone.utc).isoformat(),
                                    "resultado": resultado}, ensure_ascii=False) + "\n")
        except OSError:
            print("No se pudo registrar el resultado de autorización.", file=sys.stderr)
            return 1

    # Una notificación no constituye aprobación; el llamador debe comprobar el código.
    return 0 if resultado == "aprobada" else 2 if resultado == "pendiente" else 1


if __name__ == "__main__":
    sys.exit(main())
