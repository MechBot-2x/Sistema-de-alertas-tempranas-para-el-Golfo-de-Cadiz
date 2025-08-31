#!/usr/bin/env python3
"""
📱 SISTEMA OPTIMIZADO MÓVIL - Para conexiones variables
"""

import time
import requests
from sistema_completo_telegram import SistemaCompleto

class SistemaMovilOptimizado(SistemaCompleto):
    def __init__(self):
        super().__init__()
        self.timeout = 15  # Timeout más corto para móviles
        self.max_reintentos = 2
        self.intervalo_principal = 45  # 45 segundos entre ciclos
    
    def obtener_conexion_segura(self, url, tipo="aemet"):
        """Conexión optimizada para móviles"""
        for intento in range(self.max_reintentos):
            try:
                response = requests.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    return response
                print(f"⚠️ Intento {intento+1}: HTTP {response.status_code}")
            except Exception as e:
                print(f"❌ Intento {intento+1}: {type(e).__name__}")
            
            time.sleep(3)  # Espera entre intentos
        
        raise Exception(f"No se pudo conectar después de {self.max_reintentos} intentos")
    
    def ejecutar_ciclo_optimizado(self):
        """Ciclo optimizado para móviles"""
        try:
            # Intentar obtener datos reales
            try:
                url = f"{self.base_url}/observacion/convencional/datos/estacion/5980?api_key={self.api_key}"
                response = self.obtener_conexion_segura(url)
                datos_meteo = self._procesar_datos_reales(response.json())
                fuente = "AEMET_REAL"
            except:
                # Fallback a simulación
                datos_meteo = self._datos_simulados_mejorados()
                fuente = "AEMET_SIMULADO"
            
            # Datos oceánicos (siempre disponibles)
            datos_oceano = self.datos_oceanicos()
            
            # Generar y enviar alertas
            alertas = self.generar_alertas(datos_meteo, datos_oceano)
            self.verificar_y_alertar(datos_meteo, datos_oceano, alertas)
            
            # Mostrar dashboard
            self.mostrar_dashboard_oficial(datos_meteo, datos_oceano, alertas, fuente)
            
            return True
            
        except Exception as e:
            print(f"💥 Error grave: {e}")
            return False
    
    def iniciar_servicio_movil(self):
        """Iniciar servicio optimizado para móviles"""
        print("📱 INICIANDO SISTEMA MÓVIL OPTIMIZADO")
        print("🌊 Golfo de Cádiz - Monitorización inteligente")
        print("⏰ Intervalo: 45 segundos | 📡 Timeout: 15 segundos")
        
        # Mensaje de inicio por Telegram
        try:
            self.enviar_telegram(
                "📱 <b>SISTEMA MÓVIL ACTIVADO</b>\n"
                "🌊 Monitorización Golfo de Cádiz\n"
                "✅ Optimizado para conexiones variables\n"
                f"⏰ {time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
        except:
            print("⚠️ No se pudo enviar mensaje de inicio")
        
        ciclo = 0
        try:
            while True:
                ciclo += 1
                print(f"\n🔄 CICLO MÓVIL {ciclo}")
                
                if self.ejecutar_ciclo_optimizado():
                    time.sleep(self.intervalo_principal)
                else:
                    print("⚠️ Reintentando en 10 segundos...")
                    time.sleep(10)
                    
        except KeyboardInterrupt:
            print("\n🛑 SISTEMA MÓVIL DETENIDO")
            # Mensaje de despedida
            try:
                self.enviar_telegram(
                    "🛑 <b>SISTEMA MÓVIL DETENIDO</b>\n"
                    f"📊 Ciclos completados: {ciclo}\n"
                    f"⏰ {time.strftime('%Y-%m-%d %H:%M:%S')}"
                )
            except:
                pass

if __name__ == "__main__":
    sistema = SistemaMovilOptimizado()
    sistema.iniciar_servicio_movil()
