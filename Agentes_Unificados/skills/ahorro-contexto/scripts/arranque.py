import os
import sys
import argparse

def ejecutar_arranque(proyecto=None):
    print("=== SMT AGENCIA - MEMORIA PERSISTENTE (ARRANQUE) ===")
    if proyecto:
        from memoria_proyecto import imprimir_cloudmem, leer_cloudmem, leer_mem_palace, resolver_proyecto

        ruta_proyecto = resolver_proyecto(proyecto)
        print(f"[+] Usando memoria independiente del proyecto: {ruta_proyecto}")
        contexto = leer_mem_palace(ruta_proyecto)
        if contexto:
            print("\n--- MEM PALACE DEL PROYECTO ---")
            print(contexto)
            print("--------------------------------\n")
        else:
            print("[i] Mem Palace del proyecto no tiene entradas.")
        imprimir_cloudmem(leer_cloudmem(ruta_proyecto, limite=8))
        return

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

    try:
        from cloudmem import imprimir_entradas, leer_entradas
        print("\n[+] Consultando CloudMem local para historial operativo reciente...")
        imprimir_entradas(leer_entradas(limite=8))
    except Exception as e:
        print(f"[!] No se pudo consultar CloudMem local: {e}")

if __name__ == "__main__":
    # Asegurar que el script puede importar mem_palace local
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    parser = argparse.ArgumentParser(description="Arranque de memoria persistente.")
    parser.add_argument("--proyecto", default="", help="Ruta del proyecto para usar memoria independiente.")
    args = parser.parse_args()
    ejecutar_arranque(args.proyecto or None)
