#!/usr/bin/env python3
"""
🌊 COPERNICUS SIMPLIFICADO - Sin dependencias externas
"""

import time
from datetime import datetime
import random

class CopernicusSimple:
    """Cliente simplificado de Copernicus"""
    
    def __init__(self):
        print("🌊 Iniciando Copernicus Simple")
    
    def obtener_datos(self):
        """Obtener datos simulados"""
        return {
            'temperatura_superficie': round(19.5 + random.uniform(-1, 2), 2),
            'salinidad': round(36.2 + random.uniform(-0.5, 0.5), 2),
            'nivel_mar': round(0.1 + random.uniform(-0.2, 0.2), 3),
            'corriente_velocidad': round(0.3 + random.uniform(-0.1, 0.2), 2),
            'corriente_direccion': random.randint(180, 270),
            'timestamp': datetime.now().isoformat(),
            'fuente': 'COPERNICUS_SIMULADO',
            'nota': 'Modo simulación - Para datos reales: https://marine.copernicus.eu'
        }
    
    def verificar_conexion(self):
        """Verificar estado"""
        return {
            'estado': 'MODO_SIMULACION',
            'mensaje': 'Usando datos simulados. Registrarse en https://marine.copernicus.eu',
            'timestamp': datetime.now().isoformat()
        }

if __name__ == "__main__":
    client = CopernicusSimple()
    datos = client.obtener_datos()
    
    print("=== 🌊 DATOS COPERNICUS SIMULADOS ===")
    print(f"🌡️ Temperatura: {datos['temperatura_superficie']}°C")
    print(f"🧂 Salinidad: {datos['salinidad']} PSU")
    print(f"📈 Nivel mar: {datos['nivel_mar']} m")
    print(f"🌀 Corriente: {datos['corriente_velocidad']} m/s")
    print(f"💡 {datos['nota']}")
