#!/usr/bin/env python3
"""
🎯 SISTEMA CON COPERNICUS - Datos oceánicos profesionales
"""

import time
import logging
from datetime import datetime
from scripts.monitoreo.sistema_principal_mejorado import SistemaResiliente
from scripts.datos.copernicus_client import CopernicusMarineClient

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
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
        
        if estado['estado'] == 'MODO_SIMULACION':
            logging.info("💡 Para datos reales: https://marine.copernicus.eu")
    
    def obtener_datos_oceanicos(self):
        """Obtener datos oceánicos completos"""
        try:
            datos = self.copernicus_client.obtener_datos_golfo_cadiz()
            
            # Añadir análisis adicional
            datos['riesgo_tsunami'] = self._calcular_riesgo_tsunami(datos)
            datos['estado_mareal'] = self._clasificar_estado_mareal(datos)
            
            logging.info(f"🌊 Datos oceánicos: {datos['temperatura_superficie']}°C")
            return datos
            
        except Exception as e:
            logging.error(f"❌ Error datos oceánicos: {e}")
            return self.copernicus_client._simular_datos_copernicus()
    
    def _calcular_riesgo_tsunami(self, datos_oceanicos):
