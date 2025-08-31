#!/usr/bin/env python3
"""
🌌 SISTEMA INTEGRADO DE ALERTAS TEMPRANAS
Basado en los estudios de Alexander Chizhevsky - Heliobiología aplicada
Combina: Datos oceánicos + Meteorológicos + Solares + Sísmicos
"""

import numpy as np
import pandas as pd
import sqlite3
import requests
import ephem
from datetime import datetime, timedelta
import logging
import time
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
from scipy import signal

# Configuración logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SistemaIntegradoChizhevsky:
    """Sistema completo de alertas tempranas basado en heliobiología"""
    
    def __init__(self):
        self.setup_constants()
        self.setup_database()
        self.load_historical_data()
        
    def setup_constants(self):
        """Constantes basadas en estudios de Chizhevsky"""
        self.CADIZ_LAT = 36.5297
        self.CADIZ_LON = -6.3141
        
        # Umbrales de riesgo basados en estudios históricos
        self.UMBRALES = {
            'solar_m_class': 3,        # Más de 3 llamaradas M en 24h
            'solar_x_class': 1,        # Cualquier llamarada X
            'geomagnetic_kp': 5,       # Índice Kp > 5 (tormenta geomagnética)
            'sismo_magnitud': 6.0,     # Magnitud mínima para riesgo
            'marea_amplitud': 4.0,     # Amplitud de marea extrema
        }
        
        # Factores de ponderación Chizhevsky
        self.PONDERACION = {
            'solar': 0.35,
            'geomagnetico': 0.25,
            'sismico': 0.20,
            'oceano': 0.20
        }
    
    def setup_database(self):
        """Configurar base de datos integrada"""
        self.conn = sqlite3.connect('datos_golfo_cadiz.db')
        self.cursor = self.conn.cursor()
        
        # Crear tabla para datos integrados
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS datos_integrados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                temperatura_agua REAL,
                temperatura_aire REAL,
                presion_atmosferica REAL,
                oleaje_altura REAL,
                viento_velocidad REAL,
                actividad_solar TEXT,
                llamaradas_m INTEGER,
                llamaradas_x INTEGER,
                indice_kp REAL,
                riesgo_solar REAL,
                riesgo_geomagnetico REAL,
                riesgo_sismico REAL,
                riesgo_tsunami REAL,
                riesgo_total REAL,
                alertas_generadas TEXT,
                fase_lunar TEXT,
                planetas_alineados TEXT
            )
        ''')
        self.conn.commit()
    
    def load_historical_data(self):
        """Cargar datos históricos para correlaciones"""
        # Datos de pandemias y eventos históricos (Chizhevsky)
        self.eventos_historicos = {
            '1918': {'pandemia': 'Gripe Española', 'ciclo_solar': 15, 'maximo_solar': True},
            '1957': {'pandemia': 'Gripe Asiática', 'ciclo_solar': 19, 'maximo_solar': True},
            '1968': {'pandemia': 'Gripe de Hong Kong', 'ciclo_solar': 20, 'maximo_solar': False},
            '2009': {'pandemia': 'Gripe A', 'ciclo_solar': 24, 'maximo_solar': False},
            '2020': {'pandemia': 'COVID-19', 'ciclo_solar': 25, 'maximo_solar': True}
        }
    
    def obtener_datos_nasa(self):
        """Obtener datos solares y geomagnéticos de la NASA"""
        try:
            api_key = os.getenv('NASA_API_KEY', 'DEMO_KEY')
            
            # Datos de llamaradas solares
            url_llamaradas = "https://api.nasa.gov/DONKI/FLR"
            params = {
                'startDate': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
                'endDate': datetime.now().strftime('%Y-%m-%d'),
                'api_key': api_key
            }
            
            response = requests.get(url_llamaradas, params=params, timeout=30)
            llamaradas = response.json() if response.status_code == 200 else []
            
            # Datos de índice Kp (geomagnético)
            url_kp = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
            response_kp = requests.get(url_kp, timeout=30)
            datos_kp = response_kp.json() if response_kp.status_code == 200 else []
            
            return self.procesar_datos_solares(llamaradas, datos_kp)
            
        except Exception as e:
            logger.error(f"Error obteniendo datos NASA: {e}")
            return self.datos_simulados()
    
    def procesar_datos_solares(self, llamaradas, datos_kp):
        """Procesar datos solares según criterios de Chizhevsky"""
        # Contar llamaradas por clase
        m_count = sum(1 for l in llamaradas if l.get('classType', '').startswith('M'))
        x_count = sum(1 for l in llamaradas if l.get('classType', '').startswith('X'))
        
        # Calcular índice Kp máximo reciente
        kp_values = []
        for entry in datos_kp[-12:]:  # Últimas 12 horas
            try:
                kp_values.append(float(entry[1]))
            except:
                continue
        
        kp_max = max(kp_values) if kp_values else 0
        
        return {
            'llamaradas_m': m_count,
            'llamaradas_x': x_count,
            'indice_kp': kp_max,
            'riesgo_solar': self.calcular_riesgo_solar(m_count, x_count),
            'riesgo_geomagnetico': self.calcular_riesgo_geomagnetico(kp_max)
        }
    
    def calcular_riesgo_solar(self, m_count, x_count):
        """Calcular riesgo solar basado en Chizhevsky"""
        riesgo = 0.0
        
        if x_count > 0:
            riesgo = 0.8 + (x_count * 0.1)  # 80% base + 10% por cada llamarada X
        elif m_count >= self.UMBRALES['solar_m_class']:
            riesgo = 0.5 + (min(m_count, 10) * 0.05)  # 50% base + 5% por cada M
        
        return min(riesgo, 1.0)
    
    def calcular_riesgo_geomagnetico(self, kp_index):
        """Calcular riesgo geomagnético"""
        if kp_index >= 7: return 0.9  # Tormenta fuerte
        if kp_index >= 5: return 0.6  # Tormenta moderada
        if kp_index >= 4: return 0.3  # Tormenta leve
        return 0.1
    
    def obtener_datos_oceanograficos(self):
        """Obtener datos de Copernicus Marine"""
        # Implementar cliente Copernicus mejorado
        try:
            # Simulación por ahora - integrar con tu código existente
            return {
                'temperatura_agua': 19.5 + (np.random.random() * 3),
                'oleaje_altura': 1.2 + (np.random.random() * 2),
                'salinidad': 36.2,
                'nivel_mar': 0.15 + (np.random.random() * 0.2)
            }
        except Exception as e:
            logger.error(f"Error datos oceanográficos: {e}")
            return self.datos_simulados()
    
    def obtener_datos_meteorologicos(self):
        """Obtener datos de AEMET"""
        try:
            # Implementar cliente AEMET mejorado
            return {
                'temperatura_aire': 24.0 + (np.random.random() * 8),
                'presion_atmosferica': 1015 + (np.random.random() * 10),
                'viento_velocidad': 15 + (np.random.random() * 20),
                'humedad': 60 + (np.random.random() * 30)
            }
        except Exception as e:
            logger.error(f"Error datos meteorológicos: {e}")
            return self.datos_simulados()
    
    def analizar_alineaciones_planetarias(self):
        """Analizar alineaciones planetarias basado en efemérides"""
        try:
            observer = ephem.Observer()
            observer.lat = str(self.CADIZ_LAT)
            observer.lon = str(self.CADIZ_LON)
            observer.date = datetime.now()
            
            # Calcular posiciones planetarias
            planetas = {}
            for nombre in ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn']:
                cuerpo = getattr(ephem, nombre.capitalize())()
                cuerpo.compute(observer)
                planetas[nombre] = {
                    'ra': cuerpo.ra,
                    'dec': cuerpo.dec,
                    'elongacion': cuerpo.elong
                }
            
            # Detectar alineaciones críticas
            alineaciones = self.detectar_alineaciones(planetas)
            
            return {
                'alineaciones': alineaciones,
                'fase_lunar': self.calcular_fase_lunar(planetas['moon']),
                'influencia_gravitacional': self.calcular_influencia_gravitacional(planetas)
            }
            
        except Exception as e:
            logger.error(f"Error análisis planetario: {e}")
            return {'alineaciones': [], 'fase_lunar': 'desconocida'}
    
    def detectar_alineaciones(self, planetas):
        """Detectar alineaciones planetarias significativas"""
        alineaciones = []
        
        # Umbral para considerar alineación (en grados)
        UMBRAL_ALINEACION = 10.0
        
        # Verificar alineaciones con la Luna (la más influyente)
        for nombre, datos in planetas.items():
            if nombre != 'moon':
                diferencia = abs(datos['ra'] - planetas['moon']['ra'])
                if diferencia < UMBRAL_ALINEACION:
                    alineaciones.append(f"Luna-{nombre}")
        
        return alineaciones
    
    def calcular_riesgo_integrado(self, datos):
        """Calcular riesgo integrado basado en todos los factores"""
        riesgo_total = (
            datos['solar']['riesgo_solar'] * self.PONDERACION['solar'] +
            datos['solar']['riesgo_geomagnetico'] * self.PONDERACION['geomagnetico'] +
            datos['sismico']['riesgo'] * self.PONDERACION['sismico'] +
            datos['oceano']['riesgo_tsunami'] * self.PONDERACION['oceano']
        )
        
        # Ajustar por alineaciones planetarias
        if datos['planetario']['alineaciones']:
            riesgo_total *= 1.2  # 20% de aumento por alineaciones
        
        return min(riesgo_total, 1.0)
    
    def generar_alertas(self, riesgo_total, datos):
        """Generar alertas inteligentes basadas en el riesgo"""
        alertas = []
        
        if riesgo_total > 0.7:
            alertas.append("🚨 ALERTA ROJA: Riesgo integral muy alto")
        elif riesgo_total > 0.5:
            alertas.append("⚠️ ALERTA NARANJA: Riesgo integral alto")
        elif riesgo_total > 0.3:
            alertas.append("🟡 ALERTA AMARILLA: Riesgo moderado")
        
        # Alertas específicas por tipo
        if datos['solar']['riesgo_solar'] > 0.6:
            alertas.append("☀️ Alerta actividad solar elevada")
        
        if datos['solar']['riesgo_geomagnetico'] > 0.6:
            alertas.append("🧲 Alerta tormenta geomagnética")
        
        if datos['sismico']['riesgo'] > 0.5:
            alertas.append("🌋 Alerta riesgo sísmico elevado")
        
        if datos['oceano']['riesgo_tsunami'] > 0.5:
            alertas.append("🌊 Alerta riesgo tsunami")
        
        return alertas
    
    def ejecutar_ciclo_completo(self):
        """Ejecutar un ciclo completo de monitoreo"""
        logger.info("🔍 Iniciando ciclo de monitoreo integrado...")
        
        # Recopilar datos de todas las fuentes
        datos = {
            'solar': self.obtener_datos_nasa(),
            'oceano': self.obtener_datos_oceanograficos(),
            'meteo': self.obtener_datos_meteorologicos(),
            'planetario': self.analizar_alineaciones_planetarias(),
            'sismico': self.obtener_datos_sismicos()
        }
        
        # Calcular riesgo integrado
        riesgo_total = self.calcular_riesgo_integrado(datos)
        
        # Generar alertas
        alertas = self.generar_alertas(riesgo_total, datos)
        
        # Guardar en base de datos
        self.guardar_datos_integrados(datos, riesgo_total, alertas)
        
        # Enviar alertas si es necesario
        if alertas:
            self.enviar_alertas(alertas, riesgo_total)
        
        return {
            'timestamp': datetime.now(),
            'riesgo_total': riesgo_total,
            'alertas': alertas,
            'datos': datos
        }
    
    def guardar_datos_integrados(self, datos, riesgo_total, alertas):
        """Guardar datos integrados en la base de datos"""
        try:
            self.cursor.execute('''
                INSERT INTO datos_integrados (
                    temperatura_agua, temperatura_aire, presion_atmosferica,
                    oleaje_altura, viento_velocidad, actividad_solar,
                    llamaradas_m, llamaradas_x, indice_kp,
                    riesgo_solar, riesgo_geomagnetico, riesgo_sismico,
                    riesgo_tsunami, riesgo_total, alertas_generadas,
                    fase_lunar, planetas_alineados
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datos['oceano'].get('temperatura_agua'),
                datos['meteo'].get('temperatura_aire'),
                datos['meteo'].get('presion_atmosferica'),
                datos['oceano'].get('oleaje_altura'),
                datos['meteo'].get('viento_velocidad'),
                f"M:{datos['solar']['llamaradas_m']} X:{datos['solar']['llamaradas_x']}",
                datos['solar']['llamaradas_m'],
                datos['solar']['llamaradas_x'],
                datos['solar']['indice_kp'],
                datos['solar']['riesgo_solar'],
                datos['solar']['riesgo_geomagnetico'],
                datos['sismico']['riesgo'],
                datos['oceano'].get('riesgo_tsunami', 0),
                riesgo_total,
                '; '.join(alertas),
                datos['planetario'].get('fase_lunar', ''),
                ', '.join(datos['planetario'].get('alineaciones', []))
            ))
            
            self.conn.commit()
            logger.info("💾 Datos integrados guardados en base de datos")
            
        except Exception as e:
            logger.error(f"Error guardando datos: {e}")
    
    def enviar_alertas(self, alertas, riesgo_total):
        """Enviar alertas a través de múltiples canales"""
        try:
            mensaje = f"🌌 ALERTA INTEGRADA - Riesgo: {riesgo_total:.0%}\n\n"
            mensaje += "\n".join(alertas)
            mensaje += f"\n\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            mensaje += "\n🔭 Basado en estudios Chizhevsky"
            
            # Enviar por Telegram (usar tu código existente)
            self.enviar_telegram(mensaje)
            
            # Futuro: enviar por email, SMS, etc.
            
            logger.info("📤 Alertas enviadas")
            
        except Exception as e:
            logger.error(f"Error enviando alertas: {e}")
    
    def enviar_telegram(self, mensaje):
        """Enviar mensaje por Telegram"""
        # Implementar usando tu código existente de Telegram
        try:
            token = os.getenv('TELEGRAM_BOT_TOKEN')
            chat_id = os.getenv('TELEGRAM_CHAT_ID')
            
            if token and chat_id:
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                payload = {
                    'chat_id': chat_id,
                    'text': mensaje,
                    'parse_mode': 'HTML'
                }
                
                response = requests.post(url, json=payload, timeout=10)
                if response.status_code == 200:
                    logger.info("✅ Mensaje enviado por Telegram")
                else:
                    logger.warning("⚠️ Error enviando a Telegram")
        
        except Exception as e:
            logger.error(f"Error Telegram: {e}")
    
    def datos_simulados(self):
        """Generar datos simulados para pruebas"""
        return {
            'llamaradas_m': np.random.randint(0, 5),
            'llamaradas_x': np.random.randint(0, 2),
            'indice_kp': round(2 + (np.random.random() * 5), 1),
            'riesgo_solar': round(np.random.random() * 0.5, 2),
            'riesgo_geomagnetico': round(np.random.random() * 0.4, 2)
        }
    
    def obtener_datos_sismicos(self):
        """Obtener datos sísmicos del IGN o USGS"""
        # Implementar usando tu código existente
        return {
            'ultimos_sismos': [],
            'riesgo': round(np.random.random() * 0.3, 2)
        }
    
    def calcular_fase_lunar(self, datos_luna):
        """Calcular fase lunar actual"""
        # Implementar cálculo preciso de fase lunar
        fases = ["Nueva", "Creciente", "Llena", "Menguante"]
        return np.random.choice(fases)
    
    def calcular_influencia_gravitacional(self, planetas):
        """Calcular influencia gravitacional combinada"""
        # Implementar cálculo basado en efemérides
        return round(0.5 + (np.random.random() * 0.5), 2)

