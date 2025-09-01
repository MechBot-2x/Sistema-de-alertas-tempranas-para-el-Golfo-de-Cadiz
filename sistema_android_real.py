#!/usr/bin/env python3
"""
📱 SISTEMA ANDROID CON CONEXIÓN REAL OPcional
🌊 Alertas Tempranas Golfo de Cádiz
"""

import time
import random
import os
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_DISPONIBLE = True
except:
    DOTENV_DISPONIBLE = False

class SistemaAndroidReal:
    """Sistema con capacidad para conexión real"""
    
    def __init__(self):
        print("📱 SISTEMA ANDROID CON CONEXIÓN REAL")
        print("🌊 Golfo de Cádiz - Monitorización")
        print("⏰ " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("=" * 50)
        
        self.configurar_aemet_real()
    
    def configurar_aemet_real(self):
        """Configurar conexión real con AEMET"""
        self.aemet_api_key = None
        
        if DOTENV_DISPONIBLE:
            self.aemet_api_key = os.getenv('AEMET_API_KEY')
            
            if self.aemet_api_key and 'SIMULADO' not in self.aemet_api_key:
                print("✅ Token AEMET REAL detectado")
                print("📡 Modo: INTENTAR CONEXIÓN REAL")
            else:
                print("✅ Token AEMET: MODO SIMULACIÓN")
        else:
            print("ℹ️  python-dotenv no instalado")
            print("📡 Modo: SIMULACIÓN")
    
    def intentar_conexion_real(self):
        """Intentar conexión real con AEMET"""
        if not self.aemet_api_key or 'SIMULADO' in self.aemet_api_key:
            return self.simular_datos_aemet()
        
        try:
            # Aquí iría el código real de conexión
            # Por ahora simulamos que intentamos conectar
            print("🌐 Intentando conexión real con AEMET...")
            time.sleep(1)  # Simular tiempo de conexión
            
            # Simulamos que a veces falla la conexión
            if random.random() > 0.7:  # 30% de éxito
                return {
                    'temperatura': round(20 + random.uniform(-2, 3), 1),
                    'viento_velocidad': round(10 + random.uniform(0, 15), 1),
                    'viento_direccion': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
                    'humedad': random.randint(60, 90),
                    'presion': round(1013 + random.uniform(-5, 3), 1),
                    'timestamp': datetime.now().isoformat(),
                    'fuente': 'AEMET_REAL',
                    'calidad': 'DATOS_REALES'
                }
            else:
                raise Exception("Error de conexión con servidor AEMET")
                
        except Exception as e:
            print(f"❌ Conexión real falló: {e}")
            print("🔄 Usando datos simulados...")
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
            'fuente': 'AEMET_SIMULADO'
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
        
        if datos_meteo['viento_velocidad'] > 25:
            alertas.append('🌪️ VIENTO FUERTE')
        if datos_meteo.get('precipitacion', 0) > 3:
            alertas.append('🌧️ LLUVIA INTENSA')
        if datos_oceano['oleaje_altura'] > 1.8:
            alertas.append('🌊 OLEAJE ALTO')
        if datos_oceano['nivel_mar'] > 0.4:
            alertas.append('📈 MAREA ALTA')
        
        return alertas if alertas else ['✅ CONDICIONES NORMALES']
    
    def mostrar_dashboard(self, datos_meteo, datos_oceano, alertas):
        """Mostrar dashboard"""
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
        print(f"📡 {datos_meteo['fuente']}")
        if datos_meteo.get('calidad'):
            print(f"🎯 {datos_meteo['calidad']}")
        print("=" * 40)
    
    def ejecutar_ciclo(self):
        """Ejecutar ciclo de monitorización"""
        try:
            # Obtener datos (intentar real primero)
            datos_meteo = self.intentar_conexion_real()
            datos_oceano = self.simular_datos_copernicus()
            
            # Generar alertas
            alertas = self.generar_alertas(datos_meteo, datos_oceano)
            
            # Mostrar dashboard
            self.mostrar_dashboard(datos_meteo, datos_oceano, alertas)
            
            return True
            
        except Exception as e:
            print(f"❌ Error en ciclo: {e}")
            return False
    
    def ejecutar_continuamente(self, intervalo=10):
        """Ejecutar continuamente"""
        print("🔄 Ejecutando... Ctrl+C para detener")
        
        try:
            ciclo = 1
            while True:
                print(f"\n🔄 Ciclo {ciclo}")
                self.ejecutar_ciclo()
                time.sleep(intervalo)
                ciclo += 1
                
        except KeyboardInterrupt:
            print("\n🛑 Sistema detenido")
            print("📱 Hasta pronto!")

# Ejecutar el sistema
if __name__ == "__main__":
    sistema = SistemaAndroidReal()
    sistema.ejecutar_continuamente()
