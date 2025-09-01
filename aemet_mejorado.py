#!/usr/bin/env python3
"""
📡 CLIENTE AEMET MEJORADO - Endpoints correctos
Documentación: https://opendata.aemet.es/centrodedescargas/inicio
"""

import requests
import os
import json
from datetime import datetime

class AEMETMejorado:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://opendata.aemet.es/opendata/api"
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    
    def obtener_datos_observacion(self, estacion="ESTACION_GOLFO_CADIZ"):
        """Obtener datos de observación - Endpoint más común"""
        # Endpoint de datos de observación convencional
        url = f"{self.base_url}/observacion/convencional/datos/estacion/{estacion}"
        url_completa = f"{url}?api_key={self.api_key}"
        
        try:
            print(f"🔗 Conectando a: {url}")
            response = requests.get(url_completa, headers=self.headers)
            
            print(f"📊 Código respuesta: {response.status_code}")
            
            if response.status_code == 200:
                datos = response.json()
                return {
                    'estado': 'EXITO',
                    'datos': datos,
                    'timestamp': datetime.now().isoformat()
                }
            elif response.status_code == 401:
                return {
                    'estado': 'ERROR',
                    'codigo': 401,
                    'mensaje': 'Token AEMET inválido o no autorizado',
                    'timestamp': datetime.now().isoformat()
                }
            elif response.status_code == 404:
                return {
                    'estado': 'ERROR',
                    'codigo': 404,
                    'mensaje': 'Endpoint no encontrado. Revisar documentación AEMET',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'estado': 'ERROR',
                    'codigo': response.status_code,
                    'mensaje': response.text[:200],
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                'estado': 'ERROR',
                'mensaje': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def obtener_estaciones_playa(self):
        """Obtener datos de estaciones de playa - Puede ser más útil"""
        url = f"{self.base_url}/observacion/playas?api_key={self.api_key}"
        
        try:
            print(f"🏖️  Obteniendo datos de playas...")
            response = requests.get(url, headers=self.headers)
            
            print(f"📊 Código: {response.status_code}")
            
            if response.status_code == 200:
                return {
                    'estado': 'EXITO',
                    'datos': response.json(),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'estado': 'ERROR',
                    'codigo': response.status_code,
                    'mensaje': response.text[:200],
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                'estado': 'ERROR',
                'mensaje': str(e),
                'timestamp': datetime.now().isoformat()
            }

def probar_aemet_mejorado():
    """Probar conexión con endpoints mejorados"""
    print("🔍 PROBANDO CONEXIÓN AEMET MEJORADA")
    print("=" * 50)
    
    # Cargar token desde .env
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('AEMET_API_KEY')
    
    if not api_key or 'SIMULADO' in api_key:
        print("❌ Token AEMET no configurado en .env")
        print("💡 Verifica que el token esté en el archivo .env")
        return
    
    print(f"✅ Token AEMET detectado: {api_key[:15]}...")
    
    # Crear cliente
    cliente = AEMETMejorado(api_key)
    
    print("\n1. 🏖️ Probando endpoint de playas...")
    resultado_playas = cliente.obtener_estaciones_playa()
    print(f"   Estado: {resultado_playas['estado']}")
    
    if resultado_playas['estado'] == 'ERROR':
        print(f"   Error: {resultado_playas.get('mensaje', 'Desconocido')}")
        print(f"   Código: {resultado_playas.get('codigo', 'N/A')}")
    
    print("\n2. 🌤️ Probando endpoint de observación...")
    resultado_obs = cliente.obtener_datos_observacion("5514A")  # Ejemplo de código estación
    print(f"   Estado: {resultado_obs['estado']}")
    
    if resultado_obs['estado'] == 'ERROR':
        print(f"   Error: {resultado_obs.get('mensaje', 'Desconocido')}")
        print(f"   Código: {resultado_obs.get('codigo', 'N/A')}")
    
    print("\n" + "=" * 50)
    print("📚 Documentación AEMET: https://opendata.aemet.es/centrodedescargas/inicio")
    print("🔑 Necesitarás investigar los endpoints específicos para el Golfo de Cádiz")

if __name__ == "__main__":
    probar_aemet_mejorado()
