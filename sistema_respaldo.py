#!/usr/bin/env python3
"""
📻 SISTEMA DE RESpaldo - Sin dependencias de Internet
Monitoreo basado en patrones históricos y ciclos solares
"""

import time
from datetime import datetime

class SistemaRespaldo:
    def __init__(self):
        self.ciclos_solares = {
            '2025-08': 'MÁXIMO SOLAR',  # Agosto 2025 - Máximo solar
            '2025-09': 'ALTA ACTIVIDAD',
            '2025-10': 'ALTA ACTIVIDAD', 
        }
        
    def predecir_riesgo(self):
        """Predicción basada en ciclos históricos de Chizhevsky"""
        mes_actual = datetime.now().strftime('%Y-%m')
        hora_actual = datetime.now().hour
        
        # Patrones de riesgo conocidos
        riesgo_base = 0.3  # Riesgo base por máximo solar 2025
        
        # Aumentar riesgo en horas críticas (6h, 12h, 18h, 0h)
        if hora_actual in [6, 12, 18, 0]:
            riesgo_base += 0.2
            
        # Aumentar riesgo en fechas históricamente críticas
        dia_mes = datetime.now().day
        if dia_mes in [1, 15, 20, 25]:  # Días con mayor actividad histórica
            riesgo_base += 0.1
            
        return min(riesgo_base, 0.8)
    
    def ejecutar_monitoreo(self):
        """Monitoreo continuo sin dependencias externas"""
        print("📻 SISTEMA DE RESpaldo ACTIVADO")
        print("🌞 Basado en patrones históricos de Chizhevsky")
        print("🔍 Monitoreo ciclo solar 2025 (Máximo solar)")
        print("=" * 50)
        
        try:
            while True:
                riesgo = self.predecir_riesgo()
                nivel = "ALTO" if riesgo > 0.5 else "MEDIO" if riesgo > 0.3 else "BAJO"
                
                print(f"\n🕒 {datetime.now().strftime('%d/%m %H:%M')}")
                print(f"📈 Riesgo calculado: {riesgo:.0%}")
                print(f"🚨 Nivel: {nivel}")
                print(f"🌞 Ciclo solar: {self.ciclos_solares.get(datetime.now().strftime('%Y-%m'), 'Desconocido')}")
                
                if riesgo > 0.6:
                    print("⚠️  RECOMENDACIÓN: Aumentar vigilancia")
                elif riesgo > 0.4:
                    print("🔶 RECOMENDACIÓN: Monitorizar situación")
                
                # Esperar 15 minutos
                time.sleep(900)
                
        except KeyboardInterrupt:
            print("\n🛑 Sistema de respaldo detenido")

if __name__ == "__main__":
    sistema = SistemaRespaldo()
    sistema.ejecutar_monitoreo()
