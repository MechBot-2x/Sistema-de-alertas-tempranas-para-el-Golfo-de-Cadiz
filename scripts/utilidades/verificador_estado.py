#!/usr/bin/env python3
"""
✅ VERIFICADOR DE ESTADO DEL SISTEMA
"""

import logging
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
    except:
        print("📡 Requests: ❌ FALLO")
    
    try:
        import telegram
        print("🤖 Telegram: ✅ OK")
    except:
        print("🤖 Telegram: ⚠️ No instalado")
    
    print("=== 🎯 VERIFICACIÓN COMPLETADA ===")

if __name__ == "__main__":
    verificar_sistema()
