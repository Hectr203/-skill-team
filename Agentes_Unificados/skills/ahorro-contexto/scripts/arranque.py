import os
import sys

def ejecutar_arranque():
    print("=== SMT AGENCIA - MEMORIA PERSISTENTE (ARRANQUE) ===")
    # Validar instalación de cryptography
    try:
        import cryptography
        print("[+] Cryptography: OK")
    except ImportError:
        print("[!] Cryptography no instalado. Intentando instalar...")
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
            print("[+] Cryptography instalado exitosamente.")
        except Exception as e:
            print(f"[!] Error al instalar: {e}. Por favor, instale manualmente: pip install cryptography")
            sys.exit(1)
    
    ruta_memoria = ".memoria_palacio_cifrada"
    if os.path.exists(ruta_memoria):
        print("[+] Mem Palace detectado. Recuperando contexto cifrado...")
        try:
            from mem_palace import descifrar_datos
            with open(ruta_memoria, "rb") as f:
                contenido_cifrado = f.read()
            contexto = descifrar_datos(contenido_cifrado)
            print("\n--- CONTEXTO RECUPERADO DE LA SESIÓN ANTERIOR ---")
            print(contexto)
            print("-------------------------------------------------\n")
        except Exception as e:
            print(f"[!] Error al descifrar el contexto de Mem Palace: {e}")
    else:
        print("[i] No se encontró historial cifrado de Mem Palace. Iniciando nueva sesión limpia.")

if __name__ == "__main__":
    # Asegurar que el script puede importar mem_palace local
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    ejecutar_arranque()
