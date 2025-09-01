#!/usr/bin/env python3
"""
🌊 SISTEMA COMPLETO - AEMET + Telegram Alertas
"""

import requests
import time
from datetime import datetime
from sistema_aemet_real import SistemaAEMETReal

class SistemaCompleto(SistemaAEMETReal):
    def __init__(self):
        super().__init__()
        self.telegram_token = "8478499112:AAGxqzYm4I-3Zyc9XCXIkE3mLOl8pXFOM00"
        self.telegram_chat_id = "8350588401"
        self.ultima_alerta = None
        
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
            return response.json().get('ok', False)
            
        except Exception as e:
            print(f"❌ Error enviando Telegram: {e}")
            return False
    
    def verificar_y_alertar(self, datos_meteo, datos_oceano, alertas):
        """Verificar condiciones y enviar alertas"""
        mensaje_alertas = []
        
        # Detectar condiciones peligrosas
        if datos_meteo['viento_velocidad'] > 25:
            mensaje_alertas.append(f"🌪️ <b>VIENTO PELIGROSO</b>: {datos_meteo['viento_velocidad']} km/h {datos_meteo['viento_direccion']}")
        
        if datos_oceano['oleaje_altura'] > 2.0:
            mensaje_alertas.append(f"🌊 <b>OLEAJE PELIGROSO</b>: {datos_oceano['oleaje_altura']} m")
        
        if datos_oceano['corrientes'] > 0.4:
            mensaje_alertas.append(f"🌀 <b>CORRIENTES FUERTES</b>: {datos_oceano['corrientes']} m/s")
        
        # Enviar alerta si hay condiciones peligrosas
        if mensaje_alertas:
            mensaje = f"🚨 <b>ALERTA GOLFO DE CÁDIZ</b>\n"
            mensaje += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            mensaje += "\n".join(mensaje_alertas)
            mensaje += f"\n\n📍 <i>Datos oficiales AEMET</i>"
            
            # Evitar enviar la misma alerta repetidamente
            if mensaje != self.ultima_alerta:
                if self.enviar_telegram(mensaje):
                    print("✅ Alerta enviada por Telegram")
                    self.ultima_alerta = mensaje
        
        return mensaje_alertas
    
    def ejecutar_ciclo_completo(self):
        """Ciclo completo con Telegram"""
        try:
            # Obtener datos
            datos_meteo, fuente = self.obtener_datos_reales()
            datos_oceano = self.datos_oceanicos()
            
            # Generar alertas
            alertas = self.generar_alertas(datos_meteo, datos_oceano)
            
            # Verificar y enviar alertas por Telegram
            self.verificar_y_alertar(datos_meteo, datos_oceano, alertas)
            
            # Mostrar dashboard
            self.mostrar_dashboard_oficial(datos_meteo, datos_oceano, alertas, fuente)
            
            return True
            
        except Exception as e:
            print(f"❌ Error en ciclo completo: {e}")
            return False
    
    def iniciar_servicio_completo(self, intervalo=30):
        """Iniciar servicio completo"""
        print("🔄 INICIANDO SISTEMA COMPLETO AEMET + TELEGRAM")
        print("📱 Alertas enviándose a Telegram automáticamente")
        
        # Enviar mensaje de inicio
        self.enviar_telegram(
            f"✅ <b>SISTEMA ACTIVADO</b>\n"
            f"🌊 Monitorización Golfo de Cádiz\n"
            f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"📡 Fuente: AEMET OpenData oficial"
        )
        
        try:
            ciclo = 0
            while True:
                ciclo += 1
                print(f"\n🔁 CICLO COMPLETO {ciclo}")
                self.ejecutar_ciclo_completo()
                time.sleep(intervalo)
                
        except KeyboardInterrupt:
            # Mensaje de despedida
            self.enviar_telegram(
                f"🛑 <b>SISTEMA DETENIDO</b>\n"
                f"⏰ Final: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"📊 Ciclos completados: {ciclo}"
            )
            print("🎖️ SERVICIO COMPLETO FINALIZADO")

if __name__ == "__main__":
    sistema = SistemaCompleto()
    sistema.iniciar_servicio_completo(intervalo=30)  # 30 segundos
