#!/usr/bin/env python3
"""
🌍 MONITOR SÍSMICO IGN - Versión optimizada para Termux
"""

from datetime import datetime, timedelta
import logging

class SismicMonitor:
    """Monitor de actividad sísmica optimizado"""

    def __init__(self):
        self.api_url = "https://www.ign.es/web/ign/portal/sis-catalogo-terremotos"
        self.last_check = None

    def obtener_ultimos_sismos(self, dias=1, magnitud_minima=2.0):
        """Obtener últimos sismos - versión simplificada"""
        try:
            # Simulación de datos para evitar problemas de conexión
            sismos_ejemplo = [
                {
                    'fecha': (datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d'),
                    'hora': '10:30:45',
                    'latitud': 36.8,
                    'longitud': -7.2,
                    'profundidad': 12.5,
                    'magnitud': 2.8,
                    'localizacion': 'Golfo de Cádiz'
                },
                {
                    'fecha': (datetime.now() - timedelta(hours=5)).strftime('%Y-%m-%d'),
                    'hora': '07:45:12',
                    'latitud': 37.1,
                    'longitud': -6.9,
                    'profundidad': 8.3,
                    'magnitud': 3.2,
                    'localizacion': 'Costa de Huelva'
                }
            ]

            # Filtrar por magnitud
            sismos_filtrados = [
                s for s in sismos_ejemplo
                if s['magnitud'] >= magnitud_minima
            ]

            logging.info(f"📡 Simulados {len(sismos_filtrados)} sismos (modo prueba)")
            return sismos_filtrados

        except Exception as e:
            logging.error(f"❌ Error en monitor sísmico: {e}")
            return []

    def buscar_sismos_golfo_cadiz(self, dias=1):
        """Buscar sismos en Golfo de Cádiz"""
        try:
            # Coordenadas del Golfo de Cádiz
            sismos = self.obtener_ultimos_sismos(dias)
            sismos_golfo = [
                s for s in sismos
                if 35.5 <= s['latitud'] <= 37.5 and -8.0 <= s['longitud'] <= -5.0
            ]

            logging.info(f"🌊 Encontrados {len(sismos_golfo)} sismos en Golfo de Cádiz")
            return sismos_golfo

        except Exception as e:
            logging.error(f"❌ Error buscando sismos: {e}")
            return []
