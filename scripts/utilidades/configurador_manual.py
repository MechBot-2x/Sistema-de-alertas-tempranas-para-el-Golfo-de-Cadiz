#!/usr/bin/env python3
"""
📁 CONFIGURADOR MANUAL AEMET - Para archivos descargados manualmente
"""

import logging
import os
import re


logging.basicConfig(level=logging.INFO)


def configurar_desde_archivo_local(ruta_archivo):
    """Configurar API Key desde archivo local"""
    try:
        with open(ruta_archivo, "r", encoding="utf-8", errors="ignore") as f:
            contenido = f.read()

        print("🔍 Analizando archivo...")

        # Buscar API Key
        patrones = [
            r"eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+",
            r'api_key["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'clave["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r"[a-zA-Z0-9_-]{40,}",
        ]

        for patron in patrones:
            coincidencias = re.findall(patron, contenido)
            if coincidencias:
                api_key = coincidencias[0]
                print(f"✅ API Key encontrada: {api_key[:20]}...")

                # Guardar en .env
                with open(".env", "a") as f_env:
                    f_env.write(f"\nAEMET_API_KEY={api_key}\n")

                print("✅ API Key configurada en .env")
                return True

        print("❌ No se encontró API Key en el archivo")
        return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("🎯 CONFIGURACIÓN MANUAL AEMET")
    print("=" * 40)

    archivo = input("📁 Ruta del archivo descargado (ej: aemet_key.txt): ").strip()

    if os.path.exists(archivo):
        if configurar_desde_archivo_local(archivo):
            print("🎉 ¡Configuración completada!")
        else:
            print("💡 Puedes abrir el archivo y copiar la key manualmente")
    else:
        print("❌ Archivo no encontrado")
