#!/usr/bin/env python3
"""
📊 SISTEMA CON BASE DE DATOS - Histórico de datos AEMET
"""

import sqlite3
import json
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('datos_aemet.db')
        self.create_tables()
    
    def create_tables(self):
        """Crear tablas para almacenar datos"""
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS datos_meteo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperatura REAL,
                viento_velocidad REAL,
                viento_direccion TEXT,
                humedad INTEGER,
                presion REAL,
                timestamp DATETIME,
                fuente TEXT
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS alertas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT,
                severidad TEXT,
                mensaje TEXT,
                timestamp DATETIME
            )
        ''')
        
        self.conn.commit()

# Sistema extendido con base de datos
class SistemaCompleto(SistemaAEMETReal):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        
    def guardar_datos(self, datos_meteo):
        """Guardar datos en base de datos"""
        try:
            self.db.conn.execute('''
                INSERT INTO datos_meteo 
                (temperatura, viento_velocidad, viento_direccion, humedad, presion, timestamp, fuente)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                datos_meteo['temperatura'],
                datos_meteo['viento_velocidad'],
                datos_meteo['viento_direccion'],
                datos_meteo['humedad'],
                datos_meteo['presion'],
                datetime.now().isoformat(),
                datos_meteo['fuente']
            ))
            
            self.db.conn.commit()
            print("💾 Datos guardados en base de datos")
            
        except Exception as e:
            print(f"❌ Error guardando datos: {e}")

if __name__ == "__main__":
    sistema_completo = SistemaCompleto()
    sistema_completo.iniciar_servicio_oficial()
