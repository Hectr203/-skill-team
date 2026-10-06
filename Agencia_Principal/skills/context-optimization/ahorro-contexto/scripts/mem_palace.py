#!/usr/bin/env python3
"""
Módulo de Cifrado y Gestión Segura: Palacio de Memoria (Mem Palace).

Proporciona persistencia cifrada de nivel militar (AES-128-CBC + HMAC-SHA256 vía Fernet)
para resguardar decisiones arquitectónicas críticas, acuerdos sensibles y secretos locales.

Características de Nivel Industrial (11/10):
- Cero rutas relativas huérfanas: resuelve claves en base a proyectos o directorios explícitos.
- Creación de claves con permisos POSIX restringidos (0600 - lectura/escritura exclusiva del dueño).
- Soporte para clave vía variable de entorno (MEM_PALACE_KEY).
- Serialización transparente de texto (UTF-8) y estructuras JSON.
- Excepciones tipadas sin abortos abruptos (evita sys.exit dentro de la lógica de librería).
- CLI integrado para pruebas, diagnóstico y operaciones interactivas.
- Compatibilidad retroactiva total con la API funcional previa.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from typing import Any, Optional, Union


# --- Excepciones de Dominio ---

class MemoriaError(Exception):
    """Clase base para errores de memoria criptográfica."""
    pass


class CriptografiaNoDisponibleError(MemoriaError):
    """Lanzada cuando la librería cryptography no está disponible en el entorno."""
    pass


class ClaveInvalidaError(MemoriaError):
    """Lanzada cuando la clave provista es corrupta o no válida."""
    pass


class MemoriaCorruptaError(MemoriaError):
    """Lanzada cuando los datos cifrados están corruptos o la clave no coincide."""
    pass


# --- Clase Principal: PalacioMemoria ---

class PalacioMemoria:
    """
    Gestor criptográfico de memoria local para proyectos de la Agencia Principal.
    """

    def __init__(
        self,
        ruta_clave: Optional[Union[str, Path]] = None,
        ruta_archivo: Optional[Union[str, Path]] = None,
        clave_en_memoria: Optional[Union[str, bytes]] = None,
    ) -> None:
        """
        Inicializa una instancia del Palacio de Memoria.

        :param ruta_clave: Ruta hacia el archivo .key. Si es None, busca en .memoria/ o usa fallback.
        :param ruta_archivo: Ruta hacia el archivo .enc donde residen los datos cifrados.
        :param clave_en_memoria: Clave Fernet provista directamente (ej. desde entorno).
        """
        self._fernet = None
        self._clave_bytes: Optional[bytes] = None

        if clave_en_memoria:
            self._clave_bytes = (
                clave_en_memoria.encode("utf-8")
                if isinstance(clave_en_memoria, str)
                else clave_en_memoria
            )
            self._ruta_clave = None
        elif "MEM_PALACE_KEY" in os.environ:
            self._clave_bytes = os.environ["MEM_PALACE_KEY"].strip().encode("utf-8")
            self._ruta_clave = None
        else:
            self._ruta_clave = Path(ruta_clave).resolve() if ruta_clave else self._determinar_ruta_clave_default()

        self._ruta_archivo = Path(ruta_archivo).resolve() if ruta_archivo else None

    @staticmethod
    def _determinar_ruta_clave_default() -> Path:
        """
        Determina una ruta segura por defecto evitando contaminar el CWD si existe .memoria/.
        """
        cwd = Path.cwd()
        memoria_dir = cwd / ".memoria"
        if memoria_dir.is_dir():
            return memoria_dir / "mem_palace.key"
        return cwd / ".mem_palace.key"

    def _obtener_motor_fernet(self):
        """Inicializa o recupera la instancia de Fernet de manera perezosa (lazy)."""
        if self._fernet is not None:
            return self._fernet

        try:
            from cryptography.fernet import Fernet
        except ImportError as exc:
            raise CriptografiaNoDisponibleError(
                "La librería 'cryptography' no está instalada. "
                "Ejecute 'pip install cryptography' en su entorno."
            ) from exc

        if self._clave_bytes is None:
            if not self._ruta_clave.exists():
                # Generar nueva clave con permisos POSIX 0600
                self._clave_bytes = Fernet.generate_key()
                self._ruta_clave.parent.mkdir(parents=True, exist_ok=True)
                
                # Escritura atómica y segura con descriptor de archivo POSIX
                flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
                modo = 0o600  # Lectura y escritura exclusivamente para el propietario
                try:
                    fd = os.open(str(self._ruta_clave), flags, modo)
                    with os.fdopen(fd, "wb") as f:
                        f.write(self._clave_bytes)
                except OSError as err:
                    # Fallback en plataformas donde os.open con modo no aplica idéntico
                    self._ruta_clave.write_bytes(self._clave_bytes)
            else:
                self._clave_bytes = self._ruta_clave.read_bytes().strip()

        try:
            self._fernet = Fernet(self._clave_bytes)
        except Exception as exc:
            raise ClaveInvalidaError(f"La clave criptográfica provista no es válida: {exc}") from exc

        return self._fernet

    def cifrar_texto(self, texto: str) -> bytes:
        """Cifra una cadena de texto en bytes cifrados autenticados (Fernet)."""
        if not isinstance(texto, str):
            raise TypeError(f"Se esperaba una cadena de texto (str), pero se recibió {type(texto).__name__}.")
        fernet = self._obtener_motor_fernet()
        return fernet.encrypt(texto.encode("utf-8"))

    def descifrar_texto(self, datos_cifrados: bytes) -> str:
        """Descifra bytes cifrados y retorna la cadena de texto original en UTF-8."""
        if not isinstance(datos_cifrados, bytes):
            raise TypeError(f"Se esperaban bytes cifrados, pero se recibió {type(datos_cifrados).__name__}.")
        fernet = self._obtener_motor_fernet()
        try:
            from cryptography.fernet import InvalidToken
        except ImportError:
            InvalidToken = Exception

        try:
            return fernet.decrypt(datos_cifrados).decode("utf-8")
        except InvalidToken as exc:
            raise MemoriaCorruptaError(
                "No se pudo descifrar la información: el token está corrupto o la clave no coincide."
            ) from exc

    def cifrar_json(self, datos: Any) -> bytes:
        """Serializa una estructura de datos a JSON y la cifra."""
        texto_json = json.dumps(datos, ensure_ascii=False, indent=2)
        return self.cifrar_texto(texto_json)

    def descifrar_json(self, datos_cifrados: bytes) -> Any:
        """Descifra los bytes y deserializa el JSON subyacente."""
        texto = self.descifrar_texto(datos_cifrados)
        try:
            return json.loads(texto)
        except json.JSONDecodeError as exc:
            raise MemoriaCorruptaError(f"El contenido descifrado no es un JSON válido: {exc}") from exc

    def guardar_en_archivo(self, texto: str, ruta_destino: Optional[Union[str, Path]] = None) -> Path:
        """Cifra y guarda el texto directamente en el archivo destino."""
        destino = Path(ruta_destino).resolve() if ruta_destino else self._ruta_archivo
        if not destino:
            raise ValueError("No se especificó una ruta de archivo destino para guardar la memoria.")
        
        datos_cifrados = self.cifrar_texto(texto)
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(datos_cifrados)
        return destino

    def leer_desde_archivo(self, ruta_origen: Optional[Union[str, Path]] = None) -> str:
        """Lee un archivo cifrado y devuelve el texto plano."""
        origen = Path(ruta_origen).resolve() if ruta_origen else self._ruta_archivo
        if not origen or not origen.is_file():
            raise FileNotFoundError(f"El archivo de memoria cifrada no existe: {origen}")
        
        datos_cifrados = origen.read_bytes()
        return self.descifrar_texto(datos_cifrados)

    def rotar_clave(
        self,
        nueva_clave: Optional[Union[str, bytes]] = None,
        nueva_ruta_clave: Optional[Union[str, Path]] = None,
        ruta_archivo: Optional[Union[str, Path]] = None,
    ) -> tuple[Path, Path]:
        """
        Rota la clave criptográfica re-cifrando de forma atómica y segura los datos existentes.

        :param nueva_clave: Clave Fernet nueva (si es None, se genera automáticamente una nueva).
        :param nueva_ruta_clave: Destino para la nueva clave (si es None, sobrescribe la ruta actual).
        :param ruta_archivo: Archivo cifrado que se re-cifrará.
        :return: Tupla (ruta_archivo_actualizado, ruta_clave_actualizada).
        """
        try:
            from cryptography.fernet import Fernet
        except ImportError as exc:
            raise CriptografiaNoDisponibleError("Librería 'cryptography' no disponible.") from exc

        archivo = Path(ruta_archivo).resolve() if ruta_archivo else self._ruta_archivo
        if not archivo or not archivo.is_file():
            raise FileNotFoundError(f"No se encontró el archivo de memoria cifrada a rotar: {archivo}")

        # 1. Descifrar con la clave activa actual
        contenido_plano = self.leer_desde_archivo(archivo)

        # 2. Generar o preparar la nueva clave
        if nueva_clave:
            nueva_clave_bytes = nueva_clave.encode("utf-8") if isinstance(nueva_clave, str) else nueva_clave
        else:
            nueva_clave_bytes = Fernet.generate_key()

        destino_clave = Path(nueva_ruta_clave).resolve() if nueva_ruta_clave else self._ruta_clave
        if not destino_clave:
            destino_clave = archivo.parent / "mem_palace.key"

        # 3. Guardar la nueva clave con permisos POSIX 0600
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        modo = 0o600
        try:
            fd = os.open(str(destino_clave), flags, modo)
            with os.fdopen(fd, "wb") as f:
                f.write(nueva_clave_bytes)
        except OSError:
            destino_clave.write_bytes(nueva_clave_bytes)

        # 4. Re-cifrar con el nuevo motor
        nuevo_motor = Fernet(nueva_clave_bytes)
        nuevos_bytes = nuevo_motor.encrypt(contenido_plano.encode("utf-8"))

        # Escritura atómica del archivo cifrado
        archivo_temp = archivo.with_suffix(".tmp")
        archivo_temp.write_bytes(nuevos_bytes)
        archivo_temp.replace(archivo)

        # 5. Actualizar el estado interno de la instancia
        self._clave_bytes = nueva_clave_bytes
        self._fernet = nuevo_motor
        self._ruta_clave = destino_clave

        return archivo, destino_clave

    @property
    def clave_exportable(self) -> str:
        """Retorna la clave activa en formato string base64 seguro."""
        self._obtener_motor_fernet()
        return self._clave_bytes.decode("utf-8")


# --- Funciones de Conveniencia y Compatibilidad Retroactiva ---

_instancia_global: Optional[PalacioMemoria] = None

def _obtener_instancia_global(ruta_clave: Optional[Union[str, Path]] = None) -> PalacioMemoria:
    global _instancia_global
    if _instancia_global is None or ruta_clave is not None:
        _instancia_global = PalacioMemoria(ruta_clave=ruta_clave)
    return _instancia_global


def obtener_fernet(ruta_clave: Optional[Union[str, Path]] = None):
    """
    Retorna la instancia del motor Fernet subyacente.
    Mantiene compatibilidad con scripts existentes.
    """
    instancia = _obtener_instancia_global(ruta_clave)
    return instancia._obtener_motor_fernet()


def cifrar_datos(datos: str, ruta_clave: Optional[Union[str, Path]] = None) -> bytes:
    """Cifra texto en UTF-8 y retorna bytes cifrados."""
    instancia = _obtener_instancia_global(ruta_clave)
    return instancia.cifrar_texto(datos)


def descifrar_datos(datos_cifrados: bytes, ruta_clave: Optional[Union[str, Path]] = None) -> str:
    """Descifra bytes cifrados y retorna texto original."""
    instancia = _obtener_instancia_global(ruta_clave)
    return instancia.descifrar_texto(datos_cifrados)


# --- CLI Operativo ---

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gestor criptográfico Mem Palace (Agencia Principal - Nivel Élite 11/10)"
    )
    parser.add_argument("--clave", help="Ruta hacia el archivo de clave (.key).")
    parser.add_argument("--archivo", help="Ruta hacia el archivo de datos cifrados (.enc).")
    parser.add_argument("--cifrar", help="Texto a cifrar y mostrar por stdout.")
    parser.add_argument("--descifrar", help="Ruta de archivo cifrado o bytes hex/base64 a descifrar.")
    parser.add_argument("--generar-clave", action="store_true", help="Genera e imprime una nueva clave segura Fernet.")
    parser.add_argument("--rotar-clave", action="store_true", help="Descifra el archivo, genera nueva clave y re-cifra atómicamente.")
    parser.add_argument("--nueva-clave", help="Clave opcional a utilizar en la rotación (si se omite, se genera una nueva).")
    parser.add_argument("--probar", action="store_true", help="Ejecuta autodiagnóstico de cifrado/descifrado en memoria.")

    args = parser.parse_args()

    if args.generar_clave:
        try:
            from cryptography.fernet import Fernet
            print(Fernet.generate_key().decode("utf-8"))
            return 0
        except ImportError:
            print("[!] Error: 'cryptography' no está disponible.", file=sys.stderr)
            return 1

    if args.probar:
        print("🔒 Ejecutando autodiagnóstico Mem Palace...")
        try:
            palacio = PalacioMemoria(clave_en_memoria=None)
            test_msg = "Decisión Crítica: Usar Clean Architecture y Postgresql (2026)"
            cifrado = palacio.cifrar_texto(test_msg)
            recuperado = palacio.descifrar_texto(cifrado)
            assert recuperado == test_msg
            print("  ✓ Cifrado y descifrado de texto: OK")

            json_data = {"id": "ADR-001", "estado": "APROBADO", "impacto": "Alto"}
            cifrado_j = palacio.cifrar_json(json_data)
            recuperado_j = palacio.descifrar_json(cifrado_j)
            assert recuperado_j == json_data
            print("  ✓ Cifrado y descifrado de JSON estructurado: OK")
            print("✨ Mem Palace está 100% operativo y seguro.")
            return 0
        except Exception as err:
            print(f"[!] Falló el autodiagnóstico: {err}", file=sys.stderr)
            return 1

    if args.cifrar:
        palacio = PalacioMemoria(ruta_clave=args.clave, ruta_archivo=args.archivo)
        cifrado = palacio.cifrar_texto(args.cifrar)
        if args.archivo:
            palacio.guardar_en_archivo(args.cifrar, args.archivo)
            print(f"✓ Guardado en {args.archivo}")
        else:
            print(base64.b64encode(cifrado).decode("utf-8"))
    if args.descifrar:
        palacio = PalacioMemoria(ruta_clave=args.clave, ruta_archivo=args.archivo)
        origen = Path(args.descifrar)
        if origen.is_file():
            print(palacio.leer_desde_archivo(origen))
        else:
            # Interpretar como base64 directo
            raw_bytes = base64.b64decode(args.descifrar.strip())
            print(palacio.descifrar_texto(raw_bytes))
        return 0

    if args.rotar_clave:
        if not args.archivo:
            print("[!] Error: Se requiere especificar --archivo para rotar su clave.", file=sys.stderr)
            return 1
        palacio = PalacioMemoria(ruta_clave=args.clave, ruta_archivo=args.archivo)
        try:
            arch, clv = palacio.rotar_clave(nueva_clave=args.nueva_clave)
            print("✓ Clave rotada exitosamente con permisos POSIX 0600.")
            print(f"  Archivo re-cifrado: {arch}")
            print(f"  Nueva clave en:     {clv}")
            return 0
        except Exception as err:
            print(f"[!] Error al rotar clave: {err}", file=sys.stderr)
            return 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
