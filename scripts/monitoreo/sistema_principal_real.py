#!/usr/bin/env python3
"""
🎯 SISTEMA PRINCIPAL CON DATOS REALES - Golfo de Cádiz
"""

import time
import logging
from datetime import datetime
from scripts.monitoreo.sismico_real import SismicMonitorReal
from scripts.monitoreo.datos_mareas_reales import MarineMonitorReal
from scripts.monitoreo.influencia_lunar import LunarInfluenceCalculator

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/sistema_real.log'),
        logging.StreamHandler()
    ]
)

class SistemaAlertasReales:
    """Sistema con datos reales y fallback a simulados"""

    def __init__(self):
        self.estado = "OPERATIVO"
        self.monitor_sismico = SismicMonitorReal()
        self.monitor_marino = MarineMonitorReal()
        self.calculador_lunar = LunarInfluenceCalculator()

        logging.info("🌊 Iniciando Sistema de Alertas con Datos Reales")

    def verificar_datos_reales(self):
        """Verificación con datos reales"""
        try:
            # 1. Verificar actividad sísmica real
            sismos = self.monitor_sismico.buscar_sismos_golfo_cadiz(dias=1)

            # 2. Verificar datos marinos reales
            boyas = self.monitor_marino.obtener_datos_boyas_reales()
            mareas = self.monitor_marino.obtener_datos_mareas_reales()

            # 3. Verificar influencia lunar
            fase_lunar = self.calculador_lunar.calcular_fase_lunar(datetime.now())

            # Determinar fuentes de datos
            fuentes = {
                'sismos': 'real' if any(s.get('lugar', '').find('Simulado') == -1 for s in sismos) else 'simulado',
                'boyas': 'real' if any(b.get('fuente') == 'real' for b in boyas) else 'simulado',
                'mareas': 'real' if mareas.get('cadiz', {}).get('fuente') == 'real' else 'simulado'
            }

            logging.info(f"✅ Datos obtenidos: {len(sismos)} sismos ({fuentes['sismos']}), "
                        f"{len(boyas)} boyas ({fuentes['boyas']})")

            return {
                'sismos': sismos,
                'boyas': boyas,
                'mareas': mareas,
                'fase_lunar': fase_lunar,
                'fuentes': fuentes,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logging.error(f"❌ Error verificando datos reales: {e}")
            return self._datos_fallback()

    def _datos_fallback(self):
        """Datos de fallback en caso de error"""
        from scripts.monitoreo.sismico_ign import SismicMonitor
        from scripts.monitoreo.datos_mareas import MarineMonitor

        monitor_simulado = SismicMonitor()
        monitor_marino_simulado = MarineMonitor()

        return {
            'sismos': monitor_simulado.buscar_sismos_golfo_cadiz(dias=1),
            'boyas': monitor_marino_simulado.obtener_datos_boyas(),
            'mareas': monitor_marino_simulado.obtener_datos_mareas(),
            'fase_lunar': self.calculador_lunar.calcular_fase_lunar(datetime.now()),
            'fuentes': {'sismos': 'simulado', 'boyas': 'simulado', 'mareas': 'simulado'},
            'timestamp': datetime.now().isoformat()
        }

    def analizar_riesgo_avanzado(self, datos):
        """Análisis de riesgo avanzado con datos reales"""
        try:
            riesgo = 0.0
            alertas = []

            # 1. Análisis sísmico
            for sismo in datos['sismos']:
                if sismo['magnitud'] > 6.0:
                    riesgo += 0.6
                    alertas.append(f"⚠️ Sismo fuerte: M{sismo['magnitud']}")
                elif sismo['magnitud'] > 5.0:
                    riesgo += 0.3
                    alertas.append(f"📢 Sismo moderado: M{sismo['magnitud']}")
                elif sismo['magnitud'] > 4.0:
                    riesgo += 0.1

            # 2. Análisis de condiciones marinas
            for boya in datos['boyas']:
                if boya.get('altura_ola', 0) > 3.0:
                    riesgo += 0.2
                    alertas.append(f"🌊 Ola alta: {boya['altura_ola']}m")

            # 3. Análisis de mareas
            if datos['mareas'].get('cadiz', {}).get('coeficiente', 0) > 90:
                riesgo += 0.1

            riesgo = min(riesgo, 1.0)

            return {
                'riesgo': riesgo,
                'alertas': alertas,
                'nivel': self._determinar_nivel_alerta(riesgo)
            }

        except Exception as e:
            logging.error(f"❌ Error analizando riesgo: {e}")
            return {'riesgo': 0.0, 'alertas': [], 'nivel': 'BAJO'}

    def _determinar_nivel_alerta(self, riesgo):
        """Determinar nivel de alerta basado en riesgo"""
        if riesgo > 0.7:
            return 'ALTO'
        elif riesgo > 0.4:
            return 'MODERADO'
        elif riesgo > 0.2:
            return 'BAJO'
        else:
            return 'NORMAL'

    def ejecutar_ciclo_monitorizacion(self):
        """Ciclo completo de monitorización con datos reales"""
        try:
            logging.info("🔄 Ejecutando ciclo avanzado con datos reales")

            # Obtener datos reales
            datos_reales = self.verificar_datos_reales()

            if datos_reales:
                # Analizar riesgo
                analisis_riesgo = self.analizar_riesgo_avanzado(datos_reales)

                # Log información detallada
                logging.info(f"📊 Riesgo: {analisis_riesgo['riesgo']:.2f} "
                            f"| Nivel: {analisis_riesgo['nivel']}")

                # Mostrar alertas si las hay
                for alerta in analisis_riesgo['alertas']:
                    logging.warning(alerta)

                # Enviar alerta si es necesario
                if analisis_riesgo['riesgo'] > 0.6:
                    mensaje = (f"🚨 ALERTA {analisis_riesgo['nivel']}: "
                              f"Riesgo {analisis_riesgo['riesgo']:.2f}\n"
                              f"📋 Alertas: {len(analisis_riesgo['alertas'])}")
                    logging.warning(mensaje)

                return True

        except Exception as e:
            logging.error(f"💥 Error crítico en ciclo: {e}")
            return False

    def ejecutar_continuamente(self):
        """Ejecución continua del sistema"""
        logging.info("🚀 Iniciando ejecución continua con datos reales")

        ciclo = 0
        while True:
            try:
                ciclo += 1
                logging.info(f"🔁 Ciclo #{ciclo}")

                self.ejecutar_ciclo_monitorizacion()
                time.sleep(300)  # Esperar 5 minutos entre ciclos

            except KeyboardInterrupt:
                logging.info("⏹️ Sistema detenido por el usuario")
                break
            except Exception as e:
                logging.error(f"🔧 Error no crítico: {e}")
                time.sleep(60)

if __name__ == "__main__":
    sistema = SistemaAlertasReales()
    sistema.ejecutar_continuamente()
