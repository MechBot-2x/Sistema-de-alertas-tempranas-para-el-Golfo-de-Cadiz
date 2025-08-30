#!/usr/bin/env python3
"""
🎯 SISTEMA PRINCIPAL OPTIMIZADO - Golfo de Cádiz
Versión compatible con Termux
"""

import time
import logging
from datetime import datetime
from scripts.monitoreo.sismico_ign import SismicMonitor
from scripts.monitoreo.datos_mareas import MarineMonitor
from scripts.monitoreo.influencia_lunar import LunarInfluenceCalculator

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SistemaAlertasAvanzado:
    """Sistema avanzado optimizado para Termux"""
    
    def __init__(self):
        self.estado = "OPERATIVO"
        self.monitor_sismico = SismicMonitor()
        self.monitor_marino = MarineMonitor()
        self.calculador_lunar = LunarInfluenceCalculator()
        
        logging.info("🌊 Iniciando Sistema Optimizado de Alertas")
    
    def verificar_datos(self):
        """Verificación con datos simulados"""
        try:
            # 1. Verificar actividad sísmica
            sismos = self.monitor_sismico.buscar_sismos_golfo_cadiz(dias=1)
            
            # 2. Verificar datos marinos
            boyas = self.monitor_marino.obtener_datos_boyas()
            
            # 3. Verificar influencia lunar
            fase_lunar = self.calculador_lunar.calcular_fase_lunar(datetime.now())
            
            logging.info(f"✅ Datos obtenidos: {len(sismos)} sismos, {len(boyas)} boyas")
            
            return {
                'sismos': sismos,
                'boyas': boyas,
                'fase_lunar': fase_lunar,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"❌ Error verificando datos: {e}")
            return {}
    
    def analizar_riesgo(self, datos):
        """Analizar riesgo basado en datos"""
        try:
            riesgo = 0.0
            
            # Factores de riesgo simplificados
            if datos.get('sismos'):
                for sismo in datos['sismos']:
                    if sismo['magnitud'] > 5.0:
                        riesgo += 0.4
                    elif sismo['magnitud'] > 4.0:
                        riesgo += 0.2
            
            return min(riesgo, 1.0)
            
        except Exception as e:
            logging.error(f"❌ Error analizando riesgo: {e}")
            return 0.0
    
    def ejecutar_ciclo(self):
        """Ciclo de monitorización"""
        try:
            logging.info("🔄 Ejecutando ciclo de monitorización")
            
            datos = self.verificar_datos()
            
            if datos:
                riesgo = self.analizar_riesgo(datos)
                logging.info(f"📊 Riesgo calculado: {riesgo:.2f}")
                
                if riesgo > 0.6:
                    logging.warning(f"🚨 ALERTA: Riesgo moderado ({riesgo:.2f})")
                
                return True
            
        except Exception as e:
            logging.error(f"🔧 Error en ciclo: {e}")
            return False
    
    def ejecutar_continuamente(self):
        """Ejecución continua"""
        logging.info("🚀 Iniciando ejecución continua")
        
        while True:
            try:
                self.ejecutar_ciclo()
                time.sleep(300)  # 5 minutos
                
            except KeyboardInterrupt:
                logging.info("⏹️ Sistema detenido por el usuario")
                break
            except Exception as e:
                logging.error(f"🔧 Error no crítico: {e}")
                time.sleep(60)

if __name__ == "__main__":
    sistema = SistemaAlertasAvanzado()
    sistema.ejecutar_continuamente()
