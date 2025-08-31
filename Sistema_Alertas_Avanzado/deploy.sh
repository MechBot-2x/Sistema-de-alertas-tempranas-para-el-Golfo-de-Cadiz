#!/bin/bash
#
# 🚀 SCRIPT DE DESPLIEGUE PROFESIONAL
#

echo "🚀 INICIANDO DESPLIEGUE DEL SISTEMA DE ALERTAS"
echo "=============================================="

# 1. Verificar Python
if ! command -v python &> /dev/null; then
    echo "❌ Python no encontrado"
    exit 1
fi
echo "✅ Python encontrado: $(python --version)"

# 2. Crear entorno virtual
python -m venv venv_alertas
source venv_alertas/bin/activate

# 3. Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# 4. Crear estructura de directorios
mkdir -p data logs backups

# 5. Inicializar base de datos
python -c "
from app.main import Base, engine
Base.metadata.create_all(engine)
print('✅ Base de datos inicializada')
"

# 6. Configurar variables de entorno
cp .env.example .env
echo "⚠️ Edita .env con tus credenciales"

# 7. Iniciar sistema
echo "🚀 Iniciando sistema..."
python app/main.py

echo "🎉 DESPLIEGUE COMPLETADO"
