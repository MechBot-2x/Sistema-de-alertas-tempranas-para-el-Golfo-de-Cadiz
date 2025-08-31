#!/usr/bin/env python3
"""
✅ VERIFICADOR DE ESTADO DEL SISTEMA - Mejorado
"""

import subprocess
import sys


def verificar_sistema():
    """Verificar que todo funciona"""
    print("=== 🔍 VERIFICACIÓN DEL SISTEMA ===")

    # Verificar Python
    print(f"🐍 Python: {sys.version.split()[0]} - ✅ OK")

    # Verificar imports básicos
    try:
        import requests

        print("📡 Requests: ✅ OK")
    except ImportError:
        print("📡 Requests: ❌ FALLO - Ejecuta: pip install requests")

    try:
        import telegram

        print("🤖 Telegram: ✅ OK")
    except ImportError:
        print("🤖 Telegram: ⚠️ No instalado - Ejecuta: pip install python-telegram-bot")

    try:
        from dotenv import load_dotenv

        print("🔧 Dotenv: ✅ OK")
    except ImportError:
        print("🔧 Dotenv: ⚠️ No instalado - Ejecuta: pip install python-dotenv")

    print("=== 🎯 VERIFICACIÓN COMPLETADA ===")


if __name__ == "__main__":
    verificar_sistema()
