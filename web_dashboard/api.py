#!/usr/bin/env python3
"""
API simple para el dashboard web
"""

from flask import Flask, jsonify
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)

def get_stats():
    """Obtener estadísticas para el dashboard"""
    conn = sqlite3.connect('sistema_completo.db')
    
    # Últimos datos solares
    solar = conn.execute("""
        SELECT llamaradas_m, llamaradas_x, indice_kp, riesgo_solar 
        FROM datos_solares 
        ORDER BY id DESC LIMIT 1
    """).fetchone() or (0, 0, 2.0, 0.1)
    
    # Últimos datos oceánicos
    ocean = conn.execute("""
        SELECT temperatura_agua, oleaje_altura, riesgo_tsunami 
        FROM datos_oceanicos 
        ORDER BY id DESC LIMIT 1
    """).fetchone() or (19.0, 1.0, 0.1)
    
    # Estadísticas de alertas
    total_alertas = conn.execute("SELECT COUNT(*) FROM alertas").fetchone()[0]
    alertas_activas = conn.execute("SELECT COUNT(*) FROM alertas WHERE enviada = 1").fetchone()[0]
    
    # Últimas alertas
    ultimas_alertas = []
    alertas_data = conn.execute("""
        SELECT fecha, mensaje 
        FROM alertas 
        ORDER BY id DESC LIMIT 5
    """).fetchall()
    
    for fecha, mensaje in alertas_data:
        ultimas_alertas.append({
            'fecha': fecha[11:16],
            'mensaje': mensaje
        })
    
    conn.close()
    
    return {
        'llamaradas_m': solar[0],
        'llamaradas_x': solar[1],
        'indice_kp': solar[2],
        'riesgo_solar': solar[3],
        'temperatura_agua': ocean[0],
        'oleaje_altura': ocean[1],
        'riesgo_tsunami': ocean[2],
        'total_alertas': total_alertas,
        'alertas_activas': alertas_activas,
        'ultimas_alertas': ultimas_alertas,
        'ultima_actualizacion': datetime.now().isoformat()
    }

@app.route('/api/estadisticas')
def estadisticas():
    return jsonify(get_stats())

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
