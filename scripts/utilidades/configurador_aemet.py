#!/usr/bin/env python3
"""
🔧 CONFIGURADOR AEMET AUTOMÁTICO - Sistema inteligente de configuración
"""

import os
import re
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

class ConfiguradorAEMET:
    """Configurador automático para AEMET OpenData"""
    
    def __init__(self):
        self.env_file = '.env'
        load_dotenv()
        
    def verificar_api_key(self):
        """Verificar si la API Key está configurada y es válida"""
        api_key = os.getenv('AEMET_API_KEY')
        
        if not api_key or api_key == 'opcional' or api_key == 'TU_API_KEY_REAL':
            return False, "❌ API Key no configurada"
        
        # Verificar formato básico de API Key (normalmente JWT)
        if api_key.startswith('eyJ') and len(api_key) > 50:
            return True, "✅ API Key configurada correctamente"
        else:
            return False, "⚠️ API Key con formato sospechoso"
    
    def configurar_api_key(self, api_key):
        """Configurar la API Key en el archivo .env"""
        try:
            # Leer el archivo .env actual
            if os.path.exists(self.env_file):
                with open(self.env_file, 'r') as f:
                    lineas = f.readlines()
            else:
                lineas = []
            
            # Buscar y reemplazar la línea de AEMET_API_KEY
            clave_encontrada = False
            nuevas_lineas = []
            
            for linea in lineas:
                if linea.startswith('AEMET_API_KEY='):
                    nuevas_lineas.append(f'AEMET_API_KEY={api_key}\n')
                    clave_encontrada = True
                else:
                    nuevas_lineas.append(linea)
            
            # Si no existía, añadirla
            if not clave_encontrada:
                nuevas_lineas.append(f'AEMET_API_KEY={api_key}\n')
            
            # Escribir el archivo actualizado
            with open(self.env_file, 'w') as f:
                f.writelines(nuevas_lineas)
            
            # Recargar variables de entorno
            load_dotenv(override=True)
            
            return True, "✅ API Key configurada correctamente"
            
        except Exception as e:
            return False, f"❌ Error configurando API Key: {e}"
    
    def probar_conexion_aemet(self):
        """Probar la conexión con AEMET usando la API Key configurada"""
        from scripts.datos.aemet_client import AEMETClientRobusto
        
        client = AEMETClientRobusto()
        return client.verificar_conexion()
    
    def mostrar_estado_actual(self):
        """Mostrar el estado actual de la configuración"""
        api_key = os.getenv('AEMET_API_KEY', 'No configurada')
        
        print("=" * 50)
        print("🔧 ESTADO CONFIGURACIÓN AEMET")
        print("=" * 50)
        
        # Ocultar parte de la API Key por seguridad
        if api_key and api_key != 'opcional' and api_key != 'TU_API_KEY_REAL':
            api_key_oculta = api_key[:20] + "..." + api_key[-10:]
            print(f"🔑 API Key: {api_key_oculta}")
        else:
            print("🔑 API Key: No configurada")
        
        # Verificar validez
        valida, mensaje = self.verificar_api_key()
        print(f"📋 Estado: {mensaje}")
        
        # Probar conexión si la key parece válida
        if valida:
            print("🌐 Probando conexión con AEMET...")
            if self.probar_conexion_aemet():
                print("✅ Conexión AEMET exitosa!")
            else:
                print("❌ No se pudo conectar con AEMET")
        
        print("=" * 50)

def extraer_api_key_desde_texto(texto):
    """Intentar extraer una API Key de un texto"""
    # Patrones comunes para API Keys
    patrones = [
        r'eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+',  # JWT standard
        r'api_key["\']?\s*[:=]\s*["\']([^"\']+)["\']',         # JSON format
        r'clave["\']?\s*[:=]\s*["\']([^"\']+)["\']',           # Spanish format
        r'[a-zA-Z0-9_-]{40,}',                                 # Long alphanumeric
    ]
    
    for patron in patrones:
        coincidencias = re.findall(patron, texto)
        if coincidencias:
            return coincidencias[0]
    
    return None

# Función principal de configuración
def configurar_aemet_interactivo():
    """Configuración interactiva de AEMET"""
    configurador = ConfiguradorAEMET()
    
    print("🎯 CONFIGURACIÓN INTERACTIVA AEMET OPENDATA")
    print("=" * 50)
    
    # Mostrar estado actual
    configurador.mostrar_estado_actual()
    
    # Opciones para el usuario
    print("\n💡 OPCIONES:")
    print("1. Introducir API Key manualmente")
    print("2. Pegar texto del correo para extracción automática")
    print("3. Continuar sin API Key (modo simulación)")
    print("4. Salir")
    
    opcion = input("\nSelecciona una opción (1-4): ").strip()
    
    if opcion == "1":
        api_key = input("🔑 Introduce tu API Key de AEMET: ").strip()
        if api_key:
            exito, mensaje = configurador.configurar_api_key(api_key)
            print(mensaje)
            if exito:
                configurador.mostrar_estado_actual()
        else:
            print("❌ No se introdujo ninguna API Key")
    
    elif opcion == "2":
        print("📋 Pega el contenido del correo de AEMET (Ctrl+D para finalizar):")
        print("=" * 40)
        
        lineas = []
        try:
            while True:
                linea = input()
                lineas.append(linea)
        except EOFError:
            pass
        
        texto_correo = "\n".join(lineas)
        api_key = extraer_api_key_desde_texto(texto_correo)
        
        if api_key:
            print(f"🔑 API Key detectada: {api_key[:20]}...{api_key[-10:]}")
            exito, mensaje = configurador.configurar_api_key(api_key)
            print(mensaje)
            configurador.mostrar_estado_actual()
        else:
            print("❌ No se pudo detectar ninguna API Key en el texto")
            print("💡 Intenta la opción 1 para introducirla manualmente")
    
    elif opcion == "3":
        print("✅ Continuando en modo simulación")
        print("💡 El sistema usará datos simulados inteligentes")
    
    elif opcion == "4":
        print("👋 Saliendo...")
        return
    
    else:
        print("❌ Opción no válida")

if __name__ == "__main__":
    configurar_aemet_interactivo()
