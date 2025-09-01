#!/usr/bin/env python3
"""
📊 DASHBOARD SIMPLIFICADO - Sin dependencias pesadas
"""

import sqlite3
from datetime import datetime

def mostrar_dashboard():
    """Mostrar dashboard simple sin pandas"""
    conn = sqlite3.connect('sistema_completo.db')
    
    print("🌊 DASHBOARD SISTEMA COMPLETO")
    print("=" * 40)
    
    # Estadísticas básicas
    total_solar = conn.execute("SELECT COUNT(*) FROM datos_solares").fetchone()[0]
    total_oceano = conn.execute("SELECT COUNT(*) FROM datos_oceanicos").fetchone()[0]
    total_alertas = conn.execute("SELECT COUNT(*) FROM alertas").fetchone()[0]
    
    print(f"📈 Registros solares: {total_solar}")
    print(f"🌊 Registros oceánicos: {total_oceano}")
    print(f"🚨 Alertas totales: {total_alertas}")
    
    # Alertas por tipo y nivel
    print("\n📊 Alertas por tipo:")
    alertas_tipo = conn.execute("SELECT tipo, nivel, COUNT(*) FROM alertas GROUP BY tipo, nivel").fetchall()
    for tipo, nivel, cantidad in alertas_tipo:
        print(f"   {tipo}-{nivel}: {cantidad}")
    
    # Últimos registros solares
    print("\n🌞 Últimos registros solares:")
    ultimos_solar = conn.execute("""
        SELECT fecha, llamaradas_m, llamaradas_x, indice_kp, riesgo_solar 
        FROM datos_solares 
        ORDER BY id DESC LIMIT 3
    """).fetchall()
    
    for fecha, m, x, kp, riesgo in ultimos_solar:
        hora = fecha[11:16]  # Extraer solo hora:minuto
        print(f"   {hora}: M={m}, X={x}, Kp={kp}, Riesgo={riesgo:.0%}")
    
    # Últimos registros oceánicos
    print("\n🌊 Últimos registros oceánicos:")
    ultimos_oceano = conn.execute("""
        SELECT fecha, temperatura_agua, oleaje_altura, riesgo_tsunami 
        FROM datos_oceanicos 
        ORDER BY id DESC LIMIT 3
    """).fetchall()
    
    for fecha, temp, oleaje, riesgo in ultimos_oceano:
        hora = fecha[11:16]
        print(f"   {hora}: Temp={temp}°C, Oleaje={oleaje}m, Riesgo={riesgo:.0%}")
    
    # Estado del sistema
    print(f"\n✅ Sistema funcionando correctamente - {datetime.now().strftime('%d/%m %H:%M')}")
    
    conn.close()

if __name__ == "__main__":
    mostrar_dashboard()
