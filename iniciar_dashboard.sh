#!/bin/bash
echo "🌐 Iniciando Dashboard Web..."
echo "📊 Accede en: http://localhost:5000"
source ../venv_alerta/bin/activate
cd web_dashboard
python app.py
