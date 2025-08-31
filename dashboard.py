#!/usr/bin/env python3
"""
📊 DASHBOARD DEL SISTEMA DE ALERTA TEMPRANA
Visualización simple de datos y alertas
"""

import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd

def mostrar_estadisticas():
    """Mostrar estadísticas del sistema"""
    conn = sqlite3.connect('alertas_vidas.db')
    
    print("🌊 DASHBOARD - SISTEMA DE ALERTA TEMPRANA")
    print("=" * 50)
    
    # Estadísticas generales
    total_registros = conn.execute("SELECT COUNT(*) FROM datos_solares").fetchone()[0]
    total_alertas = conn.execute("SELECT COUNT(*) FROM alertas").fetchone()[0]
    
    print(f"📈 Total de registros: {total_registros}")
    print(f"🚨 Total de alertas: {total_alertas}")
    
    # Alertas por nivel
    print("\n📊 Alertas por nivel:")
    alertas_nivel = conn.execute("SELECT nivel, COUNT(*) FROM alertas GROUP BY nivel").fetchall()
    for nivel, cantidad in alertas_nivel:
        print(f"   {nivel}: {cantidad}")
    
    # Últimos registros
    print("\n🕒 Últimos registros:")
    ultimos = conn.execute("""
        SELECT fecha, llamaradas_m, llamaradas_x, indice_kp 
        FROM datos_solares 
        ORDER BY id DESC LIMIT 5
    """).fetchall()
    
    for fecha, m, x, kp in ultimos:
        fecha_str = datetime.fromisoformat(fecha).strftime('%d/%m %H:%M')
        print(f"   {fecha_str}: M={m}, X={x}, Kp={kp}")
    
    conn.close()

def graficar_datos():
    """Crear gráficos de los datos"""
    conn = sqlite3.connect('alertas_vidas.db')
    
    # Obtener datos de las últimas 24 horas
    df = pd.read_sql_query("""
        SELECT fecha, llamaradas_m, llamaradas_x, indice_kp 
        FROM datos_solares 
        WHERE fecha >= datetime('now', '-1 day')
        ORDER BY fecha
    """, conn)
    
    if len(df) > 0:
        df['fecha'] = pd.to_datetime(df['fecha'])
        
        # Crear gráficos
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Gráfico de llamaradas
        ax1.plot(df['fecha'], df['llamaradas_m'], 'o-', label='Llamaradas M', color='orange')
        ax1.plot(df['fecha'], df['llamaradas_x'], 's-', label='Llamaradas X', color='red')
        ax1.set_ylabel('Llamaradas solares')
        ax1.set_title('Actividad Solar - Últimas 24 horas')
        ax1.legend()
        ax1.grid(True)
        
        # Gráfico de índice Kp
        ax2.plot(df['fecha'], df['indice_kp'], '^-', label='Índice Kp', color='purple')
        ax2.set_ylabel('Índice Kp')
        ax2.set_xlabel('Fecha/Hora')
        ax2.axhline(y=5, color='r', linestyle='--', label='Límite tormenta (Kp=5)')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('dashboard_solar.png')
        print("✅ Gráfico guardado como 'dashboard_solar.png'")
        
    conn.close()

if __name__ == "__main__":
    mostrar_estadisticas()
    print("\n📸 Generando gráfico...")
    graficar_datos()
    print("\n🎯 Para gestionar el sistema: ./gestion_sistema.sh {start|stop|status|stats}")
