#!/bin/bash
# Script de inicio para sistema cósmico en PC

cd "$(dirname "$0")"

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🌌 Iniciando Sistema Cósmico en PC...${NC}"

# Verificar si el entorno virtual está activado
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activando entorno virtual..."
    source venv_pc/bin/activate
fi

echo -e "${GREEN}✅ Entorno: $(which python)${NC}"
echo -e "${GREEN}✅ Versión: $(python --version)${NC}"

# Ejecutar el sistema principal
python -m scripts.monitoreo.sistema_cosmico_completo
