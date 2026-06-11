import os
import sys

def ejecutar_cierre():
    print("=== SMT AGENCIA - REGISTRO DE CONTEXTO (CIERRE) ===")
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        from mem_palace import cifrar_datos
    except ImportError:
        print("[!] No se pudo importar mem_palace. Asegúrese de que existe en la carpeta.")
        sys.exit(1)
    
    print("\nIntroduzca los detalles de la sesión actual para cifrar en Mem Palace:")
    try:
        tareas_completadas = input("> Tareas completadas en esta sesión: ")
        pendientes = input("> Tareas pendientes para el siguiente sprint/sesión: ")
        decisiones = input("> Decisiones técnicas o de arquitectura tomadas: ")
        riesgos = input("> Riesgos o dependencias a considerar: ")
    except KeyboardInterrupt:
        print("\n[!] Operación cancelada por el usuario.")
        sys.exit(0)
    
    informe = f"""[MEMORIA DE SESIÓN SMT]
- Tareas Completadas: {tareas_completadas}
- Pendientes: {pendientes}
- Decisiones de Arquitectura: {decisiones}
- Riesgos: {riesgos}
"""
    
    try:
        cifrado = cifrar_datos(informe)
        with open(".memoria_palacio_cifrada", "wb") as f:
            f.write(cifrado)
        print("[+] Mem Palace local cifrado y guardado exitosamente en '.memoria_palacio_cifrada'.")
    except Exception as e:
        print(f"[!] Error al cifrar y guardar: {e}")

if __name__ == "__main__":
    ejecutar_cierre()
