#!/usr/bin/env python3
"""
🌊 SISTEMA AUTÓNOMO DE ALERTAS - Golfo de Cádiz
No requiere instalación de dependencias externas
"""

import time
import random
import json
from datetime import datetime, timedelta

class SistemaAutonomoAlertas:
    """Sistema completo de alertas sin dependencias externas"""
    
    def __init__(self):
        print("🚀 SISTEMA AUTÓNOMO DE ALERTAS INICIADO")
        print("📍 Golfo de Cádiz - Monitorización Integral")
        print("🌊 Incluye datos de Copernicus Marine (simulados)")
        print("⏰ " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("=" * 60)
    
    def simular_datos_copernicus(self):
        """Simular datos profesionales de Copernicus Marine"""
        return {
            'temperatura_superficie': round(19.5 + random.uniform(-1, 2), 2),
            'salinidad': round(36.2 + random.uniform(-0.5, 0.5), 2),
            'nivel_mar': round(0.1 + random.uniform(-0.2, 0.2), 3),
            'corriente_velocidad': round(0.3 + random.uniform(-0.1, 0.2), 2),
            'corriente_direccion': random.randint(180, 270),
            'oleaje_altura': round(0.8 + random.uniform(0, 2.0), 2),
            'oleaje_periodo': round(6 + random.uniform(-2, 4), 1),
            'timestamp': datetime.now().isoformat(),
            'fuente': 'COPERNICUS_MARINE_SIMULADO',
            'nota': 'Para datos reales: https://marine.copernicus.eu'
        }
    
    def simular_datos_aemet(self):
        """Simular datos de AEMET"""
        return {
            'temperatura_aire': round(20 + random.uniform(-3, 5), 1),
            'humedad': random.randint(50, 95),
            'viento_velocidad': round(8 + random.uniform(0, 20), 1),
            'viento_direccion': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
            'presion_atmosferica': round(1015 + random.uniform(-8, 5), 1),
            'precipitacion': round(random.uniform(0, 5), 1),
            'timestamp': datetime.now().isoformat(),
            'fuente': 'AEMET_SIMULADO'
        }
    
    def calcular_riesgo_tsunami(self, datos_oceanicos):
        """Calcular riesgo de tsunami basado en datos oceánicos"""
        riesgo = 0.0
        
        # Factores de riesgo (algoritmo simplificado)
        if datos_oceanicos['nivel_mar'] > 0.4:
            riesgo += 0.3
        if datos_oceanicos['corriente_velocidad'] > 0.8:
            riesgo += 0.2
        if datos_oceanicos['oleaje_altura'] > 1.5:
            riesgo += 0.2
        
        return min(riesgo, 1.0)
    
    def clasificar_estado_mareal(self, datos_oceanicos):
        """Clasificar estado mareal"""
        nivel = datos_oceanicos['nivel_mar']
        
        if nivel > 0.3:
            return "PLEAMAR"
        elif nivel < -0.3:
            return "BAJAMAR"
        else:
            return "NORMAL"
    
    def generar_alertas_integradas(self, datos_meteo, datos_oceano):
        """Generar alertas integradas basadas en todos los datos"""
        alertas = []
        
        # Alertas meteorológicas
        if datos_meteo['viento_velocidad'] > 25:
            alertas.append('🌪️ ALERTA: VIENTOS FUERTES')
        if datos_meteo['precipitacion'] > 3:
            alertas.append('🌧️ ALERTA: LLUVIA INTENSA')
        
        # Alertas oceánicas
        if datos_oceano['oleaje_altura'] > 2.0:
            alertas.append('🌊 ALERTA: OLEAJE PELIGROSO')
        
        # Riesgo de tsunami
        riesgo_tsunami = self.calcular_riesgo_tsunami(datos_oceano)
        if riesgo_tsunami > 0.5:
            alertas.append(f'🌋 ALERTA: RIESGO TSUNAMI ({riesgo_tsunami:.1%})')
        
        return alertas if alertas else ['✅ CONDICIONES NORMALES']
    
    def mostrar_dashboard(self, datos_meteo, datos_oceano, alertas):
        """Mostrar dashboard completo"""
        print(f"\n🎯 DASHBOARD - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        print("🌤️  DATOS METEOROLÓGICOS (AEMET):")
        print(f"   🌡️  Temperatura: {datos_meteo['temperatura_aire']}°C")
        print(f"   💨 Viento: {datos_meteo['viento_velocidad']} km/h {datos_meteo['viento_direccion']}")
        print(f"   💧 Humedad: {datos_meteo['humedad']}%")
        print(f"   📊 Presión: {datos_meteo['presion_atmosferica']} hPa")
        print(f"   🌧️  Precipitación: {datos_meteo['precipitacion']} mm")
        
        print("\n🌊 DATOS OCEÁNICOS (COPERNICUS MARINE):")
        print(f"   🌡️  Temp. superficie: {datos_oceano['temperatura_superficie']}°C")
        print(f"   🧂 Salinidad: {datos_oceano['salinidad']} PSU")
        print(f"   📈 Nivel mar: {datos_oceano['nivel_mar']} m")
        print(f"   🌀 Corrientes: {datos_oceano['corriente_velocidad']} m/s → {datos_oceano['corriente_direccion']}°")
        print(f"   🌊 Oleaje: {datos_oceano['oleaje_altura']} m cada {datos_oceano['oleaje_periodo']}s")
        
        print(f"\n📊 ANÁLISIS INTEGRADO:")
        print(f"   🎯 Estado mareal: {self.clasificar_estado_mareal(datos_oceano)}")
        print(f"   ⚠️  Riesgo tsunami: {self.calcular_riesgo_tsunami(datos_oceano):.1%}")
        
        print(f"\n🚨 SISTEMA DE ALERTAS:")
        for alerta in alertas:
            print(f"   {alerta}")
        
        print("=" * 60)
        print(f"📡 Fuente: {datos_oceano['fuente']}")
        print(f"💡 {datos_oceano['nota']}")
        print("=" * 60)
    
    def ejecutar_ciclo(self):
        """Ejecutar un ciclo completo de monitorización"""
        try:
            # Obtener datos de todas las fuentes
            datos_copernicus = self.simular_datos_copernicus()
            datos_aemet = self.simular_datos_aemet()
            
            # Generar alertas
            alertas = self.generar_alertas_integradas(datos_aemet, datos_copernicus)
            
            # Mostrar dashboard
            self.mostrar_dashboard(datos_aemet, datos_copernicus, alertas)
            
            return True
            
        except Exception as e:
            print(f"❌ Error en ciclo: {e}")
            return False
    
    def ejecutar_continuamente(self, intervalo=15):
        """Ejecutar el sistema continuamente"""
        print("🔄 Sistema ejecutándose. Presiona Ctrl+C para detener...")
        
        try:
            ciclo_numero = 1
            while True:
                print(f"\n🔄 CICLO {ciclo_numero}")
                self.ejecutar_ciclo()
                time.sleep(intervalo)
                ciclo_numero += 1
                
        except KeyboardInterrupt:
            print("\n🛑 Sistema detenido por el usuario")
            print("🌊 Hasta pronto!")

# Ejecutar el sistema autónomo
if __name__ == "__main__":
    sistema = SistemaAutonomoAlertas()
    sistema.ejecutar_continuamente()
