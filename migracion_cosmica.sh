#!/bin/bash
echo "🌌 SCRIPT DE MIGRACIÓN CÓSMICA"
echo "================================"

# Colores para mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}1. Verificando Python...${NC}"
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ Python3 encontrado: $(python3 --version)${NC}"
else
    echo -e "${RED}✗ Python3 no encontrado${NC}"
    exit 1
fi

echo -e "${BLUE}2. Creando entorno virtual...${NC}"
python3 -m venv venv_pc
source venv_pc/bin/activate

echo -e "${BLUE}3. Instalando dependencias cósmicas...${NC}"
pip install --upgrade pip
pip install requests beautifulsoup4 schedule python-telegram-bot python-dotenv pandas ephem matplotlib

echo -e "${BLUE}4. Verificando estructura del proyecto...${NC}"
if [ -d "scripts" ]; then
    echo -e "${GREEN}✓ Directorio scripts encontrado${NC}"
else
    echo -e "${RED}✗ Estructura incorrecta${NC}"
    exit 1
fi

echo -e "${BLUE}5. Probando sistema cósmico...${NC}"
python -c "
from scripts.monitoreo.sismico_cosmico import SismicMonitorCosmico
from scripts.monitoreo.boyas_avanzadas_2025 import BoyasAvanzadas2025
print('✅ Importaciones cósmicas exitosas')
"

echo -e "${GREEN}🎉 MIGRACIÓN CÓSMICA COMPLETADA${NC}"
echo -e "${YELLOW}Recuerda: source venv_pc/bin/activate para activar el entorno${NC}"
