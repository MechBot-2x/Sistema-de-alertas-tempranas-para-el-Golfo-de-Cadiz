#!/usr/bin/env python3
"""
🌊 SISTEMA DE ALERTA TEMPRANA - SALVANDO VIDAS
Versión simplificada para principiantes
"""

import sqlite3
import requests
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SistemaAlertaVidas:
    def __init__(self):
        self.configurar()
        self.inicializar_base_datos()
    
    def configurar(self):
        """Cargar configuración desde .env"""
        load_dotenv()
        
        self.config = {
            'telegram_token': os.getenv('TELEGRAM_BOT_TOKEN'),
            'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID'),
            'nasa_api_key': os.getenv('NASA_API_KEY'),
            'ciclo_minutos': int(os.getenv('CICLO_MONITOREO_MINUTOS', 60))
        }
        
        logger.info("✅ Configuración cargada")
    
    def inicializar_base_datos(self):
        """Crear base de datos si no existe"""
        self.conn = sqlite3.connect('alertas_vidas.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS alertas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                tipo TEXT,
                nivel TEXT,
                mensaje TEXT,
                enviada INTEGER
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS datos_solares (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                llamaradas_m INTEGER,
                llamaradas_x INTEGER,
                indice_kp REAL
            )
        ''')
        
        self.conn.commit()
        logger.info("✅ Base de datos inicializada")
    
    def obtener_datos_solares(self):
        """Obtener datos del sol de la NASA"""
        try:
            url = "https://api.nasa.gov/DONKI/FLR"
            params = {
                'startDate': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                'endDate': datetime.now().strftime('%Y-%m-%d'),
                'api_key': self.config['nasa_api_key']
            }
            
            response = requests.get(url, params=params, timeout=10)
            datos = response.json() if response.status_code == 200 else []
            
            # Contar llamaradas
            m_count = sum(1 for d in datos if d.get('classType', '').startswith('M'))
            x_count = sum(1 for d in datos if d.get('classType', '').startswith('X'))
            
            # Obtener índice Kp
            kp = self.obtener_indice_kp()
            
            return {
                'llamaradas_m': m_count,
                'llamaradas_x': x_count,
                'indice_kp': kp,
                'riesgo': self.calcular_riesgo_solar(m_count, x_count, kp)
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo datos solares: {e}")
            return {'llamaradas_m': 0, 'llamaradas_x': 0, 'indice_kp': 2.0, 'riesgo': 0.1}
    
    def obtener_indice_kp(self):
        """Obtener índice Kp geomagnético"""
        try:
            url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
            response = requests.get(url, timeout=10)
            datos = response.json()
            
            # Obtener el último valor
            if datos and len(datos) > 1:
                return float(datos[-1][1])
            return 2.0
            
        except:
            return 2.0
    
    def calcular_riesgo_solar(self, m_count, x_count, kp):
        """Calcular riesgo basado en actividad solar"""
        riesgo = 0.0
        
        if x_count > 0:
            riesgo = 0.8
        elif m_count >= 3:
            riesgo = 0.5
        elif m_count >= 1:
            riesgo = 0.3
        
        # Ajustar por actividad geomagnética
        if kp >= 5:
            riesgo += 0.2
        
        return min(riesgo, 1.0)
    
    def verificar_alertas(self, datos_solares):
        """Verificar si hay que enviar alertas"""
        alertas = []
        
        if datos_solares['riesgo'] >= 0.7:
            alertas.append({
                'tipo': 'SOLAR',
                'nivel': 'ALTO',
                'mensaje': f"⚠️ ALTA ACTIVIDAD SOLAR: {datos_solares['llamaradas_m']}M, {datos_solares['llamaradas_x']}X, Kp={datos_solares['indice_kp']}"
            })
        
        elif datos_solares['riesgo'] >= 0.5:
            alertas.append({
                'tipo': 'SOLAR', 
                'nivel': 'MEDIO',
                'mensaje': f"🔶 Actividad solar moderada: {datos_solares['llamaradas_m']} llamaradas M"
            })
        
        return alertas
    
    def enviar_alerta_telegram(self, mensaje):
        """Enviar mensaje por Telegram"""
        try:
            if not self.config['telegram_token'] or not self.config['telegram_chat_id']:
                logger.warning("❌ Configuración de Telegram incompleta")
                return False
            
            url = f"https://api.telegram.org/bot{self.config['telegram_token']}/sendMessage"
            payload = {
                'chat_id': self.config['telegram_chat_id'],
                'text': mensaje,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Error enviando Telegram: {e}")
            return False
    
    def guardar_datos(self, datos_solares, alertas):
        """Guardar datos en base de datos"""
        try:
            # Guardar datos solares
            self.cursor.execute('''
                INSERT INTO datos_solares (fecha, llamaradas_m, llamaradas_x, indice_kp)
                VALUES (?, ?, ?, ?)
            ''', (datetime.now().isoformat(), datos_solares['llamaradas_m'], 
                 datos_solares['llamaradas_x'], datos_solares['indice_kp']))
            
            # Guardar alertas
            for alerta in alertas:
                enviada = 1 if self.enviar_alerta_telegram(alerta['mensaje']) else 0
                
                self.cursor.execute('''
                    INSERT INTO alertas (fecha, tipo, nivel, mensaje, enviada)
                    VALUES (?, ?, ?, ?, ?)
                ''', (datetime.now().isoformat(), alerta['tipo'], alerta['nivel'], 
                     alerta['mensaje'], enviada))
            
            self.conn.commit()
            logger.info("💾 Datos guardados correctamente")
            
        except Exception as e:
            logger.error(f"Error guardando datos: {e}")
            self.conn.rollback()
    
    def ejecutar_ciclo(self):
        """Ejecutar un ciclo completo de monitoreo"""
        logger.info("🔍 Ejecutando ciclo de monitoreo...")
        
        # 1. Obtener datos
        datos_solares = self.obtener_datos_solares()
        
        # 2. Verificar alertas
        alertas = self.verificar_alertas(datos_solares)
        
        # 3. Guardar y enviar
        self.guardar_datos(datos_solares, alertas)
        
        # 4. Mostrar resumen
        print(f"\n🌞 RESUMEN {datetime.now().strftime('%H:%M:%S')}")
        print(f"   Llamaradas M: {datos_solares['llamaradas_m']}")
        print(f"   Llamaradas X: {datos_solares['llamaradas_x']}") 
        print(f"   Índice Kp: {datos_solares['indice_kp']}")
        print(f"   Riesgo: {datos_solares['riesgo']:.0%}")
        print(f"   Alertas: {len(alertas)}")
        
        return alertas
    
    def ejecutar_continuamente(self):
        """Ejecutar el sistema continuamente"""
        print("🚀 SISTEMA DE ALERTA TEMPRANA - INICIADO")
        print("📡 Monitoreando actividad solar para salvar vidas")
        print("=" * 50)
        
        try:
            while True:
                alertas = self.ejecutar_ciclo()
                
                if alertas:
                    print("🚨 Alertas activas:")
                    for alerta in alertas:
                        print(f"   • {alerta['mensaje']}")
                
                # Esperar hasta el próximo ciclo
                print(f"\n⏰ Próximo ciclo en {self.config['ciclo_minutos']} minutos...")
                time.sleep(self.config['ciclo_minutos'] * 60)
                
        except KeyboardInterrupt:
            print("\n🛑 Sistema detenido por el usuario")
            print("❤️  Gracias por ayudar a salvar vidas!")
        finally:
            self.conn.close()

# Ejecutar el sistema
if __name__ == "__main__":
    sistema = SistemaAlertaVidas()
    sistema.ejecutar_continuamente()
