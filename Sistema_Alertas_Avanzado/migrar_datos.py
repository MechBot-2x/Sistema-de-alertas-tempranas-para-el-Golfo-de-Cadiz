#!/usr/bin/env python3
"""
📦 MIGRACIÓN DE DATOS - Android → PC
"""

import sqlite3
import pandas as pd
from sqlalchemy import create_engine

def migrar_datos():
    print("🔄 MIGRANDO DATOS DE ANDROID A PC...")
    
    # Conectar a base de datos Android
    conn_android = sqlite3.connect('datos_golfo_cadiz.db')
    
    # Leer datos existentes
    df = pd.read_sql_query("SELECT * FROM mediciones", conn_android)
    print(f"📊 Datos a migrar: {len(df)} registros")
    
    # Conectar a base de datos PC
    engine_pc = create_engine('sqlite:///Sistema_Alertas_Avanzado/data/alertas_golfo_cadiz.db')
    
    # Migrar datos
    df.to_sql('mediciones', engine_pc, if_exists='append', index=False)
    
    print("✅ Migración completada exitosamente")
    print(f"📈 Registros migrados: {len(df)}")

if __name__ == "__main__":
    migrar_datos()
