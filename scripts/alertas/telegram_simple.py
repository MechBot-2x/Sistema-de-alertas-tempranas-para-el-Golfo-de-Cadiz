#!/usr/bin/env python3
"""
📢 SISTEMA DE NOTIFICACIONES TELEGRAM - Simple y Confiable
"""

import requests
import logging
import os
from dotenv import load_dotenv

# Cargar configuración
load_dotenv()

class TelegramNotifier:
    """Notificador simple de Telegram"""
    
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        
    def enviar_mensaje(self, mensaje):
        """Enviar mensaje simple"""
        try:
            if not self.token or not self.chat_id:
                logging.warning("⚠️ Tokens de Telegram no configurados")
                return False
            
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': mensaje,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logging.info("✅ Mensaje enviado a Telegram")
                return True
            else:
                logging.error(f"❌ Error Telegram: {response.text}")
                return False
                
        except Exception as e:
            logging.error(f"❌ Error enviando mensaje: {e}")
            return False

# Función simple para uso rápido
def enviar_alerta(mensaje):
    """Función simple para enviar alertas"""
    notifier = TelegramNotifier()
    return notifier.enviar_mensaje(mensaje)
