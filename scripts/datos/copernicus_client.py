#!/usr/bin/env python3
"""
🌊 COPERNICUS MARINE CLIENT - Datos oceánicos profesionales de la UE
"""

import logging
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class CopernicusMarineClient:
    """Cliente para Copernicus Marine Service"""

    def __init__(self):
        self.base_url = "https://data.marine.copernicus.eu"
        self.username = os.getenv('COPERNICUS_USERNAME', '')
        self.password = os.getenv('COPERNICUS_PASSWORD', '')

        logging.info("🌊 Iniciando Cliente Copernicus Marine")

    def obtener_datos_golfo_cadiz(self, product_type="GLOBAL_ANALYSIS_FORECAST_PHY_001_024"):
        """Obtener datos del Golfo de Cádiz"""
        try:
            # Coordenadas del Golfo de Cádiz
            bbox = [-9.0, 35.0, -5.0, 38.0]  # [lon_min, lat_min, lon_max, lat_max]

            # Parámetros para solicitud
            params = {
                'product': product_type,
                'variable': ['thetao', 'so', 'zos', 'uo', 'vo'],  # Temp, Salinidad, Nivel mar, corrientes
                'bbox': bbox,
                'start': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                'end': datetime.now().strftime('%Y-%m-%d'),
                'output': 'json'
            }

            # Intentar obtener datos
            return self._simular_datos_copernicus()  # Simulación por ahora

        except Exception as e:
            logging.error(f"❌ Error con Copernicus: {e}")
            return self._simular_datos_copernicus()

    def _simular_datos_copernicus(self):
        """Simular datos de Copernicus (modo fallback)"""
        from datetime import datetime
        import random

        return {
            'temperatura_superficie': round(19.5 + random.uniform(-1, 2), 2),
            'salinidad': round(36.2 + random.uniform(-0.5, 0.5), 2),
            'nivel_mar': round(0.1 + random.uniform(-0.2, 0.2), 3),
            'corriente_velocidad': round(0.3 + random.uniform(-0.1, 0.2), 2),
            'corriente_direccion': random.randint(180, 270),
            'timestamp': datetime.now().isoformat(),
            'fuente': 'COPERNICUS_SIMULADO',
            'nota': 'Datos simulados - Registrar en https://marine.copernicus.eu'
        }

    def verificar_conexion(self):
        """Verificar posibilidad de conexión"""
        try:
            # Simular verificación
            return {
                'estado': 'MODO_SIMULACION',
                'mensaje': 'Registrarse en https://marine.copernicus.eu para datos reales',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'estado': 'ERROR', 'mensaje': str(e)}

# Configuración específica para el Golfo de Cádiz
PRODUCTOS_COPERNICUS = {
    'temperatura': 'GLOBAL_ANALYSIS_FORECAST_PHY_001_024',
    'oleaje': 'GLOBAL_ANALYSIS_FORECAST_WAV_001_027',
    'bioquimica': 'GLOBAL_ANALYSIS_FORECAST_BIO_001_028'
}

def probar_copernicus():
    """Función de prueba para Copernicus"""
    print("=== 🌊 PRUEBA COPERNICUS MARINE ===")

    client = CopernicusMarineClient()
    resultado = client.verificar_conexion()

    print(f"📡 Estado: {resultado['estado']}")
    print(f"💡 Mensaje: {resultado['mensaje']}")

    # Obtener datos simulados
    datos = client.obtener_datos_golfo_cadiz()
    print(f"🌡️ Temperatura superficie: {datos['temperatura_superficie']}°C")
    print(f"🧂 Salinidad: {datos['salinidad']} PSU")
    print(f"🌊 Nivel mar: {datos['nivel_mar']} m")

    print("🔗 Registro: https://marine.copernicus.eu")

if __name__ == "__main__":
    probar_copernicus()
