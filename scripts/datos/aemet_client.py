#!/usr/bin/env python3
"""
🌤️ CLIENTE AEMET OPENDATA - Conexión robusta e inteligente
Sistema que funciona incluso cuando AEMET está lento/caído
"""

import requests
import json
import logging
from datetime import datetime, timedelta
import os
import time
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class AEMETClientRobusto:
    """Cliente robusto para AEMET OpenData con sistema de fallback"""
    
    def __init__(self):
        self.api_key = os.getenv('AEMET_API_KEY', 'opcional')
        self.base_url = "https://opendata.aemet.es/opendata/api"
        self.headers = {
            'accept': 'application/json',
            'api_key': self.api_key
        }
        self.ultima_conexion_exitosa = None
        self.estado_conexion = "DESCONOCIDO"
        
        logging.info("🌤️ Iniciando Cliente AEMET Robusto")
    
    def _request_inteligente(self, endpoint, params=None, max_intentos=3):
        """Request inteligente con reintentos y timeout adaptativo"""
        intentos = 0
        timeout_base = 10  # timeout base en segundos
        
        while intentos < max_intentos:
            try:
                url = f"{self.base_url}{endpoint}"
                
                # Timeout adaptativo: aumenta con cada intento
                timeout_actual = timeout_base * (intentos + 1)
                
                response = requests.get(
                    url, 
                    headers=self.headers, 
                    params=params, 
                    timeout=timeout_actual
                )
                
                if response.status_code == 200:
                    self.ultima_conexion_exitosa = datetime.now()
                    self.estado_conexion = "CONECTADO"
                    return response.json()
                
                elif response.status_code == 401:
                    logging.error("❌ API Key de AEMET inválida")
                    return None
                    
                elif response.status_code == 429:
                    logging.warning("⚠️ Demasiadas requests a AEMET, esperando...")
                    time.sleep(30)  # Esperar 30 segundos por rate limiting
                    intentos += 1
                    continue
                    
                else:
                    logging.warning(f"⚠️ HTTP {response.status_code}, reintentando...")
                    intentos += 1
                    time.sleep(5)
                    
            except requests.Timeout:
                logging.warning(f"⏰ Timeout en intento {intentos + 1}, reintentando...")
                intentos += 1
                time.sleep(5)
                
            except requests.ConnectionError:
                logging.warning("🌐 Error de conexión, reintentando...")
                intentos += 1
                time.sleep(10)
                
            except Exception as e:
                logging.error(f"❌ Error inesperado: {e}")
                intentos += 1
                time.sleep(5)
        
        self.estado_conexion = "DESCONECTADO"
        logging.error("❌ Máximo de intentos alcanzado")
        return None
    
    def obtener_datos_estacion(self, codigo_estacion):
        """Obtener datos de estación con fallback inteligente"""
        endpoint = f"/observacion/convencional/datos/estacion/{codigo_estacion}"
        datos = self._request_inteligente(endpoint)
        
        if datos:
            return self._procesar_datos_estacion(datos)
        else:
            return self._datos_estacion_simulados(codigo_estacion)
    
    def _procesar_datos_estacion(self, datos):
        """Procesar datos de estación AEMET"""
        try:
            # AEMET devuelve una URL con los datos reales
            if isinstance(datos, dict) and 'datos' in datos:
                url_datos = datos['datos']
                response = requests.get(url_datos, timeout=15)
                if response.status_code == 200:
                    datos_reales = response.json()
                    return self._formatear_datos_estacion(datos_reales)
            
            return datos
            
        except Exception as e:
            logging.error(f"❌ Error procesando datos estación: {e}")
            return None
    
    def _formatear_datos_estacion(self, datos_estacion):
        """Formatear datos de estación para nuestro sistema"""
        if isinstance(datos_estacion, list) and len(datos_estacion) > 0:
            ultimo_dato = datos_estacion[0]  # El más reciente
            
            return {
                'temperatura': ultimo_dato.get('ta', None),  # Temperatura ambiente
                'humedad': ultimo_dato.get('hr', None),      # Humedad relativa
                'presion': ultimo_dato.get('pres', None),    # Presión atmosférica
                'viento_velocidad': ultimo_dato.get('vv', None),  # Velocidad viento
                'viento_direccion': ultimo_dato.get('dv', None),  # Dirección viento
                'precipitacion': ultimo_dato.get('prec', None),   # Precipitación
                'timestamp': datetime.now().isoformat(),
                'fuente': 'AEMET_REAL'
            }
        
        return None
    
    def _datos_estacion_simulados(self, codigo_estacion):
        """Generar datos simulados cuando AEMET no responde"""
        # Datos basados en estaciones reales del Golfo de Cádiz
        datos_por_estacion = {
            '5783': {'temperatura': 22.5, 'humedad': 65, 'viento_velocidad': 15.3},  # Cádiz
            '5675': {'temperatura': 24.1, 'humedad': 60, 'viento_velocidad': 12.8},  # Jerez
            '6000': {'temperatura': 21.8, 'humedad': 70, 'viento_velocidad': 18.2},  # Tarifa
            '5785': {'temperatura': 23.2, 'humedad': 62, 'viento_velocidad': 14.1},  # Huelva
        }
        
        datos_base = datos_por_estacion.get(codigo_estacion, {
            'temperatura': 22.0, 
            'humedad': 65, 
            'viento_velocidad': 15.0
        })
        
        # Añadir variabilidad natural
        import random
        return {
            'temperatura': round(datos_base['temperatura'] + random.uniform(-2, 2), 1),
            'humedad': max(40, min(90, datos_base['humedad'] + random.randint(-10, 10))),
            'viento_velocidad': max(0, datos_base['viento_velocidad'] + random.uniform(-5, 5)),
            'presion': 1013 + random.randint(-10, 10),
            'timestamp': datetime.now().isoformat(),
            'fuente': 'AEMET_SIMULADO',
            'estado': 'MODO_SIMULACION'
        }
    
    def verificar_conexion(self):
        """Verificar el estado de la conexión AEMET"""
        test_endpoint = "/valores/climatologicos/inventarioestaciones/todasestaciones"
        
        inicio = datetime.now()
        resultado = self._request_inteligente(test_endpoint, max_intentos=2)
        duracion = (datetime.now() - inicio).total_seconds()
        
        if resultado:
            logging.info(f"✅ AEMET Conectado (respuesta en {duracion:.1f}s)")
            return True
        else:
            logging.warning(f"❌ AEMET No disponible (timeout después de {duracion:.1f}s)")
            return False

