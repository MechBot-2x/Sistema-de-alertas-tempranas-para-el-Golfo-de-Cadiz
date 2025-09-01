#!/usr/bin/env python3
"""
🌐 Dashboard Web para Sistema de Alerta Temprana
"""

from flask import Flask, render_template, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__, 
    template_folder='templates',
    static_folder='static'
)

def get_dashboard_stats():
    """Obtener estadísticas para el dashboard"""
    try:
        conn = sqlite3.connect('../sistema_completo.db')
        
        # Últimos datos solares
        solar = conn.execute("""
            SELECT llamaradas_m, llamaradas_x, indice_kp, riesgo_solar 
            FROM datos_solares 
            ORDER BY id DESC LIMIT 1
        """).fetchone()
        
        if not solar:
            solar = (0, 0, 2.0, 0.1)
        
        # Últimos datos oceánicos
        ocean = conn.execute("""
            SELECT temperatura_agua, oleaje_altura, riesgo_tsunami 
            FROM datos_oceanicos 
            ORDER BY id DESC LIMIT 1
        """).fetchone()
        
        if not ocean:
            ocean = (19.0, 1.0, 0.1)
        
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
                'fecha': fecha[11:16] if len(fecha) > 10 else fecha,
                'mensaje': mensaje
            })
        
        conn.close()
        
        return {
            'llamaradas_m': solar[0],
            'llamaradas_x': solar[1],
            'indice_kp': solar[2],
            'riesgo_solar': solar[3],
            'temperatura_agua': round(ocean[0], 1),
            'oleaje_altura': round(ocean[1], 1),
            'riesgo_tsunami': ocean[2],
            'total_alertas': total_alertas,
            'alertas_activas': alertas_activas,
            'ultimas_alertas': ultimas_alertas,
            'ultima_actualizacion': datetime.now().strftime('%H:%M:%S')
        }
        
    except Exception as e:
        print(f"Error obteniendo datos: {e}")
        return {
            'llamaradas_m': 0,
            'llamaradas_x': 0,
            'indice_kp': 2.0,
            'riesgo_solar': 0.1,
            'temperatura_agua': 19.0,
            'oleaje_altura': 1.0,
            'riesgo_tsunami': 0.1,
            'total_alertas': 0,
            'alertas_activas': 0,
            'ultimas_alertas': [],
            'ultima_actualizacion': datetime.now().strftime('%H:%M:%S')
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/estadisticas')
def estadisticas():
    return jsonify(get_dashboard_stats())

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    print("🌐 Iniciando Dashboard Web en http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
