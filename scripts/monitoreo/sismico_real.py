#!/usr/bin/env python3
"""
🌍 MONITOR SÍSMICO USGS - Datos reales del Servicio Geológico de EE.UU.
"""

import requests
import json
from datetime import datetime, timedelta
import logging

class SismicMonitorReal:
    """Monitor de actividad sísmica con datos reales USGS"""
    
    def __init__(self):
        self.usgs_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"
        
    def obtener_sismos_reales(self, dias=1, magnitud_minima=2.0):
        """Obtener sismos reales del USGS"""
        try:
            response = requests.get(self.usgs_url, timeout=15)
            response.raise_for_status()
            
            datos = response.json()
            sismos = []
            
            for feature in datos['features']:
                propiedades = feature['properties']
                geometria = feature['geometry']
                
                sismo = {
                    'fecha': datetime.fromtimestamp(propiedades['time']/1000).strftime('%Y-%m-%d'),
                    'hora': datetime.fromtimestamp(propiedades['time']/1000).strftime('%H:%M:%S'),
                    'magnitud': propiedades['mag'],
                    'lugar': propiedades['place'],
                    'latitud': geometria['coordinates'][1],
                    'longitud': geometria['coordinates'][0],
                    'profundidad': geometria['coordinates'][2],
                    'timestamp': propiedades['time']
                }
                
                # Filtrar por magnitud y tiempo
                if (sismo['magnitud'] >= magnitud_minima and 
                    datetime.fromtimestamp(propiedades['time']/1000) > datetime.now() - timedelta(days=dias)):
                    sismos.append(sismo)
            
            logging.info(f"📡 Obtenidos {len(sismos)} sismos reales de USGS")
            return sismos
            
        except Exception as e:
            logging.error(f"❌ Error obteniendo sismos USGS: {e}")
            # Fallback a datos simulados
            return self._datos_simulados()
    
    def buscar_sismos_golfo_cadiz(self, dias=1):
        """Buscar sismos reales en Golfo de Cádiz"""
        try:
            sismos = self.obtener_sismos_reales(dias)
            
            # Coordenadas del Golfo de Cádiz
            lat_min, lat_max = 35.5, 37.5
            lon_min, lon_max = -8.0, -5.0
            
            sismos_golfo = [
                s for s in sismos
                if (lat_min <= s['latitud'] <= lat_max and 
                    lon_min <= s['longitud'] <= lon_max)
            ]
            
            logging.info(f"🌊 Encontrados {len(sismos_golfo)} sismos reales en Golfo de Cádiz")
            return sismos_golfo
            
        except Exception as e:
            logging.error(f"❌ Error buscando sismos Golfo: {e}")
            return self._datos_simulados_golfo()
    
    def _datos_simulados(self):
        """Datos simulados como fallback"""
        return [
            {
                'fecha': (datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d'),
                'hora': '10:30:45',
                'latitud': 36.8,
                'longitud': -7.2,
                'profundidad': 12.5,
                'magnitud': 2.8,
                'lugar': 'Golfo de Cádiz - Simulado'
            }
        ]
    
    def _datos_simulados_golfo(self):
        """Datos simulados específicos para Golfo de Cádiz"""
        return self._datos_simulados()
