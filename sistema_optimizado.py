#!/usr/bin/env python3
"""
🌊 SISTEMA OPTIMIZADO - Mejorado para conexiones móviles
"""

import requests
import time
from sistema_aemet_real import SistemaAEMETReal

class SistemaOptimizado(SistemaAEMETReal):
    def __init__(self):
        super().__init__()
        # Timeout optimizado para móviles
        self.timeout = 30
        self.max_reintentos = 3
        
    def obtener_datos_reales_optimizado(self):
        """Versión optimizada para conexiones móviles"""
        for intento in range(self.max_reintentos):
            try:
                print(f"📡 Intento {intento + 1}/{self.max_reintentos}...")
                
                # Endpoint más confiable
                url = f"{self.base_url}/valores/climatologicos/inventarioestaciones/todasestaciones"
                url_completa = f"{url}?api_key={self.api_key}"
                
                response = requests.get(url_completa, headers=self.headers, timeout=self.timeout)
                
                if response.status_code == 200:
                    print("✅ Datos reales recibidos de AEMET")
                    return self._procesar_datos_reales(response.json()), "AEMET_REAL"
                else:
                    print(f"⚠️ Intento {intento + 1} falló: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error en intento {intento + 1}: {e}")
                time.sleep(5)  # Esperar entre intentos
        
        print("🔄 Usando datos simulados tras múltiples intentos")
        return self._datos_simulados_mejorados(), "AEMET_SIMULADO"

# Ejecutar sistema optimizado
if __name__ == "__main__":
    sistema = SistemaOptimizado()
    sistema.iniciar_servicio_oficial()
