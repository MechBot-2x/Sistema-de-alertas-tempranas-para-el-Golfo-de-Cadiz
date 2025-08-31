#!/bin/bash
# Script de instalación del Sistema de Alerta Temprana

echo "🚀 Instalando Sistema de Alerta Temprana..."
echo "==========================================="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado. Instalando..."
    sudo apt update
    sudo apt install -y python3 python3-pip
fi

# Crear entorno virtual
echo "🐍 Creando entorno virtual..."
python3 -m venv venv_alerta
source venv_alerta/bin/activate

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install requests python-dotenv numpy

# Crear estructura de directorios
echo "📁 Creando estructura de archivos..."
mkdir -p logs backups

# Dar permisos
chmod +x sistema_alerta_vidas.py

# Verificar instalación
echo "✅ Verificando instalación..."
python3 -c "
import requests
import sqlite3
from dotenv import load_dotenv
print('✅ Todas las dependencias funcionan')
"

echo ""
echo "🎉 INSTALACIÓN COMPLETADA!"
echo "📝 Para ejecutar el sistema:"
echo "   source venv_alerta/bin/activate"
echo "   python sistema_alerta_vidas.py"
echo ""
echo "❤️  Gracias por ayudar a salvar vidas!"
