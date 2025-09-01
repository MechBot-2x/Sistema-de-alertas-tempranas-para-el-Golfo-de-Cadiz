#!/usr/bin/env python3
"""
🌊⚡ SISTEMA COMPLETO INTEGRADO - Meteorología + Oceanografía + Sismología
"""

import time
import threading
from datetime import datetime
from sistema_completo_telegram import SistemaCompleto
from scripts.datos.sismografo import MonitorSismico

class SistemaIntegrado(SistemaCompleto):
    def __init__(self):
        super().__init__()
        self.monitor_sismico = MonitorSismico()
        self.alertas_sismicas = []
        
        print("🌋⚡ SISTEMA INTEGRADO ACTIVADO")
        print("📊 Meteorología + Oceanografía + Sismología")
        print("📍 Golfo de Cádiz - Protección Total")
    
    def iniciar_monitoreo_sismico(self):
        """Iniciar monitoreo sísmico en segundo plano"""
        def monitorear():
            while True:
                try:
                    terremotos = self.monitor_sismico.obtener_datos_usgs()
                    alertas = self.monitor_sismico.generar_alerta_sismica(terremotos)
                    
                    if alertas:
                        self.alertas_sismicas = alertas
                        self.enviar_alertas_sismicas(alertas)
                    
                    time.sleep(300)  # 5 minutos entre chequeos
                    
                except Exception as e:
                    print(f"❌ Error monitoreo sísmico: {e}")
                    time.sleep(60)
        
        # Iniciar en segundo plano
        thread = threading.Thread(target=monitorear, daemon=True)
        thread.start()
        print("✅ Monitoreo sísmico iniciado en segundo plano")
    
    def enviar_alertas_sismicas(self, alertas):
        """Enviar alertas sísmicas por Telegram"""
        for alerta in alertas:
            mensaje = f"🌋 {alerta['nivel']} SÍSMICA\n"
            mensaje += f"{alerta['mensaje']}\n"
            mensaje += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            mensaje += f"🌊 Riesgo tsunami: {alerta['riesgo_tsunami']:.1%}\n"
            mensaje += f"📍 {alerta['terremoto']['lugar']}"
            
            self.enviar_telegram(mensaje)
    
    def mostrar_dashboard_integrado(self, datos_meteo, datos_oceano, alertas, fuente):
        """Dashboard integrado con información sísmica"""
        super().mostrar_dashboard_oficial(datos_meteo, datos_oceano, alertas, fuente)
        
        # Mostrar información sísmica si hay alertas
        if self.alertas_sismicas:
            print("\n" + "=" * 60)
            print("🌋 ACTIVIDAD SÍSMICA RECIENTE:")
            for alerta in self.alertas_sismicas[-3:]:  # Últimas 3 alertas
                print(f"   {alerta['nivel']}: {alerta['mensaje']}")
            print("=" * 60)
    
    def iniciar_sistema_completo(self):
        """Iniciar sistema completo integrado"""
        print("🔄 INICIANDO SISTEMA INTEGRADO COMPLETO")
        print("⏰ Monitorizando: Meteorología, Oceanografía, Sismología")
        
        # Iniciar monitoreo sísmico
        self.iniciar_monitoreo_sismico()
        
        # Mensaje de inicio
        self.enviar_telegram(
            "🌋⚡ <b>SISTEMA INTEGRADO ACTIVADO</b>\n"
            "📊 Meteorología + Oceanografía + Sismología\n"
            "📍 Golfo de Cádiz - Protección Total\n"
            f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        # Ciclo principal
        ciclo = 0
        try:
            while True:
                ciclo += 1
                print(f"\n🔁 CICLO INTEGRADO {ciclo}")
                
                # Ejecutar ciclo meteorológico/oceanográfico
                self.ejecutar_ciclo_completo()
                
                time.sleep(30)  # 30 segundos entre ciclos
                
        except KeyboardInterrupt:
            print("\n🛑 SISTEMA INTEGRADO DETENIDO")
            self.enviar_telegram(
                "🛑 <b>SISTEMA INTEGRADO DETENIDO</b>\n"
                f"📊 Ciclos completados: {ciclo}\n"
                f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

if __name__ == "__main__":
    sistema = SistemaIntegrado()
    sistema.iniciar_sistema_completo()
