#!/usr/bin/env python3
"""
📡 CLIENTE AEMET REAL FUNCIONAL
Usando tu token real para obtener datos
"""

import requests
import os
import json
from datetime import datetime

class AEMETReal:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://opendata.aemet.es/opendata/api"
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def obtener_estaciones_golfo_cadiz(self):
        """Obtener estaciones meteorológicas del Golfo de Cádiz"""
        # Este es un endpoint de ejemplo - necesitarías ajustar según documentación AEMET
        url = f"{self.base_url}/red/especial/estaciones?api_key={self.api_key}"
        
        try:
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                datos = response.json()
                return {
                    'estado': 'EXITO',
                    'datos': datos,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'estado': 'ERROR',
                    'codigo': response.status_code,
                    'mensaje': 'Revisar token AEMET o endpoint',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                'estado': 'ERROR',
                'mensaje': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def probar_conexion(self):
        """Probar la conexión con AEMET"""
        resultado = self.obtener_estaciones_golfo_cadiz()
        return resultado

# Función para probar la conexión real
def probar_aemet_real():
    """Probar la conexión real con AEMET"""
    print("🔍 PROBANDO CONEXIÓN REAL CON AEMET")
    print("=" * 40)
    
    # Cargar token desde .env
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('AEMET_API_KEY')
    
    if not api_key or 'SIMULADO' in api_key:
        print("❌ Token AEMET no configurado correctamente")
        print("💡 Verifica el archivo .env")
        return
    
    print(f"✅ Token AEMET cargado: {api_key[:20]}...")
    
    # Crear cliente
    cliente = AEMETReal(api_key)
    
    # Probar conexión
    print("📡 Conectando con AEMET...")
    resultado = cliente.probar_conexion()
    
    print(f"📊 Estado: {resultado['estado']}")
    if resultado['estado'] == 'EXITO':
        print("🎉 ¡Conexión exitosa con AEMET!")
        print(f"📦 Datos recibidos: {len(str(resultado['datos']))} caracteres")
    else:
        print(f"❌ Error: {resultado.get('mensaje', 'Desconocido')}")
        print(f"🔍 Código: {resultado.get('codigo', 'N/A')}")
        print("💡 Revisa la documentación de AEMET para endpoints correctos")

if __name__ == "__main__":
    probar_aemet_real()
