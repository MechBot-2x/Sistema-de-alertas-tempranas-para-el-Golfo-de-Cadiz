#!/usr/bin/env python3
"""
🌌 SISTEMA CÓSMICO AVANZADO - Monitorización con energía cósmica y boyas 2025
Sistema de alertas tempranas con conciencia cósmica
"""

import time
import logging
from datetime import datetime
from scripts.monitoreo.sismico_cosmico import SismicMonitorCosmico
from scripts.monitoreo.boyas_avanzadas_2025 import BoyasAvanzadas2025
from scripts.monitoreo.influencia_lunar import LunarInfluenceCalculator

# Configurar logging cósmico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - 🌌 %(message)s',
    handlers=[
        logging.FileHandler('logs/sistema_cosmico.log'),
        logging.StreamHandler()
    ]
)

class SistemaCosmicoAvanzado:
    """Sistema de monitorización con conciencia cósmica"""

    def __init__(self):
        self.estado = "OPERATIVO_COSMICO"
        self.monitor_sismico = SismicMonitorCosmico()
        self.monitor_boyas = BoyasAvanzadas2025()
        self.calculador_lunar = LunarInfluenceCalculator()

        logging.info("🌠 INICIANDO SISTEMA CÓSMICO AVANZADO")
        logging.info("✨ Conectando con las energías del Golfo de Cádiz")
        logging.info("🔭 Sintonizando con boyas inteligentes 2025")

    def medir_energia_cosmica(self):
        """Medir la energía cósmica actual"""
        try:
            from datetime import datetime
            import math

            ahora = datetime.now()
            dia_anio = ahora.timetuple().tm_yday
            hora_dia = ahora.hour + ahora.minute/60

            # Cálculo de energía cósmica basado en múltiples factores
            energia = (
                math.sin(dia_anio / 365 * 2 * math.pi) * 0.4 +
                math.cos(hora_dia / 24 * 4 * math.pi) * 0.3 +
                (datetime.now().day / 31) * 0.3
            )

            energia_normalizada = (energia + 1) / 2  # Normalizar a 0-1

            return {
                'nivel_energia': round(energia_normalizada, 3),
                'estado': self._clasificar_energia_cosmica(energia_normalizada),
                'timestamp': ahora.isoformat()
            }

        except Exception as e:
            logging.error(f"❌ Error medición cósmica: {e}")
            return {'nivel_energia': 0.5, 'estado': 'ESTABLE', 'timestamp': datetime.now().isoformat()}

    def _clasificar_energia_cosmica(self, energia):
        """Clasificar el estado de energía cósmica"""
        if energia > 0.8: return 'ALTA_COSMICA'
        if energia > 0.6: return 'ELEVADA_COSMICA'
        if energia > 0.4: return 'ESTABLE'
        if energia > 0.2: return 'BAJA_COSMICA'
        return 'MUY_BAJA_COSMICA'

    def ejecutar_meditacion_cosmica(self):
        """Ejecutar ciclo completo de monitorización cósmica"""
        try:
            logging.info("🧘‍♂️ INICIANDO MEDITACIÓN CÓSMICA")

            # 1. Medir energía cósmica base
            energia_cosmica = self.medir_energia_cosmica()
            logging.info(f"🌠 Energía cósmica: {energia_cosmica['nivel_energia']} ({energia_cosmica['estado']})")

            # 2. Monitorizar sismos cósmicos
            sismos = self.monitor_sismico.buscar_sismos_golfo_cadiz_cosmicos(dias=3)
            logging.info(f"🌍 Sismos cósmicos detectados: {len(sismos)}")

            # 3. Conectar con boyas inteligentes 2025
            boyas = self.monitor_boyas.obtener_datos_boyas_cosmicas()
            estado_boyas = self.monitor_boyas.verificar_estado_boyas()
            logging.info(f"🌊 Boyas cósmicas: {estado_boyas['boyas_operativas']}/{estado_boyas['total_boyas']}")

            # 4. Calcular influencia lunar
            fase_lunar = self.calculador_lunar.calcular_fase_lunar(datetime.now())
            logging.info(f"🌙 Fase lunar: {fase_lunar['nombre_fase']}")

            # 5. Análisis cósmico completo
            analisis = self._analisis_cosmico_completo(
                energia_cosmica, sismos, boyas, fase_lunar
            )

            # 6. Generar alertas cósmicas
            self._generar_alertas_cosmicas(analisis)

            logging.info("✅ MEDITACIÓN CÓSMICA COMPLETADA")
            return True

        except Exception as e:
            logging.error(f"💥 Error en meditación cósmica: {e}")
            return False

    def _analisis_cosmico_completo(self, energia, sismos, boyas, fase_lunar):
        """Análisis cósmico completo"""
        try:
            # Calcular riesgo cósmico integrado
            riesgo = self._calcular_riesgo_cosmico(energia, sismos, boyas, fase_lunar)

            return {
                'riesgo_total': riesgo,
                'nivel_alerta': self._determinar_nivel_alerta_cosmico(riesgo),
                'timestamp': datetime.now().isoformat(),
                'energia_cosmica': energia,
                'total_sismos': len(sismos),
                'sismos_fuertes': sum(1 for s in sismos if s['magnitud'] > 4.0),
                'boyas_operativas': len(boyas),
                'fase_lunar': fase_lunar['nombre_fase'],
                'mensaje_cosmico': self._generar_mensaje_cosmico(riesgo, fase_lunar)
            }

        except Exception as e:
            logging.error(f"❌ Error análisis cósmico: {e}")
            return {'riesgo_total': 0.0, 'nivel_alerta': 'TRANQUILO', 'mensaje_cosmico': 'Sistema en calma'}

    def _calcular_riesgo_cosmico(self, energia, sismos, boyas, fase_lunar):
        """Calcular riesgo cósmico integrado"""
        riesgo = 0.0

        # Factor de energía cósmica
        if energia['estado'] in ['ALTA_COSMICA', 'MUY_BAJA_COSMICA']:
            riesgo += 0.2

        # Factor sísmico
        for sismo in sismos:
            if sismo['magnitud'] > 5.0:
                riesgo += 0.3
            elif sismo['magnitud'] > 4.0:
                riesgo += 0.15

        # Factor de fase lunar (Luna llena o nueva)
        if fase_lunar['nombre_fase'] in ['Luna Llena', 'Luna Nueva']:
            riesgo += 0.1

        return min(riesgo, 1.0)

    def _determinar_nivel_alerta_cosmico(self, riesgo):
        """Determinar nivel de alerta cósmico"""
        if riesgo > 0.7: return 'ALERTA_CÓSMICA_MAXIMA'
        if riesgo > 0.5: return 'ALERTA_CÓSMICA'
        if riesgo > 0.3: return 'VIGILANCIA_CÓSMICA'
        if riesgo > 0.1: return 'OBSERVACIÓN_CÓSMICA'
        return 'TRANQUILO_CÓSMICO'

    def _generar_mensaje_cosmico(self, riesgo, fase_lunar):
        """Generar mensaje cósmico personalizado"""
        mensajes = {
            'ALERTA_CÓSMICA_MAXIMA': '🚨 Las energías están intensas. Mantén la calma y la conciencia.',
            'ALERTA_CÓSMICA': '⚠️ Flujos cósmicos activos. Permanece atento a las señales.',
            'VIGILANCIA_CÓSMICA': '👀 Energías en movimiento. Observa con atención.',
            'OBSERVACIÓN_CÓSMICA': '🔍 Flujos sutiles detectados. Continúa tu práctica.',
            'TRANQUILO_CÓSMICO': '☮️ Paz cósmica. Las energías fluyen en armonía.'
        }

        nivel = self._determinar_nivel_alerta_cosmico(riesgo)
        return f"{mensajes.get(nivel, 'Estado de paz cósmica')} Fase lunar: {fase_lunar['nombre_fase']}"

    def _generar_alertas_cosmicas(self, analisis):
        """Generar alertas basadas en análisis cósmico"""
        if analisis['riesgo_total'] > 0.5:
            alerta = (f"🌌 ALERTA CÓSMICA {analisis['nivel_alerta']}\n"
                     f"📊 Riesgo: {analisis['riesgo_total']:.2f}\n"
                     f"🌍 Sismos: {analisis['total_sismos']} ({analisis['sismos_fuertes']} fuertes)\n"
                     f"💫 {analisis['mensaje_cosmico']}")

            logging.warning(alerta)

            # Aquí se integraría con Telegram en el futuro
            # self._enviar_alerta_telegram(alerta)

    def ejecutar_continuamente(self):
        """Ejecución continua del sistema cósmico"""
        logging.info("🚀 INICIANDO EJECUCIÓN CÓSMICA CONTINUA")
        logging.info("🔄 El sistema meditará cada 10 minutos")

        ciclo = 0
        while True:
            try:
                ciclo += 1
                logging.info(f"🔄 CICLO CÓSMICO #{ciclo}")

                self.ejecutar_meditacion_cosmica()

                # Meditar cada 10 minutos
                time.sleep(600)

            except KeyboardInterrupt:
                logging.info("⏹️ MEDITACIÓN CÓSMICA FINALIZADA POR EL MAESTRO")
                break
            except Exception as e:
                logging.error(f"🔧 Error no crítico en meditación: {e}")
                time.sleep(300)  # Reintentar en 5 minutos

if __name__ == "__main__":
    # Iniciar sistema cósmico
    sistema = SistemaCosmicoAvanzado()

    # Ejecutar meditación inicial
    sistema.ejecutar_meditacion_cosmica()

    # Iniciar ejecución continua
    sistema.ejecutar_continuamente()