# Configuración específica para el Golfo de Cádiz
ESTACIONES_GOLFO_CADIZ = {
    'cadiz': '5783',      # Estación Cádiz
    'jerez': '5675',      # Estación Jerez de la Frontera
    'tarifa': '6000',     # Estación Tarifa
    'huelva': '5785',     # Estación Huelva
    'chipiona': '5674',   # Estación Chipiona
    'barbate': '6001',    # Estación Barbate
}

class MonitorAEMETGolfoCadiz:
    """Monitor especializado para el Golfo de Cádiz"""
    
    def __init__(self):
        self.client = AEMETClientRobusto()
        self.estaciones = ESTACIONES_GOLFO_CADIZ
        
    def obtener_datos_completos_golfo(self):
        """Obtener datos meteorológicos de todo el Golfo de Cádiz"""
        datos_completos = {
            'timestamp': datetime.now().isoformat(),
            'estaciones': {},
            'estado_conexion': self.client.estado_conexion
        }
        
        for nombre, codigo in self.estaciones.items():
            try:
                datos_estacion = self.client.obtener_datos_estacion(codigo)
                if datos_estacion:
                    datos_completos['estaciones'][nombre] = datos_estacion
                    
                    logging.info(f"🌤️ Datos de {nombre} obtenidos")
                else:
                    logging.warning(f"⚠️ No se pudieron obtener datos de {nombre}")
                    
            except Exception as e:
                logging.error(f"❌ Error obteniendo datos de {nombre}: {e}")
        
        return datos_completos
    
    def obtener_resumen_alertas(self):
        """Generar resumen para alertas del sistema"""
        datos = self.obtener_datos_completos_golfo()
        alertas = []
        
        for nombre, datos_estacion in datos['estaciones'].items():
            # Verificar condiciones para alertas
            if datos_estacion.get('viento_velocidad', 0) > 50:  # km/h
                alertas.append(f"🌬️ Viento fuerte en {nombre}: {datos_estacion['viento_velocidad']} km/h")
            
            if datos_estacion.get('temperatura', 0) > 35:
                alertas.append(f"🌡️ Temperatura alta en {nombre}: {datos_estacion['temperatura']}°C")
        
        return {
            'total_estaciones': len(datos['estaciones']),
            'alertas': alertas,
            'timestamp': datos['timestamp'],
            'conexion': datos['estado_conexion']
        }

# Función de prueba simplificada
def probar_conexion_aemet():
    """Función simple para probar la conexión AEMET"""
    print("=== 🔍 PRUEBA CONEXIÓN AEMET ===")
    
    client = AEMETClientRobusto()
    
    # Verificar conexión
    if client.verificar_conexion():
        print("✅ Conexión AEMET exitosa")
        
        # Probar con una estación
        datos = client.obtener_datos_estacion('5783')  # Cádiz
        if datos:
            print(f"✅ Datos de Cádiz: {datos['temperatura']}°C, {datos['viento_velocidad']} km/h")
            print(f"   Fuente: {datos['fuente']}")
        else:
            print("❌ No se pudieron obtener datos")
    else:
        print("❌ AEMET no disponible - Modo simulación activado")
        
        # Mostrar datos simulados
        datos_simulados = client._datos_estacion_simulados('5783')
        print(f"🌤️ Datos simulados: {datos_simulados['temperatura']}°C")
        print("   El sistema continúa funcionando con datos simulados")

if __name__ == "__main__":
    probar_conexion_aemet()
