#!/usr/bin/env python3
"""
🚨 SISTEMA DE ALERTAS SIMPLIFICADO - Sin dependencias externas
"""

import time
import random
from datetime import datetime

class SistemaAlertasSimplificado:
    """Sistema simplificado para el Golfo de Cádiz"""
    
    def __init__(self):
        print("🌊 INICIANDO SISTEMA SIMPLIFICADO DE ALERTAS")
        print("📍 Golfo de Cádiz - Monitorización Básica")
    
    def obtener_datos_meteorologicos(self):
        """Simular datos meteorológicos"""
        return {
            'temperatura': round(20 + random.uniform(-2, 5), 1),
            'viento_velocidad': round(5 + random.uniform(0, 15), 1),
            'viento_direccion': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
            'presion': round(1013 + random.uniform(-10, 5), 1),
            'timestamp': datetime.now().isoformat()
        }
    
    def obtener_datos_oceanicos(self):
        """Simular datos oceánicos"""
        return {
            'temperatura_agua': round(18 + random.uniform(-1, 3), 1),
            'oleaje_altura': round(0.5 + random.uniform(0, 2.5), 1),
            'oleaje_periodo': round(5 + random.uniform(0, 8), 1),
            'oleaje_direccion': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
            'marea_altura': round(1.0 + random.uniform(-0.8, 0.8), 2),
            'timestamp': datetime.now().isoformat()
        }
    
    def analizar_riesgos(self, datos_meteo, datos_oceano):
        """Analizar riesgos integrados"""
        riesgos = []
        
        # Riesgo por viento fuerte
        if datos_meteo['viento_velocidad'] > 20:
            riesgos.append('⚠️ VIENTO FUERTE')
        
        # Riesgo por oleaje alto
        if datos_oceano['oleaje_altura'] > 2.0:
            riesgos.append('🌊 OLEAJE ALTO')
        
        # Riesgo por temperatura baja
        if datos_meteo['temperatura'] < 15:
            riesgos.append('❄️ TEMPERATURA BAJA')
        
        return riesgos if riesgos else ['✅ CONDICIONES NORMALES']
    
    def ejecutar_ciclo(self):
        """Ejecutar un ciclo de monitorización"""
        print(f"\n🕐 CICLO DE MONITORIZACIÓN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        # Obtener datos
        datos_meteo = self.obtener_datos_meteorologicos()
        datos_oceano = self.obtener_datos_oceanicos()
        
        # Mostrar datos
        print("🌤️  METEOROLOGÍA:")
        print(f"   Temperatura: {datos_meteo['temperatura']}°C")
        print(f"   Viento: {datos_meteo['viento_velocidad']} km/h {datos_meteo['viento_direccion']}")
        print(f"   Presión: {datos_meteo['presion']} hPa")
        
        print("\n🌊 DATOS OCEÁNICOS:")
        print(f"   Temp. agua: {datos_oceano['temperatura_agua']}°C")
        print(f"   Oleaje: {datos_oceano['oleaje_altura']} m cada {datos_oceano['oleaje_periodo']}s")
        print(f"   Marea: {datos_oceano['marea_altura']} m")
        
        # Analizar riesgos
        riesgos = self.analizar_riesgos(datos_meteo, datos_oceano)
        print(f"\n🚨 ALERTAS: {', '.join(riesgos)}")
        
        print("=" * 50)
    
    def ejecutar_continuamente(self, intervalo_segundos=10):
        """Ejecutar continuamente"""
        try:
            while True:
                self.ejecutar_ciclo()
                time.sleep(intervalo_segundos)
        except KeyboardInterrupt:
            print("\n🛑 Sistema detenido por el usuario")

if __name__ == "__main__":
    sistema = SistemaAlertasSimplificado()
    sistema.ejecutar_continuamente()
