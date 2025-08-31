# 📖 MANUAL DEL SISTEMA DE ALERTA TEMPRANA

## 🚀 INICIO RÁPIDO

### Instalación:
```bash
./instalar_sistema.sh
source venv_alerta/bin/activate
Ejecución:
bash

# Método 1: Ejecución directa
python sistema_alerta_vidas.py

# Método 2: Usar script de gestión
./gestion_sistema.sh start

📊 COMANDOS DE GESTIÓN
bash

# Iniciar sistema
./gestion_sistema.sh start

# Detener sistema  
./gestion_sistema.sh stop

# Ver estado
./gestion_sistema.sh status

# Ver estadísticas
./gestion_sistema.sh stats

# Ver logs
./gestion_sistema.sh logs

# Hacer backup
./gestion_sistema.sh backup

📈 VISUALIZACIÓN DE DATOS
bash

# Ver dashboard de datos
python dashboard.py

⚠️ NIVELES DE ALERTA

    ALTO: Riesgo > 70% (Llamaradas X o múltiples M + alta actividad geomagnética)

    MEDIO: Riesgo > 50% (Múltiples llamaradas M)

    BAJO: Riesgo > 30% (Alguna actividad solar)

🔧 CONFIGURACIÓN

Editar el archivo .env para configurar:

    Claves API de NASA y Telegram

    Intervalo de monitoreo (minutos)

    Umbrales de alerta

📁 ESTRUCTURA

    sistema_alerta_vidas.py - Sistema principal

    alertas_vidas.db - Base de datos SQLite

    alerts.log - Archivo de logs

    backups/ - Copias de seguridad

    dashboard.py - Visualización de datos

❤️ MISIÓN

Este sistema ayuda a salvar vidas mediante el monitoreo de actividad solar
que puede afectar sistemas eléctricos, comunicaciones y salud humana.

¡Cada alerta puede salvar vidas!
