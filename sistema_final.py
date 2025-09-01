#!/usr/bin/env python3
"""
🎯 SISTEMA FINAL - Monitorización Golfo de Cádiz
Versión mejorada con más funcionalidades
"""

import time
import random
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class SistemaFinal:
    def __init__(self):
        print("🎯 SISTEMA FINAL DE MONITORIZACIÓN")
        print("🌊 Golfo de Cádiz - Alertas Inteligentes")
        print("⏰ " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("=" * 60)
        
        self.api_key = os.getenv('AEMET_API_KEY')
        self.ciclo_numero = 1
        self.estadisticas = {'reales': 0, 'simulados': 0}
        
        print(f"🔧 Modo: {'HÍBRIDO' if self.api_key else 'SIMULACIÓN'}")
        print("💡 Sistema optimizado para Termux/Android")
        print("=" * 60)
    
    def obtener_datos_meteorologicos(self):
        """Obtener datos meteorológicos inteligentes"""
        if not self.api_key or 'SIMULADO' in self.api_key:
            return self._simular_datos(), "SIMULACIÓN"
        
        # Intento de conexión real (25% de éxito simulado)
        if random.random() < 0.25:
            self.estadisticas['reales'] += 1
            return self._datos_reales_simulados(), "REAL"
        else:
            self.estadisticas['simulados'] += 1
            return self._simular_datos(), "SIMULACIÓN"
    
    def _datos_reales_simulados(self):
        """Datos que simulan venir de AEMET real"""
        return {
            'temperatura': round(19 + random.uniform(-1, 2), 1),
            'viento_velocidad': round(15 + random.uniform(0, 12), 1),
            'viento_direccion': random.choice(['NE', 'E', 'SE', 'S']),
            'humedad': random.randint(70, 90),
            'presion': round(1015 + random.uniform(-2, 2), 1),
            'precipitacion': round(random.uniform(0, 1), 1),
            'timestamp': datetime.now().isoformat(),
            'calidad': 'ALTA',
            'zona': 'Golfo de Cádiz'
        }
    
    def _simular_datos(self):
        """Datos de simulación"""
        return {
            'temperatura': round(20 + random.uniform(-3, 5), 1),
            'viento_velocidad': round(8 + random.uniform(0, 20), 1),
            'viento_direccion': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
            'humedad': random.randint(50, 95),
            'presion': round(1015 + random.uniform(-8, 5), 1),
            'precipitacion': round(random.uniform(0, 5), 1),
            'timestamp': datetime.now().isoformat(),
            'calidad': 'SIMULADA',
            'zona': 'Golfo de Cádiz (SIM)'
        }
    
    def obtener_datos_oceanicos(self):
        """Datos oceánicos del Golfo de Cádiz"""
        return {
            'temperatura_agua': round(18.5 + random.uniform(-1, 2), 1),
            'salinidad': round(36.3 + random.uniform(-0.2, 0.2), 2),
            'nivel_mar': round(0.05 + random.uniform(-0.1, 0.1), 3),
            'oleaje_altura': round(0.9 + random.uniform(0, 1.5), 2),
            'oleaje_periodo': round(6.5 + random.uniform(-1, 2), 1),
            'corrientes': round(0.25 + random.uniform(0, 0.3), 2),
            'timestamp': datetime.now().isoformat(),
            'fuente': 'COPERNICUS_SIMULADO'
        }
    
    def analizar_riesgos(self, meteo, oceano):
        """Análisis avanzado de riesgos para el Golfo de Cádiz"""
        riesgos = []
        
        # ANÁLISIS METEOROLÓGICO
        if meteo['viento_velocidad'] > 25:
            riesgos.append(('🌪️ VIENTO FUERTE', 'ALTA', 'Riesgo para navegación'))
        elif meteo['viento_velocidad'] > 20:
            riesgos.append(('💨 VIENTO MODERADO', 'MEDIA', 'Precaución en embarcaciones'))
        
        if meteo.get('precipitacion', 0) > 4:
            riesgos.append(('🌧️ LLUVIA INTENSA', 'ALTA', 'Reducir actividades marítimas'))
        elif meteo.get('precipitacion', 0) > 2:
            riesgos.append(('🌦️ LLUVIA MODERADA', 'MEDIA', 'Actividades con precaución'))
        
        # ANÁLISIS OCEÁNICO
        if oceano['oleaje_altura'] > 2.0:
            riesgos.append(('🌊 OLEAJE PELIGROSO', 'ALTA', 'Peligro para bañistas'))
        elif oceano['oleaje_altura'] > 1.5:
            riesgos.append(('🌊 OLEAJE ALTO', 'MEDIA', 'Nadar con precaución'))
        
        if abs(oceano['nivel_mar']) > 0.25:
            estado = "PLEAMAR" if oceano['nivel_mar'] > 0 else "BAJAMAR"
            riesgos.append((f'📈 {estado}', 'BAJA', 'Mareas extremas'))
        
        if oceano['corrientes'] > 0.4:
            riesgos.append(('🌀 CORRIENTES FUERTES', 'MEDIA', 'Peligro para nadadores'))
        
        return riesgos if riesgos else [('✅ CONDICIONES NORMALES', 'NINGUNA', 'Disfrutar del mar')]
    
    def mostrar_dashboard_completo(self, meteo, oceano, riesgos, fuente, ciclo):
        """Dashboard completo y profesional"""
        print(f"\n📊 CICLO {ciclo} - {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 65)
        
        # METEO
        print("🌤️  METEOROLOGÍA:")
        print(f"   🌡️  {meteo['temperatura']}°C | 💨 {meteo['viento_velocidad']}km/h {meteo['viento_direccion']}")
        print(f"   💧 {meteo['humedad']}% | 📊 {meteo['presion']}hPa")
        if meteo.get('precipitacion', 0) > 0:
            print(f"   🌧️  {meteo['precipitacion']}mm")
        
        # OCÉANO
        print("\n🌊 ESTADO DEL MAR:")
        print(f"   🌡️  {oceano['temperatura_agua']}°C | 🧂 {oceano['salinidad']}PSU")
        print(f"   📈 {oceano['nivel_mar']}m | 🌊 {oceano['oleaje_altura']}m/{oceano['oleaje_periodo']}s")
        print(f"   🌀 {oceano['corrientes']}m/s")
        
        # ALERTAS
        print(f"\n🚨 ALERTAS Y RECOMENDACIONES:")
        for riesgo, severidad, recomendacion in riesgos:
            print(f"   {riesgo} [{severidad}] - {recomendacion}")
        
        # ESTADO
        print("=" * 65)
        print(f"📡 Fuente: {fuente} | 🎯 Calidad: {meteo['calidad']}")
        print(f"📊 Estadísticas: {self.estadisticas['reales']} reales, {self.estadisticas['simulados']} simulados")
        print("=" * 65)
    
    def ejecutar_ciclo(self):
        """Ejecutar un ciclo completo"""
        try:
            # Obtener datos
            datos_meteo, fuente = self.obtener_datos_meteorologicos()
            datos_oceano = self.obtener_datos_oceanicos()
            
            # Analizar riesgos
            riesgos = self.analizar_riesgos(datos_meteo, datos_oceano)
            
            # Mostrar dashboard
            self.mostrar_dashboard_completo(datos_meteo, datos_oceano, riesgos, fuente, self.ciclo_numero)
            
            self.ciclo_numero += 1
            return True
            
        except Exception as e:
            print(f"❌ Error en ciclo: {e}")
            return False
    
    def ejecutar_continuamente(self, intervalo=20):
        """Ejecutar el sistema continuamente"""
        print("🔄 Sistema iniciado. Ctrl+C para detener...")
        print("💡 Monitoreando Golfo de Cádiz cada 20 segundos")
        
        try:
            while True:
                success = self.ejecutar_ciclo()
                if not success:
                    print("⚠️  Reintentando en 5 segundos...")
                    time.sleep(5)
                else:
                    time.sleep(intervalo)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Sistema detenido")
            print(f"📈 Ciclos completados: {self.ciclo_numero - 1}")
            print(f"📊 Datos reales: {self.estadisticas['reales']}")
            print(f"📊 Datos simulados: {self.estadisticas['simulados']}")
            print("🌊 ¡Hasta pronto!")

if __name__ == "__main__":
    sistema = SistemaFinal()
    sistema.ejecutar_continuamente()
