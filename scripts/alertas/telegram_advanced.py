#!/usr/bin/env python3
"""
📢 NOTIFICADOR AVANZADO - Sistema de alertas Telegram
"""

import requests
from datetime import datetime

class NotificadorAvanzado:
    def __init__(self):
        self.telegram_token = "8478499112:AAGxqzYm4I-3Zyc9XCXIkE3mLOl8pXFOM00"
        self.telegram_chat_id = "8350588401"
        
    def enviar_telegram(self, mensaje):
        """Enviar mensaje a Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {
                'chat_id': self.telegram_chat_id,
                'text': mensaje,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data, timeout=10)
            if response.json().get('ok'):
                print("✅ Alerta enviada por Telegram")
                return True
                
        except Exception as e:
            print(f"❌ Error enviando Telegram: {e}")
        
        return False

# Prueba rápida
if __name__ == "__main__":
    notificador = NotificadorAvanzado()
    notificador.enviar_telegram("🤖 Bot Telegram funcionando correctamente")
