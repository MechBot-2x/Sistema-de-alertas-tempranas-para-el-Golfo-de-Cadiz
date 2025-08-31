#!/usr/bin/env python3
"""
🎯 SISTEMA PRINCIPAL AVANZADO - Con MyOcean Pro
"""

import time
import logging
from datetime import datetime
from scripts.datos.myocean_pro_client import MyOceanProClient
from scripts.alertas.telegram_advanced import NotificadorAvanzado

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SistemaAvanzado:
    """Sistema avanzado con MyOcean Pro"""
    
    def __init__(self):
        self.client = MyOceanProClient()
        self.notificador = NotificadorAvanzado()
        self.estado = "INICIANDO"
        
        logging.info("🚀 INICIANDO SISTEMA AVANZADO CON MYOCEAN PRO")
    
    def ejecutar_ciclo_avanzado(self):
        """Ejecutar ciclo avanzado de monitorización"""
        try:
            logging.info("🔄 EJECUTANDO CICLO AVANZADO...")
            
            # Obtener datos avanzados
            reporte = self.client.generar_reporte_avanzado()
            
            # Mostrar información
            self._mostrar_dashboard_avanzado(reporte)
            
            # Enviar alertas si es necesario
            if reporte['analisis']['alertas']:
                self._enviar_alertas_avanzadas(reporte)
            
            logging.info("✅ CICLO AVANZADO COMPLETADO")
            return True
            
        except Exception as e:
            logging.error(f"💥 Error en ciclo avanzado: {e}")
            return False
    
    def _mostrar_dashboard_avanzado(self, reporte):
        """Mostrar dashboard avanzado"""
        print("\n" + "=" * 80)
        print("🌊 DASHBOARD AVANZADO MYOCEAN PRO - Golfo de Cádiz")
        print("=" * 80)
        
        print(f"🌡️  Temperatura: {reporte['temperatura_superficie']}°C")
        print(f"🧂 Salinidad: {reporte['salinidad']} PSU")
        print(f"📈 Nivel mar: {reporte['nivel_mar']} m")
        print(f"🌀 Corrientes: {reporte['corriente_velocidad']} m/s → {reporte['corriente_direccion']}°")
        
        print(f"\n🎯 Calidad: {reporte['calidad']}")
        print(f"📡 Fuente: {reporte['fuente']}")
        print(f"📦 Producto: {reporte['producto']}")
        
        print(f"\n🚨 Estado: {reporte['analisis']['estado_general']}")
        print(f"📊 Riesgo: {reporte['analisis']['riesgo_total']:.1%}")
        
        if reporte['analisis']['alertas']:
            print(f"\n⚠️  Alertas activas: {len(reporte['analisis']['alertas'])}")
            for alerta in reporte['analisis']['alertas']:
                print(f"   • {alerta}")
        
        print("=" * 80)
    
    def _enviar_alertas_avanzadas(self, reporte):
        """Enviar alertas avanzadas"""
        mensaje = f"🚨 ALERTA MYOCEAN PRO - Golfo de Cádiz\n"
        mensaje += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        mensaje += f"📊 Riesgo: {reporte['analisis']['riesgo_total']:.1%}\n"
        
        for alerta in reporte['analisis']['alertas']:
            mensaje += f"⚠️ {alerta}\n"
        
        for recomendacion in reporte['recomendaciones']:
            mensaje += f"💡 {recomendacion}\n"
        
        # Enviar por Telegram
        if self.notificador.enviar_telegram(mensaje):
            logging.info("✅ Alerta avanzada enviada por Telegram")
    
    def ejecutar_continuamente(self, intervalo_minutos=10):
        """Ejecutar continuamente"""
        logging.info(f"🔁 INICIANDO EJECUCIÓN CONTINUA ({intervalo_minutos} min)")
        
        ciclo = 0
        try:
            while True:
                ciclo += 1
                print(f"\n🔄 CICLO AVANZADO #{ciclo} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                self.ejecutar_ciclo_avanzado()
                time.sleep(intervalo_minutos * 60)
                
        except KeyboardInterrupt:
            print("\n⏹️ SISTEMA AVANZADO DETENIDO")
            logging.info("Sistema avanzado detenido manualmente")

if __name__ == "__main__":
    sistema = SistemaAvanzado()
    sistema.ejecutar_continuamente(intervalo_minutos=5)