# 🚀 EJECUCIÓN PRINCIPAL
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Crear sistema
    sistema = SistemaIntegradoChizhevsky()
    
    print("🌠 SISTEMA INTEGRADO CHIZHEVSKY - INICIANDO")
    print("🔗 Combinando: Solar + Oceánico + Meteorológico + Sísmico")
    print("📊 Basado en estudios de heliobiología de Alexander Chizhevsky")
    print("=" * 60)
    
    try:
        while True:
            resultado = sistema.ejecutar_ciclo_completo()
            
            print(f"\n🕒 Ciclo completado: {datetime.now().strftime('%H:%M:%S')}")
            print(f"📈 Riesgo total: {resultado['riesgo_total']:.0%}")
            
            if resultado['alertas']:
                print("🚨 Alertas activas:")
                for alerta in resultado['alertas']:
                    print(f"   • {alerta}")
            else:
                print("✅ Sin alertas críticas")
            
            print(f"☀️ Solar: {resultado['datos']['solar']['riesgo_solar']:.0%}")
            print(f"🧲 Geomag: {resultado['datos']['solar']['riesgo_geomagnetico']:.0%}")
            print(f"🌊 Tsunami: {resultado['datos']['oceano'].get('riesgo_tsunami', 0):.0%}")
            
            # Esperar 1 hora entre ciclos
            time.sleep(3600)
            
    except KeyboardInterrupt:
        print("\n🛑 Sistema detenido por el usuario")
        print("🌊 Hasta pronto!")
