#!/usr/bin/env python3
"""
🌐 API LOCAL - Servir datos AEMET via REST                        """
                                                                  from flask import Flask, jsonify
from sistema_aemet_real import SistemaAEMETReal                   
app = Flask(__name__)                                             sistema = SistemaAEMETReal()
                                                                  @app.route('/datos', methods=['GET'])
def obtener_datos():
    datos, fuente = sistema.obtener_datos_reales()
    return jsonify({                                                      'datos': datos,
        'fuente': fuente,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/estado', methods=['GET'])
def estado():
    return jsonify({                                                      'estado': 'operativo',
        'servicio': 'AEMET OpenData',
        'region': 'Golfo de Cádiz'
    })
                                                                  if __name__ == '__main__':
    print("🌐 Iniciando API local en http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
