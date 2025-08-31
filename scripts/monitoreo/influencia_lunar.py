#!/usr/bin/env python3
"""
🌙 INFLUENCIA LUNAR - Cálculos simplificados
"""

import logging
import math
from datetime import datetime


class LunarInfluenceCalculator:
    """Calculadora de influencia lunar simplificada"""

    def __init__(self):
        pass

    def calcular_fase_lunar(self, fecha):
        """Calcular fase lunar aproximada"""
        try:
            dias_ciclo = 29.53
            fecha_referencia = datetime(2024, 1, 11)
            dias_desde_referencia = (fecha - fecha_referencia).days

            fase = (dias_desde_referencia % dias_ciclo) / dias_ciclo

            if fase < 0.05 or fase > 0.95:
                nombre_fase = "Luna Nueva"
            elif fase < 0.45:
                nombre_fase = "Cuarto Creciente"
            elif fase < 0.55:
                nombre_fase = "Luna Llena"
            else:
                nombre_fase = "Cuarto Menguante"

            return {
                "fase": fase,
                "nombre_fase": nombre_fase,
                "iluminacion": int(abs(fase - 0.5) * 200),
            }

        except Exception as e:
            logging.error(f"❌ Error calculando fase lunar: {e}")
            return {"nombre_fase": "Desconocida"}

    def calcular_mareas_gravitacionales(self, fecha):
        """Calcular influencia gravitacional simplificada"""
        try:
            fase_data = self.calcular_fase_lunar(fecha)
            fase = fase_data.get("fase", 0.5)

            influencia = abs(math.sin(fase * 2 * math.pi))

            return {
                "influencia_total": influencia,
                "marea_alta_estimada": 2.0 + influencia * 1.5,
            }

        except Exception as e:
            logging.error(f"❌ Error calculando influencia gravitacional: {e}")
            return {}
