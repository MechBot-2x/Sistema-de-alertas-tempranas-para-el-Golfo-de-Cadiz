#!/usr/bin/env python3
"""
🎯 SISTEMA PRINCIPAL CON ALERTAS TELEGRAM - Evolución completa
"""

import time
import logging
from datetime import datetime
from scripts.monitoreo.sistema_principal_mejorado import SistemaResiliente
from scripts.alertas.telegram_advanced import TelegramAdvancedBot

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SistemaConAlertas(SistemaResiliente):
    """Sistema evolucionado con alertas por Telegram"""
    
    def __init__(self):
        super().__init__()
        self.bot_telegram = TelegramAdvancedBot()
        self.ultima_alerta_enviada = None
        
        logging.info("🤖 SISTEMA CON ALERTAS TELEGRAM INICIADO")
        
        # Enviar mensaje de inicio
        self.bot_telegram.enviar_prueba_sistema()
    
    def _generar_alertas_integradas(self, analisis):
        """Generar alertas integradas con Telegram"""
        alertas = analisis.get('alertas', [])
        
        if alertas:
            for alerta in alertas:
                logging.warning(f"⚠️ {alerta}")
                
                # Enviar alerta por Telegram si es importante
                if any(keyword in alerta for keyword in ['ALERTA', 'Sismo', 'Ola alta', 'Viento fuerte']):
                    self.bot_telegram.enviar_alerta_profesional(
                        "AUTOMÁTICA", 
                        alerta,
                        {
                            "Riesgo Total": f"{analisis['riesgo_total']:.2f}",
                            "Tipo Alerta": analisis['nivel_alerta'],
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                    )
    
    def ejecutar_ciclo_completo(self):
        """Ciclo completo con alertas"""
        try:
            resultado = super().ejecutar_ciclo_completo()
            
            # Enviar resumen cada 6 horas
            hora_actual = datetime.now().hour
            if hora_actual % 6 == 0 and datetime.now().minute < 5:
                self._enviar_resumen_diario()
            
            return resultado
            
        except Exception as e:
            logging.error(f"💥 Error en ciclo con alertas: {e}")
            return False
    
    def _enviar_resumen_diario(self):
        """Enviar resumen diario por Telegram"""
        try:
            from scripts.datos.aemet_client import MonitorAEMETGolfoCadiz
            from scripts.monitoreo.sismico_cosmico import SismicMonitorCosmico
            
            monitor = MonitorAEMETGolfoCadiz()
            sismico = SismicMonitorCosmico()
            
            datos_meteo = monitor.obtener_datos_completos_golfo()
            sismos = sismico.buscar_sismos_golfo_cadiz_cosmicos(dias=1)
            
            mensaje = "📊 **RESUMEN DIARIO SISTEMA**\n\n"
            mensaje += f"🌤️ Estaciones meteorológicas: {len(datos_meteo.get('estaciones', {}))}\n"
            mensaje += f"🌍 Sismos últimos 24h: {len(sismos)}\n"
            mensaje += f"🚨 Nivel alerta actual: {datos_meteo.get('estado_conexion', 'SIMULACIÓN')}\n\n"
            mensaje += "✅ Sistema operativo y monitorizando\n"
            mensaje += "🌊 Golfo de Cádiz - Seguridad 24/7"
            
            self.bot_telegram.enviar_alerta_profesional("REPORTE DIARIO", mensaje)
            
        except Exception as e:
            logging.error(f"❌ Error enviando resumen: {e}")

def ejecutar_sistema_completo():
    """Ejecutar el sistema evolucionado"""
    print("=" * 60)
    print("🚀 SISTEMA EVOLUCIONADO CON ALERTAS TELEGRAM")
    print("=" * 60)
    
    sistema = SistemaConAlertas()
    
    try:
        sistema.ejecutar_continuamente()
    except KeyboardInterrupt:
        print("\n⏹️ Sistema detenido por el usuario")
        # Enviar mensaje de cierre
        sistema.bot_telegram.enviar_alerta_profesional(
            "SISTEMA", 
            "Sistema de monitorización detenido manualmente. Seguridad reactivada en próximo inicio."
        )

if __name__ == "__main__":
    ejecutar_sistema_completo()
