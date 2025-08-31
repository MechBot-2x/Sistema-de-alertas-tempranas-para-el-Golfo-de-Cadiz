#!/bin/bash
# Script para gestionar el Sistema de Alerta Temprana

case "$1" in
    start)
        echo "🚀 Iniciando Sistema de Alerta Temprana..."
        source venv_alerta/bin/activate
        nohup python sistema_alerta_vidas.py > alerts.log 2>&1 &
        echo $! > sistema.pid
        echo "✅ Sistema iniciado (PID: $(cat sistema.pid))"
        ;;
    stop)
        if [ -f sistema.pid ]; then
            echo "🛑 Deteniendo Sistema de Alerta Temprana..."
            kill $(cat sistema.pid)
            rm sistema.pid
            echo "✅ Sistema detenido"
        else
            echo "❌ No hay sistema ejecutándose"
        fi
        ;;
    status)
        if [ -f sistema.pid ] && kill -0 $(cat sistema.pid) 2>/dev/null; then
            echo "✅ Sistema ejecutándose (PID: $(cat sistema.pid))"
            tail -5 alerts.log
        else
            echo "❌ Sistema no está ejecutándose"
        fi
        ;;
    stats)
        echo "📊 ESTADÍSTICAS DEL SISTEMA:"
        echo "=============================="
        sqlite3 alertas_vidas.db "SELECT COUNT(*) as 'Total registros' FROM datos_solares;"
        sqlite3 alertas_vidas.db "SELECT COUNT(*) as 'Total alertas' FROM alertas;"
        sqlite3 alertas_vidas.db "SELECT nivel, COUNT(*) as cantidad FROM alertas GROUP BY nivel;"
        sqlite3 alertas_vidas.db "SELECT DATE(fecha) as dia, COUNT(*) as registros FROM datos_solares GROUP BY dia ORDER BY dia DESC LIMIT 5;"
        ;;
    backup)
        echo "💾 Creando backup de la base de datos..."
        backup_file="backups/alertas_$(date +%Y%m%d_%H%M%S).db"
        cp alertas_vidas.db "$backup_file"
        echo "✅ Backup creado: $backup_file"
        ;;
    logs)
        echo "📋 Últimas 10 líneas del log:"
        tail -10 alerts.log
        ;;
    *)
        echo "Usage: $0 {start|stop|status|stats|backup|logs}"
        echo ""
        echo "Comandos disponibles:"
        echo "  start   - Iniciar el sistema"
        echo "  stop    - Detener el sistema"
        echo "  status  - Ver estado del sistema"
        echo "  stats   - Ver estadísticas"
        echo "  backup  - Hacer backup de la base de datos"
        echo "  logs    - Ver logs del sistema"
        exit 1
        ;;
esac
