# 🌊🚨 Sistema de Alertas Tempranas - Golfo de Cádiz

Sistema profesional de monitorización y alertas para el Golfo de Cádiz.

## 🎯 Características

- 📡 **Datos en tiempo real** de AEMET (Gobierno de España)
- 🌊 **Monitorización oceánica** con Copernicus Marine
- 🌋 **Detección sísmica** en tiempo real
- 🤖 **Alertas automáticas** por Telegram
- 📊 **Base de datos** histórica
- 🚨 **Protocolos de emergencia**

## 🛠️ Tecnologías

- Python 3.8+
- SQLite3
- APIs: AEMET, Copernicus, USGS
- Telegram Bot API
- Pandas, NumPy, Matplotlib

## 📦 Instalación

```bash
git clone https://github.com/mechmind-dwv/Sistema-de-alertas-tempranas-para-el-Golfo-de-Cadiz.git
cd sistema-alertas-golfo-cadiz

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## ⚙️ Configuración

1. Copiar `.env.example` a `.env`
2. Configurar credenciales API
3. Ejecutar `python sistema_principal.py`

## 🚀 Uso

```bash
# Sistema principal
python sistema_principal.py

# Solo Copernicus
python -m scripts.datos.copernicus_simple

# Solo sismógrafo  
python -m scripts.datos.sismografo
```

## 📞 Contacto

- 📧 Email: ia.mechmind@gmail.com
- 🤖 Telegram: @Tsunamis_bot
- 🌐 AEMET: https://opendata.aemet.es

## 📜 Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles.
