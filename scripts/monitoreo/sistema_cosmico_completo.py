#!/usr/bin/env python3
"""
🌌 SISTEMA CÓSMICO COMPLETO - Versión reconstruida
"""

import time
import logging
from datetime import datetime
from scripts.monitoreo.sismico_cosmico import SismicMonitorCosmico
from scripts.monitoreo.boyas_avanzadas_2025 import BoyasAvanzadas2025
from scripts.monitoreo.influencia_lunar import LunarInfluenceCalculator

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - 🌌 %(message)s'
)

class SistemaCosmicoCompleto:
    """Sistema completo de monitorización cósmica"""

    def __init__(self):
        self.estado = "OPERATIVO_CÓSMICO"
        self.monitor_sismico = SismicMonitorCosmico()
        self.monitor_boyas = BoyasAvanzadas2025()
        self.calculador_lunar = LunarInfluenceCalculator()

        logging.info("🌠 SISTEMA CÓSMICO INICIADO")

    def medir_energia_cosmica(self):
        """Medir energía cósmica"""
        try:
            import math
            ahora = datetime.now()
            dia_anio = ahora.timetuple().tm_yday
            hora_dia = ahora.hour + ahora.minute/60

            energia = (
                math.sin(dia_anio / 365 * 2 * math.pi) * 0.4 +
                math.cos(hora_dia / 24 * 4 * math.pi) * 0.3 +
                (ahora.day / 31) * 0.3
            )

            energia_normalizada = (energia + 1) / 2

            return {
                'nivel_energia': round(energia_normalizada, 3),
                'estado': self._clasificar_energia_cosmica(energia_normalizada),
                'timestamp': ahora.isoformat()
            }

        except Exception as e:
            logging.error(f"❌ Error medición cósmica: {e}")
            return {'nivel_energia': 0.5, 'estado': 'ESTABLE'}

    def _clasificar_energia_cosmica(self, energia):
        """Clasificar energía cósmica"""
        if energia > 0.8: return 'ALTA_COSMICA'
        if energia > 0.6: return 'ELEVADA_COSMICA'
        if energia > 0.4: return 'ESTABLE'
        if energia > 0.2: return 'BAJA_COSMICA'
        return 'MUY_BAJA_COSMICA'

    def ejecutar_meditacion_cosmica(self):
        """Ejecutar ciclo de monitorización"""
        try:
            logging.info("🧘‍♂️ INICIANDO MEDITACIÓN CÓSMICA")

            energia_cosmica = self.medir_energia_cosmica()
            logging.info(f"🌠 Energía cósmica: {energia_cosmica['nivel_energia']}")

            sismos = self.monitor_sismico.buscar_sismos_golfo_cadiz_cosmicos(dias=3)
            logging.info(f"🌍 Sismos cósmicos: {len(sismos)}")

            boyas = self.monitor_boyas.obtener_datos_boyas_cosmicas()
            estado_boyas = self.monitor_boyas.verificar_estado_boyas()
            logging.info(f"🌊 Boyas operativas: {estado_boyas['boyas_operativas']}")

            fase_lunar = self.calculador_lunar.calcular_fase_lunar(datetime.now())
            logging.info(f"🌙 Fase lunar: {fase_lunar['nombre_fase']}")

            analisis = self._analisis_cosmico(energia_cosmica, sismos, boyas, fase_lunar)
            self._generar_alertas(analisis)

            logging.info("✅ MEDITACIÓN COMPLETADA")
            return True

        except Exception as e:
            logging.error(f"💥 Error en meditación: {e}")
            return False

    def _analisis_cosmico(self, energia, sismos, boyas, fase_lunar):
        """Análisis cósmico"""
        riesgo = 0.0

        for sismo in sismos:
            if sismo['magnitud'] > 5.0:
                riesgo += 0.3
            elif sismo['magnitud'] > 4.0:
                riesgo += 0.15

        if fase_lunar['nombre_fase'] in ['Luna Llena', 'Luna Nueva']:
            riesgo += 0.1

        return {
            'riesgo_total': min(riesgo, 1.0),
            'nivel_alerta': self._determinar_nivel_alerta(riesgo),
            'energia_cosmica': energia,
            'total_sismos': len(sismos),
            'boyas_operativas': len([b for b in boyas if b['estado'] == 'OPERATIVA']),
            'fase_lunar': fase_lunar['nombre_fase']
        }

    def _determinar_nivel_alerta(self, riesgo):
        """Determinar nivel de alerta"""
        if riesgo > 0.7: return 'ALERTA_CÓSMICA_MAXIMA'
        if riesgo > 0.5: return 'ALERTA_CÓSMICA'
        if riesgo > 0.3: return 'VIGILANCIA_CÓSMICA'
        if riesgo > 0.1: return 'OBSERVACIÓN_CÓSMICA'
        return 'TRANQUILO_CÓSMICO'

    def _generar_alertas(self, analisis):
        """Generar alertas"""
        if analisis['riesgo_total'] > 0.5:
            logging.warning(f"🌌 ALERTA {analisis['nivel_alerta']} - Riesgo: {analisis['riesgo_total']:.2f}")

    def ejecutar_continuamente(self):
        """Ejecución continua"""
        logging.info("🚀 INICIANDO EJECUCIÓN CONTINUA")

        ciclo = 0
        while True:
            try:
                ciclo += 1
                logging.info(f"🔄 CICLO #{ciclo}")

                self.ejecutar_meditacion_cosmica()
                time.sleep(300)  # 5 minutos

            except KeyboardInterrupt:
                logging.info("⏹️ SISTEMA DETENIDO POR EL MAESTRO")
                break
            except Exception as e:
                logging.error(f"🔧 Error no crítico: {e}")
                time.sleep(60)

if __name__ == "__main__":
    sistema = SistemaCosmicoCompleto()
    sistema.ejecutar_continuamente()
