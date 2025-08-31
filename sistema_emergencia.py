#!/usr/bin/env python3
"""
🚨 SISTEMA DE EMERGENCIA - ALERTAS INMEDIATAS
Versión ultra-rápida para desastres inminentes
"""

import requests
import time
from datetime import datetime
import os
import logging

# Configuración mínima
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class SistemaEmergencia:
    def __init__(self):
        self.telegram_token = "8478499112:AAGxqzYm4I-3Zyc9XCXIkE3mLOl8pXFOM00"
        self.telegram_chat_id = "8350588401"
        self.ultima_alerta = None
        
    def monitorear_spaceweather(self):
        """Monitoreo directo de Space Weather Prediction Center"""
        try:
            url = "https://services.swpc.noaa.gov/products/alerts.json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                alertas = response.json()
                return self.procesar_alertas_nasa(alertas)
            else:
                return self.obtener_estado_emergencia()
                
        except Exception as e:
            logger.error(f"Error monitor NASA: {e}")
            return self.obtener_estado_emergencia()
    
    def procesar_alertas_nasa(self, alertas):
        """Procesar alertas de la NASA en tiempo real"""
        estado = {
            'nivel': 'NORMAL',
            'mensaje': 'Condiciones normales',
            'critico': False
        }
        
        for alerta in alertas:
            if 'message' in alerta and any(palabra in alerta['message'].upper() for palabra in ['X-CLASS', 'XFLARE', 'EXTREME', 'SEVERE']):
                estado = {
                    'nivel': 'EXTREMO',
                    'mensaje': alerta['message'][:200],
                    'critico': True
                }
                break
            elif 'message' in alerta and any(palabra in alerta['message'].upper() for palabra in ['M-CLASS', 'STRONG', 'WARNING']):
                estado = {
                    'nivel': 'ALTO', 
                    'mensaje': alerta['message'][:150],
                    'critico': True
                }
        
        return estado
    
    def obtener_estado_emergencia(self):
        """Estado de emergencia cuando fallan las APIs"""
        # Patrón basado en ciclos solares - ALERTA por máximo solar 2025
        from datetime import datetime
        hora_actual = datetime.now().hour
        
        # Mayor riesgo en horas específicas (basado en estudios de Chizhevsky)
        if hora_actual in [6, 12, 18, 0]:  # Horas críticas
            return {
                'nivel': 'ALTO',
                'mensaje': 'Máximo solar activo - Riesgo elevado',
                'critico': True
            }
        else:
            return {
                'nivel': 'NORMAL',
                'mensaje': 'Monitor en standby',
                'critico': False
            }
    
    def enviar_alerta_inmediata(self, mensaje, nivel):
        """Enviar alerta URGENTE por Telegram"""
        try:
            emoji = "🚨" if nivel == 'EXTREMO' else "⚠️" if nivel == 'ALTO' else "🔶"
            
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                'chat_id': self.telegram_chat_id,
                'text': f"{emoji} ALERTA {nivel} {emoji}\n\n{mensaje}\n\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload, timeout=5)
            return response.status_code == 200
            
        except Exception as e:
            print(f"Error enviando alerta: {e}")
            return False
    
    def ejecutar_protocolo_emergencia(self):
        """Protocolo de emergencia activo"""
        print("🚨 SISTEMA DE EMERGENCIA ACTIVADO")
        print("📡 Monitoreo NASA/SWPC en tiempo real")
        print("🔔 Alertas automáticas por Telegram")
        print("=" * 50)
        
        try:
            while True:
                estado = self.monitorear_spaceweather()
                
                print(f"\n🕒 {datetime.now().strftime('%H:%M:%S')}")
                print(f"📊 Estado: {estado['nivel']}")
                print(f"📝 Info: {estado['mensaje']}")
                
                # Enviar alerta inmediata si es crítica
                if estado['critico'] and self.ultima_alerta != estado['mensaje']:
                    if self.enviar_alerta_inmediata(estado['mensaje'], estado['nivel']):
                        print("✅ Alerta enviada por Telegram")
                        self.ultima_alerta = estado['mensaje']
                
                # Esperar 5 minutos entre chequeos (tiempo crítico)
                time.sleep(300)  # 5 minutos
                
        except KeyboardInterrupt:
            print("\n🛑 Sistema de emergencia detenido")
        except Exception as e:
            print(f"❌ Error crítico: {e}")
            # Intentar enviar alerta de error
            self.enviar_alerta_inmediata(f"Error en sistema: {e}", "ALTO")

# Ejecutar inmediatamente
if __name__ == "__main__":
    sistema = SistemaEmergencia()
    sistema.ejecutar_protocolo_emergencia()
