#!/usr/bin/env python3
"""
📡 CLIENTE AEMET REAL - Para implementar con tu token
"""

import requests
import os

class AEMETReal:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://opendata.aemet.es/opendata/api"
        
    def obtener_datos_golfo_cadiz(self):
        """Obtener datos reales del Golfo de Cádiz"""
        # URL de ejemplo (necesitas ajustar endpoints específicos)
        url = f"{self.base_url}/prediccion/especifica/playa/1/{self.api_key}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}", "mensaje": "Revisar token AEMET"}
                
        except Exception as e:
            return {"error": str(e), "modo": "simulacion"}
