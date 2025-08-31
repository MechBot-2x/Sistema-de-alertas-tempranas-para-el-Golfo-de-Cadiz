#!/usr/bin/env python3
"""
📢 NOTIFICADOR AVANZADO - Sistema de alertas inteligentes
"""

import requests
from datetime import datetime

class NotificadorAvanzado:
    def __init__(self):
        self.telegram_token = "8478499112:AAGxqzYm4I-3Zyc9XCXIkE3mLOl8pXFOM00"
        self.telegram_chat_id = "8350588401"
        self.ultimas_alertas = []
    
    def enviar_alerta_oleaje(self, altura_oleaje):
        """Enviar alerta específica por oleaje"""
        if altura_oleaje > 2.5:
            nivel = "🔴 ALERTA ROJA"
            mensaje = "OLEAJE MUY PELIGROSO"
            recomendacion = "Evitar TODA actividad acuática"
        elif altura_oleaje > 2.0:
            nivel = "🟡 ALERTA AMARILLA" 
            mensaje = "OLEAJE PELIGROSO"
            recomendacion = "Precaución extrema en playas"
        else:
            nivel = "🟢 SITUACIÓN NORMAL"
            mensaje = "Condiciones normales"
            recomendacion = "Baño con precaución normal"
        
        texto = f"""
{nivel} - GOLFO DE CÁDIZ
🌊 Altura de ola: {altura_oleaje} m
📋 {mensaje}
💡 {recomendacion}
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📍 Datos: Copernicus Marine + AEMET
        """
        
        self.enviar_telegram(texto)
        return texto
    
    def enviar_telegram(self, mensaje):
        """Enviar mensaje a Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {
                'chat_id': self.telegram_chat_id,
                'text': mensaje,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, data=data, timeout=10)
            if response.json().get('ok'):
                print("✅ Alerta enviada por Telegram")
                return True
                
        except Exception as e:
            print(f"❌ Error enviando alerta: {e}")
        
        return False

# Uso inmediato
if __name__ == "__main__":
    notificador = NotificadorAvanzado()
    
    # Obtener datos actuales
    from scripts.datos.copernicus_simple import CopernicusSimpleClient
    client = CopernicusSimpleClient()
    datos = client.obtener_datos_golfo_cadiz()
    
    # Enviar alerta
    notificador.enviar_alerta_oleaje(datos['oleaje_altura'])
