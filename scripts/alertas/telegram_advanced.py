#!/usr/bin/env python3
"""
🤖 BOT TELEGRAM AVANZADO - Sistema profesional de alertas
"""

import requests
import logging
from datetime import datetime
from scripts.config.token_manager import token_manager

class TelegramAdvancedBot:
    """Bot avanzado de Telegram con formato profesional"""
    
    def __init__(self):
        self.bot_token = token_manager.get_token('telegram', 'bot_token')
        self.chat_id = token_manager.get_token('telegram', 'chat_id')
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        
        logging.info("🤖 Iniciando Bot Telegram Avanzado")
    
    def enviar_alerta_profesional(self, tipo, mensaje, datos=None):
        """Enviar alerta con formato profesional"""
        try:
            # Formato profesional de alerta
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            texto = f"🚨 **ALERTA OFICIAL SISTEMA GOLFO DE CÁDIZ**\n\n"
            texto += f"📋 **Tipo:** {tipo}\n"
            texto += f"⏰ **Hora:** {timestamp}\n"
            texto += f"📍 **Ubicación:** Golfo de Cádiz\n\n"
            texto += f"📝 **Descripción:**\n{mensaje}\n\n"
            
            if datos:
                texto += f"📊 **Datos Técnicos:**\n"
                for key, value in datos.items():
                    texto += f"• {key}: {value}\n"
            
            texto += f"\n🌊 **Sistema de Alertas Tempranas**\n"
            texto += f"🔗 **Estado:** ACTIVO\n"
            texto += f"📞 **Emergencias:** 112\n\n"
            texto += f"#Alerta #GolfoDeCadiz #Seguridad"
            
            payload = {
                'chat_id': self.chat_id,
                'text': texto,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': True
            }
            
            response = requests.post(f"{self.base_url}/sendMessage", json=payload, timeout=10)
            response.raise_for_status()
            
            logging.info("✅ Alerta profesional enviada por Telegram")
            return True
            
        except Exception as e:
            logging.error(f"❌ Error enviando alerta: {e}")
            return False
    
    def enviar_alerta_sismica(self, datos_sismo):
        """Alerta específica para sismos"""
        mensaje = f"🌍 Actividad sísmica detectada\nMagnitud: {datos_sismo['magnitud']}"
        
        datos_tecnicos = {
            "Magnitud": f"{datos_sismo['magnitud']}",
            "Ubicación": datos_sismo['lugar'],
            "Profundidad": f"{datos_sismo.get('profundidad', 'N/A')} km",
            "Coordenadas": f"{datos_sismo['latitud']}, {datos_sismo['longitud']}"
        }
        
        return self.enviar_alerta_profesional("SÍSMICA", mensaje, datos_tecnicos)
    
    def enviar_alerta_meteorologica(self, datos_meteo):
        """Alerta específica para condiciones meteorológicas"""
        mensaje = "🌤️ Condiciones meteorológicas extremas detectadas"
        
        datos_tecnicos = {
            "Viento": f"{datos_meteo.get('viento_velocidad', 'N/A')} km/h",
            "Temperatura": f"{datos_meteo.get('temperatura', 'N/A')}°C",
            "Presión": f"{datos_meteo.get('presion', 'N/A')} hPa",
            "Estación": datos_meteo.get('fuente', 'Simulación')
        }
        
        return self.enviar_alerta_profesional("METEOROLÓGICA", mensaje, datos_tecnicos)
    
    def enviar_prueba_sistema(self):
        """Enviar mensaje de prueba del sistema"""
        mensaje = "✅ **PRUEBA DEL SISTEMA DE ALERTAS**\n\n"
        mensaje += "El sistema de monitorización del Golfo de Cádiz está operativo y funcionando correctamente.\n\n"
        mensaje += "📊 **Estado:** SISTEMA ACTIVO\n"
        mensaje += "🌊 **Monitorización:** 24/7\n"
        mensaje += "🚨 **Alertas:** CONFIGURADAS\n\n"
        mensaje += "#Prueba #SistemaActivo #GolfoDeCadiz"
        
        payload = {
            'chat_id': self.chat_id,
            'text': mensaje,
            'parse_mode': 'Markdown'
        }
        
        try:
            response = requests.post(f"{self.base_url}/sendMessage", json=payload, timeout=10)
            response.raise_for_status()
            logging.info("✅ Prueba del sistema enviada por Telegram")
            return True
        except Exception as e:
            logging.error(f"❌ Error enviando prueba: {e}")
            return False

# Función de utilidad para pruebas rápidas
def enviar_alerta_rapida(mensaje):
    """Enviar alerta rápida desde línea de comandos"""
    bot = TelegramAdvancedBot()
    return bot.enviar_alerta_profesional("PRUEBA", mensaje)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        mensaje = " ".join(sys.argv[1:])
        enviar_alerta_rapida(mensaje)
    else:
        bot = TelegramAdvancedBot()
        bot.enviar_prueba_sistema()
