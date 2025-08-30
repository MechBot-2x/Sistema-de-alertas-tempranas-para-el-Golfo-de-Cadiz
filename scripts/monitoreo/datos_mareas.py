#!/usr/bin/env python3
"""
🌊 MONITOR DE DATOS MARINOS - Versión optimizada
"""

from datetime import datetime
import logging

class MarineMonitor:
    """Monitor de datos marinos simplificado"""
    
    def __init__(self):
        pass
        
    def obtener_datos_boyas(self):
        """Obtener datos de boyas - versión simulada"""
        try:
            # Datos simulados para evitar dependencias externas
            boyas = [
                {
                    'nombre': 'Boyas Cádiz Simuladas',
                    'latitud': 36.5,
                    'longitud': -6.3,
                    'altura_ola': 1.2,
                    'periodo_ola': 7.8,
                    'timestamp': datetime.now().isoformat()
                }
            ]
            
            logging.info("📡 Datos de boyas simulados")
            return boyas
            
        except Exception as e:
            logging.error(f"❌ Error obteniendo datos boyas: {e}")
            return []
    
    def obtener_datos_mareas(self):
        """Obtener datos de mareas simulados"""
        try:
            mareas = {
                'cadiz': {
                    'pleamar': '06:45',
                    'bajamar': '12:30',
                    'coeficiente': 85
                }
            }
            
            logging.info("🌊 Datos de mareas simulados")
            return mareas
            
        except Exception as e:
            logging.error(f"❌ Error obteniendo datos mareas: {e}")
            return {}
