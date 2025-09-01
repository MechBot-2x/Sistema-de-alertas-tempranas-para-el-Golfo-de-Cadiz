#!/usr/bin/env python3
"""
🎯 SISTEMA PRINCIPAL MEJORADO - Funciona incluso sin AEMET
"""

import time
import logging
from datetime import datetime
from scripts.datos.aemet_client import MonitorAEMETGolfoCadiz
from scripts.monitoreo.sismico_cosmico import SismicMonitorCosmico
from scripts.monitoreo.boyas_avanzadas_2025 import BoyasAvanzadas2025

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SistemaResiliente:
    """Sistema que funciona incluso cuando las APIs fallan"""

    def __init__(self):
        self.estado = "INICIANDO"
        self.monitor_aemet = MonitorAEMETGolfoCadiz()
        self.monitor_sismico = SismicMonitorCosmico()
        self.monitor_boyas = BoyasAvanzadas2025()

        logging.info("🚀 INICIANDO SISTEMA RESILIENTE")
        logging.info("🌊 Monitorización del Golfo de Cádiz - Siempre activa")

    def ejecutar_ciclo_inteligente(self):
        """Ciclo de monitorización inteligente"""
        try:
            logging.info("🔄 EJECUTANDO CICLO INTELIGENTE")

            # 1. Datos meteorológicos (AEMET o simulados)
            datos_meteo = self.monitor_aemet.obtener_datos_completos_golfo()

            # 2. Datos sísmicos
            sismos = self.monitor_sismico.buscar_sismos_golfo_cadiz_cosmicos(dias=1)

            # 3. Datos de boyas
            boyas = self.monitor_boyas.obtener_datos_boyas_cosmicas()

            # 4. Análisis y alertas
            self._generar_alertas_inteligentes(datos_meteo, sismos, boyas)

            # 5. Mostrar estado del sistema
            self._mostrar_estado_sistema(datos_meteo, sismos, boyas)

            logging.info("✅ CICLO COMPLETADO")
            return True

        except Exception as e:
            logging.error(f"💥 Error en ciclo: {e}")
            return False

    def _generar_alertas_inteligentes(self, meteo, sismos, boyas):
        """Generar alertas basadas en todos los datos disponibles"""
        alertas = []

        # Alertas meteorológicas
        if 'alertas' in meteo:
            alertas.extend(meteo['alertas'])

        # Alertas sísmicas
        for sismo in sismos:
            if sismo['magnitud'] > 4.0:
                alertas.append(f"🌍 Sismo M{sismo['magnitud']} en {sismo['lugar']}")

        # Alertas de boyas
        for boya in boyas:
            if boya.get('altura_ola', 0) > 2.5:
                alertas.append(f"🌊 Ola alta {boya['altura_ola']}m en {boya['nombre']}")

        # Mostrar alertas si las hay
        if alertas:
            for alerta in alertas:
                logging.warning(f"⚠️ {alerta}")
        else:
            logging.info("✅ Sin alertas - Condiciones normales")

    def _mostrar_estado_sistema(self, meteo, sismos, boyas):
        """Mostrar estado resumido del sistema"""
        print("\n" + "="*50)
        print("🌊 ESTADO SISTEMA - Golfo de Cádiz")
        print("="*50)

        print(f"🌤️ Meteorología: {len(meteo.get('estaciones', {}))} estaciones")
        print(f"   Estado: {meteo.get('estado_conexion', 'DESCONOCIDO')}")

        print(f"🌍 Sismicidad: {len(sismos)} sismos (24h)")
        print(f"🌊 Boyas: {len(boyas)} boyas operativas")

        # Mostrar temperatura de Cádiz si disponible
        if 'cadiz' in meteo.get('estaciones', {}):
            temp = meteo['estaciones']['cadiz'].get('temperatura', 'N/A')
            print(f"📊 Temp Cádiz: {temp}°C")

        print(f"⏰ Última actualización: {datetime.now().strftime('%H:%M:%S')}")
        print("="*50 + "\n")

    def ejecutar_continuamente(self):
        """Ejecución continua del sistema resiliente"""
        logging.info("🔁 INICIANDO EJECUCIÓN CONTINUA")

        ciclo = 0
        while True:
            try:
                ciclo += 1
                print(f"\n🔄 CICLO #{ciclo} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                self.ejecutar_ciclo_inteligente()

                # Esperar entre ciclos (5 minutos)
                time.sleep(300)

            except KeyboardInterrupt:
                print("\n⏹️ SISTEMA DETENIDO POR EL USUARIO")
                break
            except Exception as e:
                print(f"🔧 Error no crítico: {e}")
                time.sleep(60)  # Reintentar en 1 minuto

if __name__ == "__main__":
    # Probamos la conexión primero
    from scripts.datos.aemet_client import probar_conexion_aemet
    probar_conexion_aemet()

    print("\n" + "="*50)
    print("🚀 INICIANDO SISTEMA DE MONITORIZACIÓN")
    print("="*50)

    # Iniciar sistema
    sistema = SistemaResiliente()
    sistema.ejecutar_continuamente()
