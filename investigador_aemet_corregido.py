#!/usr/bin/env python3
"""
🔍 INVESTIGADOR DE ENDPOINTS AEMET - CORREGIDO
Ayuda a encontrar los endpoints correctos para tu token
"""

import requests
import os
import time  # ✅ CORREGIDO: Importar time
from dotenv import load_dotenv

load_dotenv()

class InvestigadorAEMET:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://opendata.aemet.es/opendata/api"
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Termux; Android)'
        }
    
    def probar_endpoint(self, endpoint, nombre):
        """Probar un endpoint específico"""
        print(f"\n🔍 Probando: {nombre}")
        print(f"📡 Endpoint: {endpoint}")
        
        url = f"{self.base_url}{endpoint}?api_key={self.api_key}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ ¡Éxito! Endpoint funciona")
                print(f"📦 Datos: {response.text[:100]}...")
                return True
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"📄 Respuesta: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"💥 Excepción: {e}")
            return False
    
    def investigar_endpoints(self):
        """Investigar varios endpoints comunes"""
        endpoints = [
            ("/valores/climatologicos/inventarioestaciones/todasestaciones", "Inventario estaciones"),
            ("/maestro/municipios", "Maestro municipios"),
            ("/observacion/convencional/todas", "Observación convencional"),
            ("/prediccion/especifica/playa/1/", "Predicción playas"),
            ("/api/red/radar/", "Datos radar"),
            ("/antiguos_web/observacion/ultimodato", "Últimos datos")
        ]
        
        print("🔍 INVESTIGACIÓN ENDPOINTS AEMET")
        print("=" * 50)
        print(f"🔑 Token: {self.api_key[:20]}...")
        print("=" * 50)
        
        resultados = []
        
        for endpoint, nombre in endpoints:
            resultado = self.probar_endpoint(endpoint, nombre)
            resultados.append((endpoint, nombre, resultado))
            time.sleep(2)  # ✅ CORREGIDO: Esperar entre requests
        
        print("\n" + "=" * 50)
        print("📊 RESUMEN DE INVESTIGACIÓN:")
        for endpoint, nombre, resultado in resultados:
            status = "✅ FUNCIONA" if resultado else "❌ FALLA"
            print(f"{status} - {nombre}")
        
        print("\n💡 RECOMENDACIONES:")
        print("1. Visita: https://opendata.aemet.es/centrodedescargas/inicio")
        print("2. Busca endpoints para 'Andalucía' o 'Cádiz'")
        print("3. Los timeouts pueden ser por bloqueo de Termux")

def main():
    api_key = os.getenv('AEMET_API_KEY')
    
    if not api_key:
        print("❌ No se encontró AEMET_API_KEY en .env")
        return
    
    investigador = InvestigadorAEMET(api_key)
    investigador.investigar_endpoints()

if __name__ == "__main__":
    main()
