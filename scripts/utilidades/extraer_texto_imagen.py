#!/usr/bin/env python3
"""
🔍 EXTRACTOR DE TEXTO DE IMAGEN - Para API Keys en imágenes
"""

import os
import sys

import pytesseract
from PIL import Image


def extraer_texto_desde_imagen(ruta_imagen):
    """Extraer texto de una imagen usando OCR"""
    try:
        # Convertir GIF a imagen manejable
        with Image.open(ruta_imagen) as img:
            # Convertir a RGB si es necesario
            if img.mode != "RGB":
                img = img.convert("RGB")

            # Extraer texto usando OCR
            texto = pytesseract.image_to_string(img)
            return texto.strip()

    except Exception as e:
        print(f"❌ Error procesando imagen: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python extraer_texto_imagen.py <ruta_imagen>")
        sys.exit(1)

    ruta_imagen = sys.argv[1]
    if not os.path.exists(ruta_imagen):
        print(f"❌ Archivo no encontrado: {ruta_imagen}")
        sys.exit(1)

    print(f"🔍 Analizando imagen: {ruta_imagen}")
    texto = extraer_texto_desde_imagen(ruta_imagen)

    if texto:
        print("✅ Texto extraído:")
        print("=" * 50)
        print(texto)
        print("=" * 50)

        # Buscar posible API Key
        import re

        api_keys = re.findall(r"eyJ[a-zA-Z0-9_\-\.]+", texto)
        if api_keys:
            print(f"🎯 Posible API Key encontrada: {api_keys[0]}")
        else:
            print("❌ No se encontraron API Keys en el texto")
    else:
        print("❌ No se pudo extraer texto de la imagen")
