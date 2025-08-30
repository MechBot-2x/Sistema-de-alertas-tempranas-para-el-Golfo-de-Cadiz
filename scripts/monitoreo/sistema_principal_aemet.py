#!/usr/bin/env python3
"""
🎯 SISTEMA PRINCIPAL CON AEMET OPENDATA - Conexión profesional
"""

import time
import logging
from datetime import datetime
from scripts.datos.aemet_client import AEMETGolfoCadiz
from scripts.monitoreo.sismico_cosmico import SismicMonitorCosmico
from scripts.monitoreo.boyas_avanzadas_2025 import BoyasAvanzadas2025

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/sistema_aemet.log'),
        logging.StreamHandler()
    ]
)

class SistemaAEMETCompleto:
    """Sistema completo con integración AEMET OpenData"""
    
    def __init__(self):
        self.estado = "INICIANDO"
        self.aemet_client = AEMETGolfoCadiz()
        self.monitor_sismico = SismicMonitorCosmico()
        self.monitor_boyas = BoyasAvanzadas2025()
        
        logging.info("🌤️ INICIANDO SISTEMA AEMET OPENDATA")
        
        # Verificar conexión AEMET
        if self._verificar_aemet():
            self.estado = "OPERATIVO"
        else:
            self.estado = "LIMITADO"
            logging.warning("⚠️ Sistema operando en modo limitado (sin AEMET)")
    
    def _verificar_aemet(self):
        """Verificar conexión con AEMET"""
        try:
            # Usar el cliente básico para verificación
            from scripts.datos.aemet_client import AEMETClient
            client = AEMETClient()
            return client.verificar_conexion()
        except Exception as e:
            logging.error(f"❌ Error verificando AEMET: {e}")
            return False
    
    def obtener_datos_meteorologicos(self):
        """Obtener datos meteorológicos completos"""
        try:
            datos = self.aemet_client.obtener_meteo_golfo_cadiz()
            
            if datos:
                logging.info(f"🌤️ Datos AEMET obtenidos: {len(datos)} elementos")
                return datos
            else:
                logging.warning("⚠️ No se pudieron obtener datos AEMET")
                return self._datos_meteo_simulados()
                
        except Exception as e:
            logging.error(f"❌ Error obteniendo datos meteorológicos: {e}")
            return self._datos_meteo_simulados()
    
    def _datos_meteo_simulados(self):
        """Datos simulados como fallback"""
        from datetime import datetime
        return {
            'timestamp': datetime.now().isoformat(),
            'estado': 'SIMULADO',
            'temperatura': 22.5,
            'viento_velocidad': 15.3,
            'viento_direccion': 270,
            'presion': 1013.2,
            'humedad': 65,
            'fuente': 'SISTEMA_RESERVA'
        }
    
    def ejecutar_ciclo_completo(self):
        """Ejecutar ciclo completo de monitorización"""
        try:
            logging.info("🔄 EJECUTANDO CICLO COMPLETO AEMET")
            
            # 1. Datos meteorológicos (AEMET)
            datos_meteo = self.obtener_datos_meteorologicos()
            
            # 2. Datos sísmicos
            sismos = self.monitor_sismico.buscar_sismos_golfo_cadiz_cosmicos(dias=1)
            
            # 3. Datos de boyas
            boyas = self.monitor_boyas.obtener_datos_boyas_cosmicas()
            
            # 4. Análisis integrado
            analisis = self._analizar_datos_integrados(datos_meteo, sismos, boyas)
            
            # 5. Generar alertas si es necesario
            self._generar_alertas_integradas(analisis)
            
            logging.info("✅ CICLO AEMET COMPLETADO")
            return True
            
        except Exception as e:
            logging.error(f"💥 Error en ciclo AEMET: {e}")
            return False
    
    def _analizar_datos_integrados(self, meteo, sismos, boyas):
        """Analizar datos integrados de todas las fuentes"""
        riesgo = 0.0
        alertas = []
        
        # Análisis meteorológico
        if meteo.get('viento_velocidad', 0) > 50:  # km/h
            riesgo += 0.3
            alertas.append("🌬️ Viento muy fuerte")
        
        if meteo.get('temperatura', 0) > 35:
            riesgo += 0.1
            alertas.append("🌡️ Temperatura muy alta")
        
        # Análisis sísmico
        for sismo in sismos:
            if sismo['magnitud'] > 4.0:
                riesgo += 0.4
                alertas.append(f"🌍 Sismo M{sismo['magnitud']}")
        
        # Análisis de boyas
        for boya in boyas:
            if boya.get('altura_ola', 0) > 3.0:
                riesgo += 0.2
                alertas.append(f"🌊 Ola alta: {boya['altura_ola']}m")
        
        return {
            'riesgo_total': min(riesgo, 1.0),
            'alertas': alertas,
            'timestamp': datetime.now().isoformat(),
            'total_datos': len(meteo) + len(sismos) + len(boyas)
        }
    
    def _generar_alertas_integradas(self, analisis):
        """Generar alertas basadas en análisis integrado"""
        if analisis['riesgo_total'] > 0.6:
            mensaje = f"🚨 ALERTA INTEGRADA - Riesgo: {analisis['riesgo_total']:.2f}"
            logging.warning(mensaje)
            
            # Aquí integraríamos con Telegram
            # self._enviar_alerta_telegram(mensaje)
        
        for alerta in analisis['alertas']:
            logging.warning(f"⚠️ {alerta}")
    
    def ejecutar_continuamente(self):
        """Ejecución continua del sistema"""
        logging.info("🚀 INICIANDO EJECUCIÓN CONTINUA AEMET")
        
        ciclo = 0
        while True:
            try:
                ciclo += 1
                logging.info(f"🔁 CICLO AEMET #{ciclo}")
                
                self.ejecutar_ciclo_completo()
                time.sleep(1800)  # 30 minutos entre ciclos
                
            except KeyboardInterrupt:
                logging.info("⏹️ SISTEMA AEMET DETENIDO POR EL USUARIO")
                break
            except Exception as e:
                logging.error(f"🔧 Error no crítico: {e}")
                time.sleep(300)  # Reintentar en 5 minutos

if __name__ == "__main__":
    # Ejecutar debug primero
    from scripts.datos.aemet_client import debug_aemet
    debug_aemet()
    
    # Iniciar sistema completo
    sistema = SistemaAEMETCompleto()
    sistema.ejecutar_continuamente()
