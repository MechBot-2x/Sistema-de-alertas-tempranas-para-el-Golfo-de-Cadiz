#!/usr/bin/env python3
"""
📥 DESCARGADOR AUTOMÁTICO API KEY AEMET - Desde Google Drive
"""

import logging
import os
import re
import tempfile

import gdown
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


class DescargadorAEMET:
    """Descargador automático de API Key desde Google Drive"""

    def __init__(self):
        self.env_file = ".env"
        self.url_drive = (
            "https://drive.google.com/uc?id=1buceaEXByOO228JyVDkWwTrf7sqgaJoN"
        )
        load_dotenv()

    def descargar_archivo_drive(self):
        """Descargar archivo desde Google Drive"""
        try:
            # Crear directorio temporal
            temp_dir = tempfile.mkdtemp()
            archivo_temp = os.path.join(temp_dir, "aemet_api_key.txt")

            logging.info("📥 Descargando archivo desde Google Drive...")

            # Descargar usando gdown
            gdown.download(self.url_drive, archivo_temp, quiet=False)

            if os.path.exists(archivo_temp):
                logging.info("✅ Archivo descargado correctamente")
                return archivo_temp
            else:
                logging.error("❌ No se pudo descargar el archivo")
                return None

        except Exception as e:
            logging.error(f"❌ Error descargando archivo: {e}")
            return None

    def extraer_api_key_desde_archivo(self, ruta_archivo):
        """Extraer API Key desde el archivo descargado"""
        try:
            with open(ruta_archivo, "r", encoding="utf-8", errors="ignore") as f:
                contenido = f.read()

            logging.info(f"📊 Analizando archivo ({len(contenido)} caracteres)...")

            # Patrones para buscar API Keys (AEMET usa JWT)
            patrones = [
                r"eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+",  # JWT completo
                r'api_key["\']?\s*[:=]\s*["\']([^"\']+)["\']',  # JSON format
                r'clave["\']?\s*[:=]\s*["\']([^"\']+)["\']',  # Spanish
                r"[a-zA-Z0-9_-]{40,}",  # Long alphanumeric
                r"[a-f0-9]{64}",  # Hash-like
            ]

            api_key_encontrada = None

            for i, patron in enumerate(patrones):
                coincidencias = re.findall(patron, contenido)
                if coincidencias:
                    api_key = coincidencias[0]
                    if len(api_key) > 30:  # Asegurar que es suficientemente larga
                        api_key_encontrada = api_key
                        logging.info(f"✅ API Key encontrada (patrón {i+1})")
                        break

            if api_key_encontrada:
                # Limpiar la key si está en formato JSON
                if api_key_encontrada.startswith('"') and api_key_encontrada.endswith(
                    '"'
                ):
                    api_key_encontrada = api_key_encontrada[1:-1]

                logging.info(
                    f"🔑 API Key: {api_key_encontrada[:20]}...{api_key_encontrada[-10:]}"
                )
                return api_key_encontrada
            else:
                logging.warning("⚠️ No se encontró API Key en el archivo")
                # Mostrar preview del contenido para debug
                preview = contenido[:200] + "..." if len(contenido) > 200 else contenido
                logging.info(f"📄 Contenido del archivo: {preview}")
                return None

        except Exception as e:
            logging.error(f"❌ Error leyendo archivo: {e}")
            return None

    def configurar_api_key(self, api_key):
        """Configurar la API Key en el sistema"""
        try:
            # Leer .env existente o crear nuevo
            if os.path.exists(self.env_file):
                with open(self.env_file, "r") as f:
                    lineas = f.readlines()
            else:
                lineas = []

            # Buscar y reemplazar AEMET_API_KEY
            clave_actualizada = False
            nuevas_lineas = []

            for linea in lineas:
                if linea.startswith("AEMET_API_KEY="):
                    nuevas_lineas.append(f"AEMET_API_KEY={api_key}\n")
                    clave_actualizada = True
                else:
                    nuevas_lineas.append(linea)

            # Si no existía, añadirla
            if not clave_actualizada:
                nuevas_lineas.append(f"AEMET_API_KEY={api_key}\n")
                nuevas_lineas.append("\n")

            # Escribir archivo actualizado
            with open(self.env_file, "w") as f:
                f.writelines(nuevas_lineas)

            # Recargar variables de entorno
            load_dotenv(override=True)

            logging.info("✅ API Key configurada en .env")
            return True

        except Exception as e:
            logging.error(f"❌ Error configurando API Key: {e}")
            return False

    def verificar_conexion(self):
        """Verificar que la API Key funciona"""
        try:
            from scripts.datos.aemet_client import AEMETClientRobusto

            logging.info("🌐 Probando conexión con AEMET...")
            client = AEMETClientRobusto()

            if client.verificar_conexion():
                logging.info("✅ Conexión AEMET exitosa!")
                return True
            else:
                logging.warning("⚠️ No se pudo conectar con AEMET")
                return False

        except Exception as e:
            logging.error(f"❌ Error probando conexión: {e}")
            return False

    def ejecutar_descarga_configuracion(self):
        """Ejecutar todo el proceso automáticamente"""
        print("=" * 60)
        print("🎯 CONFIGURACIÓN AUTOMÁTICA API KEY AEMET")
        print("=" * 60)

        # Paso 1: Descargar archivo
        archivo_descargado = self.descargar_archivo_drive()
        if not archivo_descargado:
            return False

        # Paso 2: Extraer API Key
        api_key = self.extraer_api_key_desde_archivo(archivo_descargado)
        if not api_key:
            # Limpiar archivo temporal
            try:
                os.remove(archivo_descargado)
                os.rmdir(os.path.dirname(archivo_descargado))
            except:
                pass
            return False

        # Paso 3: Configurar en sistema
        if self.configurar_api_key(api_key):
            # Paso 4: Verificar conexión
            conexion_ok = self.verificar_conexion()

            # Limpiar archivo temporal
            try:
                os.remove(archivo_descargado)
                os.rmdir(os.path.dirname(archivo_descargado))
            except:
                pass

            if conexion_ok:
                print("=" * 60)
                print("🎉 CONFIGURACIÓN COMPLETADA EXITOSAMENTE!")
                print("🌤️ El sistema está listo para usar datos reales de AEMET")
                print("=" * 60)
                return True
            else:
                print("⚠️ API Key configurada pero verificación falló")
                print("💡 El sistema puede que necesite la key igualmente")
                return True

        return False


# Función principal
def configuracion_automatica():
    """Configuración automática completa"""
    descargador = DescargadorAEMET()

    if descargador.ejecutar_descarga_configuracion():
        # Preguntar si ejecutar el sistema
        respuesta = (
            input("\n¿Quieres ejecutar el sistema ahora? (s/n): ").lower().strip()
        )
        if respuesta in ["s", "si", "sí", "y", "yes"]:
            print("🚀 Iniciando sistema de monitorización...")
            from scripts.monitoreo.sistema_principal_mejorado import \
                SistemaResiliente

            sistema = SistemaResiliente()
            sistema.ejecutar_continuamente()
    else:
        print("❌ Configuración automática falló")
        print("💡 Puedes intentar:")
        print("1. Verificar el enlace de Google Drive")
        print(
            "2. Configurar manualmente con: python -m scripts.utilidades.configurador_aemet"
        )
        print("3. Usar el sistema en modo simulación")


if __name__ == "__main__":
    configuracion_automatica()
