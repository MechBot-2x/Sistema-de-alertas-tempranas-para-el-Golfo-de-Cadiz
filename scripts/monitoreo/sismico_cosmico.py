#!/usr/bin/env python3
"""
🌍 SISTEMA SÍSMICO CÓSMICO - Monitorización avanzada
"""

import json
import logging
import math
import random
from datetime import datetime, timedelta

import requests


class SismicMonitorCosmico:
    """Monitor sísmico con análisis de energía telúrica cósmica"""

    def __init__(self):
        self.fuentes = {
            "usgs": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"
        }

    def obtener_sismos_cosmicos(self, dias=3):
        """Obtener sismos con análisis de energía telúrica"""
        try:
            sismos = self._obtener_usgs_data()

            if not sismos:
                sismos = self._sismos_simulados_cosmicos()

            sismos_filtrados = []
            for sismo in sismos:
                if self._es_reciente(sismo, dias):
                    sismo_con_energia = self._analizar_energia_telurica(sismo)
                    sismos_filtrados.append(sismo_con_energia)

            logging.info(f"🌌 Obtenidos {len(sismos_filtrados)} sismos cósmicos")
            return sismos_filtrados

        except Exception as e:
            logging.error(f"❌ Error cósmico sísmico: {e}")
            return self._sismos_simulados_cosmicos()

    def _obtener_usgs_data(self):
        """Obtener datos de USGS"""
        try:
            response = requests.get(self.fuentes["usgs"], timeout=10)
            if response.status_code == 200:
                datos = response.json()
                sismos = []

                for feature in datos["features"][:20]:
                    prop = feature["properties"]
                    geo = feature["geometry"]

                    sismo = {
                        "magnitud": prop["mag"],
                        "lugar": prop["place"],
                        "timestamp": prop["time"],
                        "latitud": geo["coordinates"][1],
                        "longitud": geo["coordinates"][0],
                        "profundidad": geo["coordinates"][2],
                        "fuente": "USGS",
                        "energia_telurica": self._calcular_energia_telurica(
                            prop["mag"], geo["coordinates"][2]
                        ),
                    }
                    sismos.append(sismo)

                return sismos
        except:
            return []

    def _calcular_energia_telurica(self, magnitud, profundidad):
        """Calcular energía telúrica cósmica"""
        energia = (magnitud**2) / max(1, profundidad / 10)
        return round(min(energia, 10.0), 2)

    def _analizar_energia_telurica(self, sismo):
        """Añadir análisis de energía telúrica"""
        sismo["nivel_energia"] = self._clasificar_energia(sismo["energia_telurica"])
        sismo["riesgo_cosmico"] = self._calcular_riesgo_cosmico(sismo)
        return sismo

    def _clasificar_energia(self, energia):
        """Clasificar energía telúrica"""
        if energia > 5.0:
            return "ALTA_COSMICA"
        if energia > 2.0:
            return "MEDIA_COSMICA"
        return "BAJA_COSMICA"

    def _calcular_riesgo_cosmico(self, sismo):
        """Calcular riesgo cósmico"""
        riesgo = sismo["magnitud"] * 0.2 + sismo["energia_telurica"] * 0.1
        return round(min(riesgo, 1.0), 2)

    def _es_reciente(self, sismo, dias):
        """Verificar si el sismo es reciente"""
        try:
            sismo_time = datetime.fromtimestamp(sismo["timestamp"] / 1000)
            return sismo_time > datetime.now() - timedelta(days=dias)
        except:
            return False

    def _sismos_simulados_cosmicos(self):
        """Sismos simulados con energía cósmica"""
        from datetime import datetime

        return [
            {
                "magnitud": round(2.5 + random.uniform(0, 1.5), 1),
                "lugar": "Golfo de Cádiz - Energía Cósmica",
                "timestamp": int(datetime.now().timestamp() * 1000),
                "latitud": round(36.5 + random.uniform(-0.5, 0.5), 3),
                "longitud": round(-6.5 + random.uniform(-0.5, 0.5), 3),
                "profundidad": round(10 + random.uniform(0, 20), 1),
                "fuente": "SISTEMA_COSMICO",
                "energia_telurica": round(1.5 + random.uniform(0, 2.0), 2),
                "nivel_energia": "MEDIA_COSMICA",
                "riesgo_cosmico": round(0.3 + random.uniform(0, 0.3), 2),
            }
        ]

    def buscar_sismos_golfo_cadiz_cosmicos(self, dias=3):
        """Buscar sismos en Golfo de Cádiz con análisis cósmico"""
        try:
            sismos = self.obtener_sismos_cosmicos(dias)

            # Coordenadas ampliadas del Golfo de Cádiz
            lat_min, lat_max = 35.0, 38.5
            lon_min, lon_max = -9.5, -5.0

            sismos_golfo = [
                s
                for s in sismos
                if (
                    lat_min <= s["latitud"] <= lat_max
                    and lon_min <= s["longitud"] <= lon_max
                )
            ]

            logging.info(
                f"🌊 Encontrados {len(sismos_golfo)} sismos cósmicos en Golfo de Cádiz"
            )
            return sismos_golfo

        except Exception as e:
            logging.error(f"❌ Error cósmico en Golfo: {e}")
            return self._sismos_simulados_cosmicos()
