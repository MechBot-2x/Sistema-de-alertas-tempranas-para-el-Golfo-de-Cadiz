#!/bin/bash
echo "🌊 Activando Sistema de Alertas del Golfo de Cádiz..."

# Crear directorio de logs
mkdir -p logs

if [ ! -d "venv" ]; then
    echo "🐍 Creando entorno virtual..."
    python -m venv venv
fi

# Activar entorno virtual
source venv/bin/activate

echo "📦 Instalando dependencias..."
pip install requests python-telegram-bot python-dotenv beautifulsoup4 schedule

echo "✅ Verificando sistema..."
python -m scripts.utilidades.verificador_estado

echo "🎉 Sistema listo para usar!"
echo "💡 Para ejecutar: python -m scripts.monitoreo.sistema_principal"
echo "💡 Para desactivar: deactivate"
