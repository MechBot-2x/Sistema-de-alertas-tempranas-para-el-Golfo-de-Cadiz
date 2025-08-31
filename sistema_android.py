#!/usr/bin/env python3
"""
📱 SISTEMA OPTIMIZADO PARA ANDROID/TERMUX - CORREGIDO
🌊 Alertas Tempranas Golfo de Cádiz
"""

import time
import random
import json
import os
from datetime import datetime, timedelta

class SistemaAndroid:
    """Sistema optimizado para Termux/Android - Versión corregida"""
    
    def __init__(self):
        print("📱 SISTEMA ANDROID INICIADO")
        print("🌊 Golfo de Cádiz - Monitorización")
        print("⏰ " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("=" * 50)
        
        # Cargar configuración
        self.cargar_configuracion()
    
    def cargar_configuracion(self):
        """Cargar configuración desde variables de entorno"""
        try:
            # Simular carga de .env para Android
            self.aemet_api_key = os.getenv('AEMET_API_KEY', 'SIMULADO_1234567890')
            self.copernicus_user = os.getenv('COPERNICUS_USERNAME', 'usuario_simulado')
            self.copernicus_pass = os.getenv('COPERNICUS_PASSWORD', 'password_simulado')
            
            print(f"✅ Configuración cargada")
            print(f"📡 AEMET: {'CONFIGURADO' if 'SIMULADO' not in self.aemet_api_key else 'MODO SIMULACIÓN'}")
            
        except Exception as e:
            print(f"❌ Error config: {e}")
    
    def obtener_datos_aemet_reales(self):
        """Intentar obtener datos reales de AEMET"""
        try:
            # Simulación de conexión real (para implementar luego)
            return {
                'estado': 'SIMULADO',
                'temperatura': round(20 + random.uniform(-3, 5), 1),
                'viento_velocidad': round(8 + random.uniform(0, 20), 1),
                'viento_direccion': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
                'humedad': random.randint(50, 95),
                'presion': round(1015 + random.uniform(-8, 5), 1),
                'precipitacion': round(random.uniform(0, 5), 1),
                'timestamp': datetime.now().isoformat(),
                'fuente': 'AEMET_SIMULADO',  # ✅ CORREGIDO: Añadida clave 'fuente'
                'mensaje': 'Token AEMET configurado. Implementar API real.'
            }
        except Exception as e:
            return self.simular_datos_aemet()
    
    def simular_datos_aemet(self):
        """Simular datos AEMET"""
        return {
            'temperatura': round(20 + random.uniform(-3, 5), 1),
            'viento_velocidad': round(8 + random.uniform(0, 20), 1),
            'viento_direccion': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
            'humedad': random.randint(50, 95),
            'presion': round(1015 + random.uniform(-8, 5), 1),
            'precipitacion': round(random.uniform(0, 5), 1),
            'timestamp': datetime.now().isoformat(),
            'fuente': 'AEMET_SIMULADO'  # ✅ CORREGIDO: Añadida clave 'fuente'
        }
    
    def simular_datos_copernicus(self):
        """Simular datos Copernicus"""
        return {
            'temperatura_agua': round(18 + random.uniform(-1, 3), 1),
            'salinidad': round(36.2 + random.uniform(-0.5, 0.5), 2),
            'nivel_mar': round(0.1 + random.uniform(-0.2, 0.2), 3),
            'oleaje_altura': round(0.8 + random.uniform(0, 2.0), 2),
            'oleaje_periodo': round(6 + random.uniform(-2, 4), 1),
            'timestamp': datetime.now().isoformat(),
            'fuente': 'COPERNICUS_SIMULADO'
        }
    
    def generar_alertas(self, datos_meteo, datos_oceano):
        """Generar alertas integradas"""
        alertas = []
        
        # Alertas meteorológicas
        if datos_meteo['viento_velocidad'] > 25:
            alertas.append('🌪️ VIENTO FUERTE')
        if datos_meteo.get('precipitacion', 0) > 3:
            alertas.append('🌧️ LLUVIA INTENSA')
        
        # Alertas oceánicas
        if datos_oceano['oleaje_altura'] > 1.8:
            alertas.append('🌊 OLEAJE ALTO')
        if datos_oceano['nivel_mar'] > 0.4:
            alertas.append('📈 MAREA ALTA')
        
        return alertas if alertas else ['✅ CONDICIONES NORMALES']
    
    def mostrar_dashboard(self, datos_meteo, datos_oceano, alertas):
        """Mostrar dashboard optimizado para móvil"""
        print(f"\n📊 DASHBOARD - {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 40)
        
        print("🌤️  METEOROLOGÍA:")
        print(f"   🌡️  {datos_meteo['temperatura']}°C")
        print(f"   💨 {datos_meteo['viento_velocidad']} km/h {datos_meteo['viento_direccion']}")
        print(f"   💧 {datos_meteo['humedad']}%")
        
        print("\n🌊 OCÉANO:")
        print(f"   🌡️  {datos_oceano['temperatura_agua']}°C")
        print(f"   🌊 {datos_oceano['oleaje_altura']} m")
        print(f"   📈 {datos_oceano['nivel_mar']} m")
        
        print(f"\n🚨 ALERTAS:")
        for alerta in alertas:
            print(f"   {alerta}")
        
        print("=" * 40)
        print(f"📡 {datos_meteo.get('fuente', 'SISTEMA_LOCAL')}")  # ✅ CORREGIDO: Usar get() por seguridad
        print("=" * 40)
    
    def ejecutar_ciclo(self):
        """Ejecutar ciclo de monitorización"""
        try:
            # Obtener datos
            datos_meteo = self.obtener_datos_aemet_reales()
            datos_oceano = self.simular_datos_copernicus()
            
            # Generar alertas
            alertas = self.generar_alertas(datos_meteo, datos_oceano)
            
            # Mostrar dashboard
            self.mostrar_dashboard(datos_meteo, datos_oceano, alertas)
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def ejecutar_continuamente(self, intervalo=10):
        """Ejecutar continuamente"""
        print("🔄 Ejecutando... Ctrl+C para detener")
        
        try:
            ciclo = 1
            while True:
                print(f"\n🔄 Ciclo {ciclo}")
                success = self.ejecutar_ciclo()
                if not success:
                    print("⚠️  Reintentando en 5 segundos...")
                    time.sleep(5)
                else:
                    time.sleep(intervalo)
                ciclo += 1
                
        except KeyboardInterrupt:
            print("\n🛑 Sistema detenido")
            print("📱 Hasta pronto!")

# Ejecutar el sistema
if __name__ == "__main__":
    sistema = SistemaAndroid()
    sistema.ejecutar_continuamente()
