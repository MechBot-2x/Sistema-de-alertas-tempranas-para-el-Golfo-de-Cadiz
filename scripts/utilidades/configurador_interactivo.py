#!/usr/bin/env python3
"""
🎯 CONFIGURADOR INTERACTIVO AEMET - Sin dependencias externas
"""

import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def configuracion_interactiva():
    """Configuración interactiva sin dependencias externas"""
    print("=" * 50)
    print("🎯 CONFIGURACIÓN INTERACTIVA AEMET API KEY")
    print("=" * 50)

    load_dotenv()

    # Verificar estado actual
    api_key_actual = os.getenv('AEMET_API_KEY', 'No configurada')
    if api_key_actual not in ['opcional', 'No configurada', 'TU_API_KEY_REAL']:
        print(f"✅ API Key ya configurada: {api_key_actual[:20]}...")
        return True

    print("🔍 No se detectó API Key de AEMET configurada")
    print("\n💡 **INSTRUCCIONES RÁPIDAS:**")
    print("1. Abre el correo de AEMET o el archivo de Google Drive")
    print("2. Busca un texto que empiece con 'eyJ' (ej: eyJhbGciOiJIUzI1NiJ9...)")
    print("3. Copia TODO ese texto")
    print("4. Pégala cuando te lo pida el sistema")
    print("\n🔄 El sistema funciona perfectamente en modo simulación meanwhile")
    print("=" * 50)

    opcion = input("\n¿Tienes la API Key a mano? (s/n): ").lower().strip()

    if opcion in ['s', 'si', 'sí', 'y', 'yes']:
        api_key = input("🔑 Pega tu API Key de AEMET: ").strip()

        if api_key:
            # Limpiar la key por si acaso
            api_key = api_key.replace('"', '').replace("'", "").strip()

            if api_key.startswith('eyJ') and len(api_key) > 50:
                # Guardar en .env
                with open('.env', 'a') as f:
                    f.write(f'\nAEMET_API_KEY={api_key}\n')

                print("✅ API Key configurada correctamente!")
                print("🔄 Recargando configuración...")

                # Recargar variables
                load_dotenv(override=True)

                # Probar conexión
                print("🌐 Probando conexión con AEMET...")
                try:
                    from scripts.datos.aemet_client import AEMETClientRobusto
                    client = AEMETClientRobusto()
                    if client.verificar_conexion():
                        print("🎉 ¡Conexión exitosa! El sistema usará datos reales")
                    else:
                        print("⚠️ API Key configurada pero conexión falló")
                        print("💡 El sistema puede necesitar la key igualmente")
                except Exception as e:
                    print(f"⚠️ Error probando conexión: {e}")

                return True
            else:
                print("❌ El formato no parece una API Key válida de AEMET")
                print("💡 Las API Keys de AEMET suelen empezar con 'eyJ' y ser muy largas")
                return False
        else:
            print("❌ No se introdujo ninguna API Key")
            return False
    else:
        print("✅ Continuando en modo simulación")
        print("🌟 El sistema funcionará con datos simulados inteligentes")
        return True

if __name__ == "__main__":
    configuracion_interactiva()

    # Preguntar si ejecutar el sistema
    respuesta = input("\n¿Quieres ejecutar el sistema ahora? (s/n): ").lower().strip()
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        print("🚀 Iniciando sistema de monitorización...")
        try:
            from scripts.monitoreo.sistema_principal_mejorado import SistemaResiliente
            sistema = SistemaResiliente()
            sistema.ejecutar_continuamente()
        except Exception as e:
            print(f"❌ Error iniciando sistema: {e}")
            print("💡 Intentando instalar dependencias faltantes...")
            os.system("pip install requests python-dotenv")
            print("🔄 Por favor, ejecuta nuevamente: python -m scripts.monitoreo.sistema_principal_mejorado")
