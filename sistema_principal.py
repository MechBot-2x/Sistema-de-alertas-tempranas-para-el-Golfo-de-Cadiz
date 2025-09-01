#!/usr/bin/env python3
"""
🎯 SISTEMA PRINCIPAL SIMPLIFICADO - Monitorización Golfo de Cádiz
"""

import time
import logging
from datetime import datetime
from scripts.datos.copernicus_simple import CopernicusSimpleClient

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SistemaPrincipal:
    """Sistema principal de monitorización"""
    
    def __init__(self):
        self.client = CopernicusSimpleClient()
        self.estado = "INICIANDO"
        
        logging.info("🚀 INICIANDO SISTEMA PRINCIPAL")
        logging.info("🌊 Monitorización Golfo de Cádiz")
    
    def ejecutar_ciclo(self):
        """Ejecutar un ciclo de monitorización"""
        try:
            logging.info("🔄 EJECUTANDO CICLO")
            
            # Obtener datos
            reporte = self.client.generar_reporte()
            
            # Mostrar información
            self._mostrar_estado(reporte)
            
            # Verificar alertas
            self._verificar_alertas(reporte)
            
            logging.info("✅ CICLO COMPLETADO")
            return True
            
        except Exception as e:
            logging.error(f"💥 Error en ciclo: {e}")
            return False
    
    def _mostrar_estado(self, reporte):
        """Mostrar estado del sistema"""
        print("\n" + "=" * 60)
        print("🌊 SISTEMA DE MONITORIZACIÓN - Golfo de Cádiz")
        print("=" * 60)
        
        print(f"🌡️ Temp: {reporte['temperatura_superficie']}°C")
        print(f"🧂 Sal: {reporte['salinidad']} PSU")
        print(f"📈 Nivel: {reporte['nivel_mar']} m")
        print(f"🌀 Corriente: {reporte['corriente_velocidad']} m/s")
        print(f"🌊 Oleaje: {reporte['oleaje_altura']} m")
        
        print(f"📡 Estado: {reporte['conexion']['estado']}")
        print(f"🎯 Riesgo: {reporte['analisis']['riesgo_total']:.1%}")
        
        print("=" * 60)
    
    def _verificar_alertas(self, reporte):
        """Verificar y manejar alertas"""
        if reporte['analisis']['alertas']:
            for alerta in reporte['analisis']['alertas']:
                logging.warning(f"⚠️ {alerta}")
            
            for recomendacion in reporte['analisis']['recomendaciones']:
                logging.info(f"💡 {recomendacion}")
        else:
            logging.info("✅ Sin alertas - Condiciones normales")
    
    def ejecutar_continuamente(self, intervalo_minutos=5):
        """Ejecutar continuamente"""
        logging.info(f"🔁 INICIANDO EJECUCIÓN CONTINUA ({intervalo_minutos} min)")
        
        ciclo = 0
        try:
            while True:
                ciclo += 1
                print(f"\n🔄 CICLO #{ciclo} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                self.ejecutar_ciclo()
                
                # Esperar para el próximo ciclo
                time.sleep(intervalo_minutos * 60)
                
        except KeyboardInterrupt:
            print("\n⏹️ SISTEMA DETENIDO POR EL USUARIO")
            logging.info("Sistema detenido manualmente")

if __name__ == "__main__":
    sistema = SistemaPrincipal()
    sistema.ejecutar_continuamente(intervalo_minutos=2)
