# En tu PC, clonar el repositorio:
git clone https://github.com/tuusuario/sistema-alertas-golfo-cadiz.git
cd sistema-alertas-golfo-cadiz

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar entorno
cp .env.example .env
# Editar .env con tus credenciales reales

# Ejecutar sistema
python sistema_principal.py
