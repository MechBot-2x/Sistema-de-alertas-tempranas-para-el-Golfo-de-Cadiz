#!/usr/bin/env python3
"""
🎯 SISTEMA PRINCIPAL DE ALERTAS MEJORADO - Golfo de Cádiz
Con monitorización sísmica, marina y lunar REAL
"""

import time
import logging
from datetime import datetime
from scripts.monitoreo.sismico_ign import SismicMonitor
from scripts.monitoreo.datos_mareas import MarineMonitor
from scripts.monitoreo.influencia_lunar import LunarInfluenceCalculator
from scripts.alertas.telegram_simple import enviar_alerta

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/sistema.log'),
        logging.StreamHandler()
    ]
)

class SistemaAlertasAvanzado:
    """Sistema avanzado de monitorización con datos reales"""

    def __init__(self):
        self.estado = "OPERATIVO"
        self.monitor_sismico = SismicMonitor()
        self.monitor_marino = MarineMonitor()
        self.calculador_lunar = LunarInfluenceCalculator()
        self.ultima_verificacion = None

        logging.info("🌊 Iniciando Sistema Avanzado de Alertas del Golfo de Cádiz")

    def verificar_datos_reales(self):
        """Verificación con datos reales de múltiples fuentes"""
        try:
            self.ultima_verificacion = datetime.now()

            # 1. Verificar actividad sísmica
            sismos = self.monitor_sismico.buscar_sismos_golfo_cadiz(dias=1)

            # 2. Verificar datos marinos
            boyas = self.monitor_marino.obtener_datos_boyas()
            mareas = self.monitor_marino.obtener_datos_mareas()

            # 3. Verificar influencia lunar
            fase_lunar = self.calculador_lunar.calcular_fase_lunar(datetime.now())
            influencia_mareas = self.calculador_lunar.calcular_mareas_gravitacionales(datetime.now())

            logging.info(f"✅ Datos reales obtenidos: {len(sismos)} sismos, {len(boyas)} boyas")

            return {
                'sismos': sismos,
                'boyas': boyas,
                'mareas': mareas,
                'fase_lunar': fase_lunar,
                'influencia_mareas': influencia_mareas,
                'timestamp': self.ultima_verificacion.isoformat()
            }

        except Exception as e:
            logging.error(f"❌ Error verificando datos reales: {e}")
            return {}

    def analizar_riesgo_tsunami(self, datos):
        """Analizar riesgo de tsunami basado en datos reales"""
        try:
            riesgo = 0.0

            # Factores de riesgo
            if datos.get('sismos'):
                sismo_mas_fuerte = max([s['magnitud'] for s in datos['sismos']], default=0)
                if sismo_mas_fuerte > 6.0:
                    riesgo += 0.6
                elif sismo_mas_fuerte > 5.0:
                    riesgo += 0.3

            # Influencia de mareas vivas
            if datos.get('influencia_mareas', {}).get('influencia_total', 0) > 1.2:
                riesgo += 0.2

            return min(riesgo, 1.0)

        except Exception as e:
            logging.error(f"❌ Error analizando riesgo tsunami: {e}")
            return 0.0

    def ejecutar_ciclo_monitorizacion(self):
        """Ciclo completo de monitorización"""
        try:
            logging.info("🔄 Ejecutando ciclo avanzado de monitorización")

            # Obtener datos reales
            datos_reales = self.verificar_datos_reales()

            if datos_reales:
                # Analizar riesgo
                riesgo_tsunami = self.analizar_riesgo_tsunami(datos_reales)

                # Log información
                logging.info(f"📊 Riesgo tsunami calculado: {riesgo_tsunami:.2f}")

                # Enviar alerta si es necesario
                if riesgo_tsunami > 0.7:
                    mensaje = f"🚨 ALERTA: Riesgo tsunami alto ({riesgo_tsunami:.2f})"
                    enviar_alerta(mensaje)
                    logging.warning(mensaje)

                return True
            else:
                logging.warning("⚠️ No se pudieron obtener datos reales")
                return False

        except Exception as e:
            logging.critical(f"💥 Error crítico en ciclo: {e}")
            return False

    def ejecutar_continuamente(self):
        """Ejecución continua del sistema"""
        logging.info("🚀 Iniciando ejecución continua avanzada")

        while True:
            try:
                self.ejecutar_ciclo_monitorizacion()
                time.sleep(300)  # Esperar 5 minutos entre ciclos

            except KeyboardInterrupt:
                logging.info("⏹️ Sistema detenido por el usuario")
                break
            except Exception as e:
                logging.error(f"🔧 Error no crítico: {e}")
                time.sleep(60)

if __name__ == "__main__":
    sistema = SistemaAlertasAvanzado()
    sistema.ejecutar_continuamente()
