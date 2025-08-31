#!/usr/bin/env python3
"""
🌋 SISTEMA SISMOLÓGICO - Monitorización de terremotos en tiempo real
Datos de: USGS, IGN, EMSC
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

class MonitorSismico:
    """Monitor de actividad sísmica en tiempo real"""
    
    def __init__(self):
        self.fuentes = {
            'usgs': 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson',
            'ign': 'https://www.ign.es/web/ign/portal/sis-catalogo-terremotos',
            'emsc': 'https://www.seismicportal.eu/fdsnws/event/1/query'
        }
        
        self.umbral_alertas = {
            'leve': 3.0,      # M3.0+ - Alertar
            'moderado': 4.0,  # M4.0+ - Peligro
            'fuerte': 5.0     # M5.0+ - Emergencia
        }
        
        logging.info("🌋 Iniciando Monitor Sísmico")
    
    def obtener_datos_usgs(self):
        """Obtener datos de USGS (United States Geological Survey)"""
        try:
            response = requests.get(self.fuentes['usgs'], timeout=10)
            data = response.json()
            
            terremotos = []
            for feature in data['features']:
                prop = feature['properties']
                geo = feature['geometry']
                
                terremoto = {
                    'magnitud': prop['mag'],
                    'profundidad': prop.get('depth', 0),
                    'lugar': prop['place'],
                    'timestamp': datetime.fromtimestamp(prop['time'] / 1000),
                    'lat': geo['coordinates'][1],
                    'lon': geo['coordinates'][0],
                    'fuente': 'USGS',
                    'tsunami': prop.get('tsunami', 0) == 1
                }
                
                # Filtrar por región del Golfo de Cádiz
                if self._es_cercano_golfo_cadiz(terremoto['lat'], terremoto['lon']):
                    terremotos.append(terremoto)
            
            return terremotos
            
        except Exception as e:
            logging.error(f"❌ Error USGS: {e}")
            return []
    
    def _es_cercano_golfo_cadiz(self, lat, lon):
        """Verificar si el sismo es cercano al Golfo de Cádiz"""
        # Coordenadas aproximadas del Golfo de Cádiz
        lat_min, lat_max = 35.0, 37.5
        lon_min, lon_max = -8.0, -5.0
        
        return (lat_min <= lat <= lat_max) and (lon_min <= lon <= lon_max)
    
    def analizar_peligro_tsunami(self, terremoto):
        """Analizar potencial de tsunami basado en parámetros sísmicos"""
        riesgo = 0.0
        
        # Factores de riesgo para tsunami
        if terremoto['magnitud'] >= 7.0:
            riesgo += 0.8
        elif terremoto['magnitud'] >= 6.0:
            riesgo += 0.5
        
        if terremoto['profundidad'] < 30:  # Menos de 30km de profundidad
            riesgo += 0.3
        
        if terremoto['tsunami']:
            riesgo = min(riesgo + 0.4, 1.0)
        
        return min(riesgo, 1.0)
    
    def generar_alerta_sismica(self, terremotos):
        """Generar alertas sísmicas"""
        alertas = []
        
        for terremoto in terremotos:
            if terremoto['magnitud'] >= self.umbral_alertas['fuerte']:
                alertas.append({
                    'nivel': 'EMERGENCIA',
                    'mensaje': f'🌋 TERREMOTO FUERTE M{terremoto["magnitud"]} - {terremoto["lugar"]}',
                    'riesgo_tsunami': self.analizar_peligro_tsunami(terremoto),
                    'terremoto': terremoto
                })
            elif terremoto['magnitud'] >= self.umbral_alertas['moderado']:
                alertas.append({
                    'nivel': 'PELIGRO', 
                    'mensaje': f'⚠️ TERREMOTO MODERADO M{terremoto["magnitud"]} - {terremoto["lugar"]}',
                    'riesgo_tsunami': self.analizar_peligro_tsunami(terremoto),
                    'terremoto': terremoto
                })
            elif terremoto['magnitud'] >= self.umbral_alertas['leve']:
                alertas.append({
                    'nivel': 'ALERTA',
                    'mensaje': f'📢 TERREMOTO LEVE M{terremoto["magnitud"]} - {terremoto["lugar"]}',
                    'riesgo_tsunami': self.analizar_peligro_tsunami(terremoto),
                    'terremoto': terremoto
                })
        
        return alertas
    
    def monitorear_continuo(self, intervalo_minutos=5):
        """Monitoreo sísmico continuo"""
        logging.info(f"🔍 Iniciando monitoreo sísmico cada {intervalo_minutos} minutos")
        
        while True:
            try:
                print(f"\n🌋 MONITOREO SÍSMICO - {datetime.now().strftime('%H:%M:%S')}")
                print("=" * 60)
                
                # Obtener datos
                terremotos = self.obtener_datos_usgs()
                
                if terremotos:
                    print(f"📊 Sismos detectados: {len(terremotos)}")
                    
                    for i, terremoto in enumerate(terremotos, 1):
                        print(f"{i}. M{terremoto['magnitud']} - {terremoto['lugar']} - {terremoto['timestamp'].strftime('%H:%M:%S')}")
                    
                    # Generar alertas
                    alertas = self.generar_alerta_sismica(terremotos)
                    
                    if alertas:
                        print(f"🚨 Alertas generadas: {len(alertas)}")
                        for alerta in alertas:
                            print(f"   {alerta['nivel']}: {alerta['mensaje']}")
                            print(f"   🌊 Riesgo tsunami: {alerta['riesgo_tsunami']:.1%}")
                
                else:
                    print("✅ Sin actividad sísmica significativa")
                
                print("=" * 60)
                time.sleep(intervalo_minutos * 60)
                
            except KeyboardInterrupt:
                print("\n🛑 Monitoreo sísmico detenido")
                break
            except Exception as e:
                logging.error(f"💥 Error en monitoreo: {e}")
                time.sleep(60)  # Esperar 1 minuto antes de reintentar

def main():
    """Función principal"""
    print("=" * 60)
    print("🌋 SISTEMA DE MONITOREO SÍSMICO")
    print("📍 Golfo de Cádiz - Alertas Tempranas")
    print("=" * 60)
    
    monitor = MonitorSismico()
    monitor.monitorear_continuo(intervalo_minutos=2)

if __name__ == "__main__":
    main()
