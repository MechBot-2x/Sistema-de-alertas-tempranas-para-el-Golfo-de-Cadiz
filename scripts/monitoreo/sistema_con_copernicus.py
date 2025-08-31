#!/usr/bin/env python3
"""
🎯 SISTEMA CON COPERNICUS - Datos oceánicos profesionales
"""

import logging
import time
from datetime import datetime

from scripts.datos.copernicus_client import CopernicusMarineClient
from scripts.monitoreo.sistema_principal_mejorado import SistemaResiliente

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class SistemaConCopernicus(SistemaResiliente):
    """Sistema evolucionado con datos de Copernicus Marine"""

    def __init__(self):
        super().__init__()
        self.copernicus_client = CopernicusMarineClient()

        logging.info("🌊 SISTEMA COPERNICUS MARINE INICIADO")

        # Verificar conexión
        self._verificar_copernicus()

    def _verificar_copernicus(self):
        """Verificar estado de Copernicus"""
        estado = self.copernicus_client.verificar_conexion()
        logging.info(f"📡 Copernicus: {estado['estado']}")

        if estado["estado"] == "MODO_SIMULACION":
            logging.info("💡 Para datos reales: https://marine.copernicus.eu")

    def obtener_datos_oceanicos(self):
        """Obtener datos oceánicos completos"""
        try:
            datos = self.copernicus_client.obtener_datos_golfo_cadiz()

            # Añadir análisis adicional
            datos["riesgo_tsunami"] = self._calcular_riesgo_tsunami(datos)
            datos["estado_mareal"] = self._clasificar_estado_mareal(datos)

            logging.info(f"🌊 Datos oceánicos: {datos['temperatura_superficie']}°C")
            return datos

        except Exception as e:
            logging.error(f"❌ Error datos oceánicos: {e}")
            return self.copernicus_client._simular_datos_copernicus()

    def _calcular_riesgo_tsunami(self, datos_oceanicos):
        """Calcular riesgo de tsunami basado en datos oceánicos"""
        riesgo = 0.0

        # Factores de riesgo (simplificado)
        if datos_oceanicos.get("nivel_mar", 0) > 0.5:
            riesgo += 0.3

        if datos_oceanicos.get("corriente_velocidad", 0) > 1.0:
            riesgo += 0.2

        return min(riesgo, 1.0)

    def _clasificar_estado_mareal(self, datos_oceanicos):
        """Clasificar estado mareal"""
        nivel = datos_oceanicos.get("nivel_mar", 0)

        if nivel > 0.3:
            return "PLEAMAR"
        elif nivel < -0.3:
            return "BAJAMAR"
        else:
            return "NORMAL"

    def ejecutar_ciclo_completo(self):
        """Ciclo completo con datos oceánicos"""
        try:
            # Datos de sistemas base
            datos_base = super().ejecutar_ciclo_completo()

            # Datos oceánicos de Copernicus
            datos_oceanicos = self.obtener_datos_oceanicos()

            # Análisis integrado
            self._analisis_integrado(datos_base, datos_oceanicos)

            return True

        except Exception as e:
            logging.error(f"💥 Error en ciclo Copernicus: {e}")
            return False

    def _analisis_integrado(self, datos_base, datos_oceanicos):
        """Análisis integrado de todos los datos"""
        print("\n" + "=" * 60)
        print("🌊 ANÁLISIS INTEGRADO COPERNICUS")
        print("=" * 60)

        print(f"🌡️ Temp superficie: {datos_oceanicos['temperatura_superficie']}°C")
        print(f"🧂 Salinidad: {datos_oceanicos['salinidad']} PSU")
        print(f"📈 Nivel mar: {datos_oceanicos['nivel_mar']} m")
        print(f"🌀 Corrientes: {datos_oceanicos['corriente_velocidad']} m/s")
        print(f"🎯 Riesgo tsunami: {datos_oceanicos['riesgo_tsunami']:.2f}")
        print(f"🌊 Estado mareal: {datos_oceanicos['estado_mareal']}")
        print(f"📡 Fuente: {datos_oceanicos['fuente']}")

        print("=" * 60)


def ejecutar_sistema_copernicus():
    """Ejecutar sistema con Copernicus"""
    print("=" * 60)
    print("🚀 SISTEMA CON COPERNICUS MARINE SERVICE")
    print("=" * 60)

    sistema = SistemaConCopernicus()

    try:
        sistema.ejecutar_continuamente()
    except KeyboardInterrupt:
        print("\n⏹️ Sistema Copernicus detenido")


if __name__ == "__main__":
    ejecutar_sistema_copernicus()
