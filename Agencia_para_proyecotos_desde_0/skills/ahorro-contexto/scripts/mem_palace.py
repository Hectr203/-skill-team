import os
import sys

def obtener_fernet():
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        print("[!] Error: La librería 'cryptography' no está instalada. Ejecute 'pip install cryptography'.")
        sys.exit(1)
    
    ruta_clave = ".mem_palace_key"
    if not os.path.exists(ruta_clave):
        clave = Fernet.generate_key()
        with open(ruta_clave, "wb") as f:
            f.write(clave)
    else:
        with open(ruta_clave, "rb") as f:
            clave = f.read()
    return Fernet(clave)

def cifrar_datos(datos: str) -> bytes:
    fernet = obtener_fernet()
    return fernet.encrypt(datos.encode("utf-8"))

def descifrar_datos(datos_cifrados: bytes) -> str:
    fernet = obtener_fernet()
    return fernet.decrypt(datos_cifrados).decode("utf-8")
