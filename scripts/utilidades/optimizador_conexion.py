#!/usr/bin/env python3
"""
⚡ OPTIMIZADOR DE CONEXIÓN - Para redes lentas
"""

import requests
import time
import logging
from functools import wraps

def retry_on_failure(max_retries=3, delay=2, backoff=2):
    """Decorator para reintentar conexiones fallidas"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (requests.ConnectionError, requests.Timeout) as e:
                    retries += 1
                    if retries >= max_retries:
                        logging.error(f"❌ Máximo de reintentos alcanzado para {func.__name__}")
                        raise

                    wait_time = delay * (backoff ** (retries - 1))
                    logging.warning(f"⚠️ Reintento {retries}/{max_retries} para {func.__name__} en {wait_time}s")
                    time.sleep(wait_time)

        return wrapper
    return decorator

class ConexionOptimizada:
    """Clase para optimizar conexiones lentas"""

    def __init__(self):
        self.timeout = 20  # Timeout más generoso
        self.session = requests.Session()

        # Configurar session para mejor performance
        self.session.headers.update({
            'User-Agent': 'SistemaAlertasGolfoCadiz/1.0',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })

    @retry_on_failure(max_retries=3, delay=2, backoff=2)
    def get_optimizado(self, url, **kwargs):
        """GET optimizado para conexiones lentas"""
        kwargs.setdefault('timeout', self.timeout)
        return self.session.get(url, **kwargs)

    def descargar_json_optimizado(self, url):
        """Descargar JSON con optimizaciones"""
        try:
            response = self.get_optimizado(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"❌ Error descargando JSON: {e}")
            return None

# Uso recomendado en AEMET Client
def aemet_request_optimizada(endpoint, params=None):
    """Versión optimizada para AEMET"""
    conexion = ConexionOptimizada()
    url = f"https://opendata.aemet.es/opendata/api{endpoint}"

    try:
        response = conexion.get_optimizado(url, params=params)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logging.error(f"❌ Error en request optimizada: {e}")

    return None
