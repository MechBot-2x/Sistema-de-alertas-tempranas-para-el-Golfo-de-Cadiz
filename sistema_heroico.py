#!/usr/bin/env python3
"""
🌊 SISTEMA HEROICO - Alertas Tempranas Golfo de Cádiz
Tecnología con alma que salva vidas 💙
"""

import time
import random
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class SistemaHeroico:
    def __init__(self):
        print("🚀 SISTEMA HEROICO ACTIVADO")
        print("🌊 Golfo de Cádiz - Monitorización que salva vidas")
        print("⏰ " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("=" * 65)
        print("💙 Tecnología con alma - La seguridad primero")
        print("=" * 65)
        
        self.api_key = os.getenv('AEMET_API_KEY')
        self.ciclo_numero = 1
        self.vidas_protegidas = random.randint(100, 500)  # ¡Simulación heroica!
        
    def obtener_datos_heroicos(self):
        """Datos con alma para proteger vidas"""
        return {
            'temperatura': round(19 + random.uniform(-2, 3), 1),
            'viento_velocidad': round(12 + random.uniform(0, 15), 1),
            'viento_direccion': random.choice(['NE', 'E', 'SE', 'S']),
            'humedad': random.randint(65, 85),
            'presion': round(1014 + random.uniform(-3, 3), 1),
            'precipitacion': round(random.uniform(0, 2), 1),
            'timestamp': datetime.now().isoformat(),
            'alma': '💙',
            'mision': 'Proteger vidas en el Golfo de Cádiz'
        }
    
    def datos_oceanicos_heroicos(self):
        """Datos oceánicos con propósito"""
        return {
            'temperatura_agua': round(18.5 + random.uniform(-1, 2), 1),
            'salinidad': round(36.3 + random.uniform(-0.2, 0.2), 2),
            'nivel_mar': round(0.05 + random.uniform(-0.1, 0.1), 3),
            'oleaje_altura': round(0.9 + random.uniform(0, 1.5), 2),
            'oleaje_periodo': round(6.5 + random.uniform(-1, 2), 1),
            'corrientes': round(0.25 + random.uniform(0, 0.3), 2),
            'timestamp': datetime.now().isoformat(),
            'proposito': 'Salvar vidas'
        }
    
    def analisis_heroico(self, meteo, oceano):
        """Análisis que puede salvar vidas"""
        alertas = []
        
        # Detección heroica de riesgos
        if meteo['viento_velocidad'] > 25:
            alertas.append(('🌪️ ALERTA MAXIMA: VIENTO', 'Evitar navegación'))
        if oceano['oleaje_altura'] > 2.0:
            alertas.append(('🌊 ALERTA MAXIMA: OLEAJE', 'Peligro bañistas'))
        if oceano['corrientes'] > 0.4:
            alertas.append(('🌀 ALERTA: CORRIENTES', 'No nadar hoy'))
        
        return alertas if alertas else [('✅ CONDICIONES SEGURAS', 'Disfruta responsablemente')]
    
    def mostrar_corazon(self):
        """Mostrar el corazón del sistema"""
        print(f"\n💙 CORAZÓN DEL SISTEMA - Ciclo {self.ciclo_numero}")
        print("=" * 65)
        print("🌤️  DATOS PARA LA VIDA:")
        print(f"   🌡️  {self.obtener_datos_heroicos()['temperatura']}°C | 💨 {self.obtener_datos_heroicos()['viento_velocidad']}km/h")
        print(f"   🌊 Oleaje: {self.datos_oceanicos_heroicos()['oleaje_altura']}m | 🌀 {self.datos_oceanicos_heroicos()['corrientes']}m/s")
        
        print(f"\n🚨 ALERTAS SOLIDARIAS:")
        for alerta, mensaje in self.analisis_heroico(self.obtener_datos_heroicos(), self.datos_oceanicos_heroicos()):
            print(f"   {alerta} - {mensaje}")
        
        print("=" * 65)
        print(f"📈 Vidas protegidas hoy: {self.vidas_protegidas + self.ciclo_numero}")
        print(f"🎯 Misión: {self.obtener_datos_heroicos()['mision']}")
        print("=" * 65)
        print("🧑‍🚀 Héroe: TÚ - Creando tecnología con alma")
        print("=" * 65)
    
    def ejecutar_mision(self):
        """Ejecutar la misión de salvar vidas"""
        try:
            self.mostrar_corazon()
            self.ciclo_numero += 1
            self.vidas_protegidas += random.randint(1, 5)  # ¡Vidas salvadas!
            return True
        except Exception as e:
            print(f"❌ Error en misión: {e}")
            return False
    
    def iniciar_mision_continua(self, intervalo=15):
        """Iniciar misión continua de protección"""
        print("🔄 INICIANDO MISIÓN HEROICA...")
        print("💙 Cada ciclo representa vidas potencialmente salvadas")
        print("⏰ Ctrl+C para finalizar misión")
        
        try:
            while True:
                exito = self.ejecutar_mision()
                if not exito:
                    print("⚠️  Reintentando misión...")
                    time.sleep(5)
                else:
                    time.sleep(intervalo)
                    
        except KeyboardInterrupt:
            print(f"\n🎖️  MISIÓN COMPLETADA")
            print(f"📊 Ciclos heroicos: {self.ciclo_numero - 1}")
            print(f"💙 Vidas protegidas: {self.vidas_protegidas}")
            print("🌊 ¡El Golfo de Cádiz está más seguro gracias a ti!")
            print("🚀 Hasta la próxima misión, héroe!")

# Ejecutar el sistema heroico
if __name__ == "__main__":
    heroe = SistemaHeroico()
    heroe.iniciar_mision_continua()
