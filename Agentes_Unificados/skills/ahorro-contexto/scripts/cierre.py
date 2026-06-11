import os
import sys
import argparse


def _leer_contexto_previo():
    ruta_memoria = ".memoria_palacio_cifrada"
    if not os.path.exists(ruta_memoria):
        return ""
    try:
        from mem_palace import descifrar_datos
        with open(ruta_memoria, "rb") as f:
            return descifrar_datos(f.read())
    except Exception:
        return ""


def _construir_informe(tareas_completadas, pendientes, decisiones, riesgos):
    return f"""[MEMORIA DE SESION SMT]
- Tareas Completadas: {tareas_completadas}
- Pendientes: {pendientes}
- Decisiones de Arquitectura: {decisiones}
- Riesgos: {riesgos}
"""

def ejecutar_cierre(args=None):
    print("=== SMT AGENCIA - REGISTRO DE CONTEXTO (CIERRE) ===")
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    if args and args.proyecto:
        from memoria_proyecto import agregar_cloudmem, guardar_mem_palace, informe, lista_archivos, resolver_proyecto

        proyecto = resolver_proyecto(args.proyecto)
        tareas = args.tareas or ""
        pendientes = args.pendientes or ""
        decisiones = args.decisiones or ""
        riesgos = args.riesgos or ""
        guardar_mem_palace(proyecto, informe(tareas, pendientes, decisiones, riesgos))
        if args.cloud_resumen:
            agregar_cloudmem(
                proyecto,
                args.cloud_resumen,
                lista_archivos(args.archivos),
                args.tipo,
                decisiones,
                pendientes,
                riesgos,
            )
        print(f"[+] Memoria independiente del proyecto actualizada: {proyecto / '.memoria'}")
        return

    try:
        from mem_palace import cifrar_datos
    except ImportError:
        print("[!] No se pudo importar mem_palace. Asegúrese de que existe en la carpeta.")
        sys.exit(1)
    
    if args and any([args.tareas, args.pendientes, args.decisiones, args.riesgos]):
        tareas_completadas = args.tareas
        pendientes = args.pendientes
        decisiones = args.decisiones
        riesgos = args.riesgos
    else:
        print("\nIntroduzca los detalles de la sesión actual para cifrar en Mem Palace:")
        try:
            tareas_completadas = input("> Tareas completadas en esta sesión: ")
            pendientes = input("> Tareas pendientes para el siguiente sprint/sesión: ")
            decisiones = input("> Decisiones técnicas o de arquitectura tomadas: ")
            riesgos = input("> Riesgos o dependencias a considerar: ")
        except KeyboardInterrupt:
            print("\n[!] Operación cancelada por el usuario.")
            sys.exit(0)

    contexto_previo = _leer_contexto_previo()
    informe_actual = _construir_informe(tareas_completadas, pendientes, decisiones, riesgos)
    informe = f"{contexto_previo.rstrip()}\n\n{informe_actual}" if contexto_previo else informe_actual
    
    try:
        cifrado = cifrar_datos(informe)
        with open(".memoria_palacio_cifrada", "wb") as f:
            f.write(cifrado)
        print("[+] Mem Palace local cifrado y guardado exitosamente en '.memoria_palacio_cifrada'.")
    except Exception as e:
        print(f"[!] Error al cifrar y guardar: {e}")

    if args and args.cloud_resumen:
        try:
            from cloudmem import agregar_entrada
            archivos = [item.strip() for item in args.archivos.split(",") if item.strip()]
            agregar_entrada(
                resumen=args.cloud_resumen,
                archivos=archivos,
                tipo=args.tipo,
                decisiones=decisiones,
                pendientes=pendientes,
                riesgos=riesgos,
            )
            print("[+] CloudMem local actualizado con el historial operativo.")
        except Exception as e:
            print(f"[!] Error al actualizar CloudMem local: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cierre de memoria persistente SMT.")
    parser.add_argument("--tareas", default="")
    parser.add_argument("--pendientes", default="")
    parser.add_argument("--decisiones", default="")
    parser.add_argument("--riesgos", default="")
    parser.add_argument("--cloud-resumen", default="")
    parser.add_argument("--archivos", default="")
    parser.add_argument("--tipo", default="operativo")
    parser.add_argument("--proyecto", default="", help="Ruta del proyecto para usar memoria independiente.")
    ejecutar_cierre(parser.parse_args())
