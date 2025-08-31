#!/usr/bin/env python3
"""
🎯 SISTEMA OPTIMIZADO FINAL - Golfo de Cádiz
Usando solo las APIs que ya tenemos funcionando
"""

import time
import logging
from datetime import datetime
from scripts.datos.copernicus_simple import CopernicusSimpleClient
from scripts.datos.aemet_client import MonitorAEMETGolfoCadiz
from scripts.alertas.telegram_advanced import NotificadorAvanzado

# Configurar logging optimizado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('sistema_alertas.log', encoding='utf-8')
    ]
)

class SistemaOptimizadoFinal:
    """Sistema final optimizado con lo que funciona"""
    
    def __init__(self):
        self.client_copernicus = CopernicusSimpleClient()
        self.client_aemet = MonitorAEMETGolfoCadiz()
        self.notificador = NotificadorAvanzado()
        
        logging.info("🚀 SISTEMA OPTIMIZADO INICIADO")
        logging.info("📍 Golfo de Cádiz - Alertas Tempranas")
        logging.info("✅ Usando APIs confirmadas: AEMET + Copernicus + Telegram")
    
    def obtener_datos_combinados(self):
        """Obtener datos de todas las fuentes disponibles"""
        try:
            # Datos de Copernicus (siempre disponible)
            datos_copernicus = self.client_copernicus.obtener_datos_golfo_cadiz()
            
            # Intentar datos AEMET (puede fallar a veces)
            try:
                datos_aemet = self.client_aemet.obtener_datos_actuales()
                fuente_aemet = "AEMET_REAL"
            except Exception as e:
                logging.warning(f"⚠️ AEMET no disponible: {e}")
                datos_aemet = self.client_aemet._simular_datos()
                fuente_aemet = "AEMET_SIMULADO"
            
            # Combinar datos
            datos_combinados = {
                **datos_copernicus,
                'temperatura_aire': datos_aemet.get('temperatura', 20.0),
                'viento_velocidad': datos_aemet.get('viento_velocidad', 10.0),
                'viento_direccion': datos_aemet.get('viento_direccion', 'NE'),
                'humedad': datos_aemet.get('humedad', 70),
                'presion': datos_aemet.get('presion', 1015.0),
                'fuente_meteo': fuente_aemet,
                'fuente_oceano': datos_copernicus.get('fuente', 'COPERNICUS'),
                'timestamp': datetime.now().isoformat()
            }
            
            return datos_combinados
            
        except Exception as e:
            logging.error(f"💥 Error obteniendo datos combinados: {e}")
            return self._datos_emergencia()
    
    def _datos_emergencia(self):
        """Datos de emergencia si todo falla"""
        return {
            'temperatura_superficie': 19.5,
            'salinidad': 36.2,
            'nivel_mar': 0.1,
            'corriente_velocidad': 0.3,
            'corriente_direccion': 225,
            'oleaje_altura': 1.0,
            'oleaje_periodo': 6.0,
            'temperatura_aire': 20.0,
            'viento_velocidad': 10.0,
            'viento_direccion': 'NE',
            'humedad': 70,
            'presion': 1015.0,
            'fuente_meteo': 'EMERGENCIA',
            'fuente_oceano': 'EMERGENCIA',
            'timestamp': datetime.now().isoformat()
        }
    
    def analizar_riesgos(self, datos):
        """Análisis de riesgos optimizado"""
        alertas = []
        
        # Análisis oceánico
        if datos['oleaje_altura'] > 2.0:
            alertas.append('🌊 OLEAJE PELIGROSO')
        if datos['corriente_velocidad'] > 0.5:
            alertas.append('🌀 CORRIENTES FUERTES')
        
        # Análisis meteorológico
        if datos['viento_velocidad'] > 25.0:
            alertas.append('🌪️ VIENTOS FUERTES')
        if datos.get('precipitacion', 0) > 3.0:
            alertas.append('🌧️ LLUVIA INTENSA')
        
        return {
            'alertas': alertas,
            'riesgo_total': min(len(alertas) * 0.2, 1.0),
            'estado': 'ALERTA' if alertas else 'NORMAL'
        }
    
    def mostrar_dashboard_optimizado(self, datos, analisis):
        """Dashboard optimizado y claro"""
        print(f"\n{'='*60}")
        print(f"🌊 SISTEMA ALERTAS GOLFO CÁDIZ - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*60}")
        
        print(f"🌡️ AIRE: {datos['temperatura_aire']}°C | 💨 {datos['viento_velocidad']}km/h {datos['viento_direccion']}")
        print(f"💧 HUMEDAD: {datos['humedad']}% | 📊 PRESIÓN: {datos['presion']}hPa")
        
        print(f"🌊 AGUA: {datos['temperatura_superficie']}°C | 🧂 {datos['salinidad']}PSU")
        print(f"📈 NIVEL: {datos['nivel_mar']}m | 🌊 OLEAJE: {datos['oleaje_altura']}m")
        print(f"🌀 CORRIENTE: {datos['corriente_velocidad']}m/s → {datos['corriente_direccion']}°")
        
        print(f"\n🎯 ESTADO: {analisis['estado']} | 📊 RIESGO: {analisis['riesgo_total']:.0%}")
        print(f"📡 METEOROLOGÍA: {datos['fuente_meteo']}")
        print(f"📡 OCEANOGRAFÍA: {datos['fuente_oceano']}")
        
        if analisis['alertas']:
            print(f"\n🚨 ALERTAS ACTIVAS ({len(analisis['alertas'])}):")
            for alerta in analisis['alertas']:
                print(f"   ⚠️ {alerta}")
        
        print(f"{'='*60}")
    
    def enviar_alertas_si_corresponde(self, datos, analisis):
        """Enviar alertas solo si es necesario"""
        if analisis['alertas']:
            mensaje = f"🚨 ALERTA GOLFO CÁDIZ\n"
            mensaje += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            mensaje += f"📊 RIESGO: {analisis['riesgo_total']:.0%}\n\n"
            
            for alerta in analisis['alertas']:
                mensaje += f"⚠️ {alerta}\n"
            
            mensaje += f"\n🌡️ AIRE: {datos['temperatura_aire']}°C"
            mensaje += f" | 🌊 AGUA: {datos['temperatura_superficie']}°C"
            mensaje += f"\n💨 VIENTO: {datos['viento_velocidad']}km/h"
            mensaje += f" | 🌊 OLEAJE: {datos['oleaje_altura']}m"
            
            # Enviar por Telegram
            if self.notificador.enviar_telegram(mensaje):
                logging.info("✅ Alertas enviadas por Telegram")
    
    def ejecutar_ciclo_optimizado(self):
        """Ciclo optimizado de monitorización"""
        try:
            logging.info("🔄 EJECUTANDO CICLO OPTIMIZADO")
            
            # Obtener datos
            datos = self.obtener_datos_combinados()
            
            # Analizar riesgos
            analisis = self.analizar_riesgos(datos)
            
            # Mostrar información
            self.mostrar_dashboard_optimizado(datos, analisis)
            
            # Enviar alertas si es necesario
            self.enviar_alertas_si_corresponde(datos, analisis)
            
            logging.info("✅ CICLO OPTIMIZADO COMPLETADO")
            return True
            
        except Exception as e:
            logging.error(f"💥 Error en ciclo optimizado: {e}")
            return False
    
    def ejecutar_continuamente(self, intervalo_minutos=5):
        """Ejecutar continuamente"""
        logging.info(f"🔁 INICIANDO EJECUCIÓN CONTINUA ({intervalo_minutos}min)")
        
        ciclo = 0
        try:
            while True:
                ciclo += 1
                print(f"\n🔄 CICLO #{ciclo} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                if self.ejecutar_ciclo_optimizado():
                    time.sleep(intervalo_minutos * 60)
                else:
                    logging.warning("⚠️ Reintentando en 30 segundos...")
                    time.sleep(30)
                    
        except KeyboardInterrupt:
            print(f"\n🛑 SISTEMA DETENIDO - Ciclos completados: {ciclo}")
            logging.info("Sistema detenido manualmente por el usuario")

if __name__ == "__main__":
    sistema = SistemaOptimizadoFinal()
    sistema.ejecutar_continuamente(intervalo_minutos=3)
