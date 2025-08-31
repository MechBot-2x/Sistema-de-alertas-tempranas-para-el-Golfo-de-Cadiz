import logging
import os
from datetime import datetime, timedelta

import requests


class NASAClient:
    def __init__(self):
        self.api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
        self.base_url = "https://api.nasa.gov"
        self.logger = logging.getLogger(__name__)

    def get_solar_events(self, start_date=None, end_date=None):
        """Obtener datos de eventos solares de la NASA"""
        try:
            if not start_date:
                start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            if not end_date:
                end_date = datetime.now().strftime("%Y-%m-%d")

            url = f"{self.base_url}/DONKI/FLR"
            params = {
                "startDate": start_date,
                "endDate": end_date,
                "api_key": self.api_key,
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            solar_events = response.json()
            return self._analyze_solar_events(solar_events)

        except Exception as e:
            self.logger.error(f"Error obteniendo datos solares: {e}")
            return self._get_simulated_data()

    def get_geomagnetic_storms(self):
        """Obtener datos de tormentas geomagnéticas"""
        try:
            url = f"{self.base_url}/DONKI/GST"
            params = {
                "startDate": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                "endDate": datetime.now().strftime("%Y-%m-%d"),
                "api_key": self.api_key,
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            return response.json()

        except Exception as e:
            self.logger.error(f"Error obteniendo tormentas geomagnéticas: {e}")
            return []

    def _analyze_solar_events(self, events):
        """Analizar eventos solares y determinar riesgo"""
        analysis = {
            "total_events": len(events),
            "m_class_events": 0,
            "x_class_events": 0,
            "max_intensity": "A0.0",
            "risk_level": "LOW",
        }

        for event in events:
            if "classType" in event:
                class_type = event["classType"]
                if class_type.startswith("M"):
                    analysis["m_class_events"] += 1
                elif class_type.startswith("X"):
                    analysis["x_class_events"] += 1

                # Determinar máxima intensidad
                if self._compare_intensity(class_type, analysis["max_intensity"]) > 0:
                    analysis["max_intensity"] = class_type

        # Determinar nivel de riesgo
        if analysis["x_class_events"] > 0:
            analysis["risk_level"] = "HIGH"
        elif analysis["m_class_events"] > 2:
            analysis["risk_level"] = "MEDIUM"

        return analysis

    def _compare_intensity(self, class1, class2):
        """Comparar intensidad de clases solares"""

        def get_numeric_value(cls):
            if cls.startswith("X"):
                return 100 + float(cls[1:]) if cls[1:] else 100
            elif cls.startswith("M"):
                return 10 + float(cls[1:]) if cls[1:] else 10
            elif cls.startswith("C"):
                return 1 + float(cls[1:]) if cls[1:] else 1
            else:
                return 0

        return get_numeric_value(class1) - get_numeric_value(class2)

    def _get_simulated_data(self):
        """Datos simulados para cuando la API falla"""
        return {
            "total_events": 3,
            "m_class_events": 1,
            "x_class_events": 0,
            "max_intensity": "M2.5",
            "risk_level": "LOW",
            "simulated": True,
        }
