#!/bin/bash
# Script para gestionar el Sistema Completo de Alerta Temprana

case "$1" in
    start)
        echo "🚀 Iniciando Sistema Completo de Alerta Temprana..."
        source venv_alerta/bin/activate
        nohup python sistema_completo_vidas.py > sistema_completo.log 2>&1 &
        echo $! > sistema_completo.pid
        echo "✅ Sistema completo iniciado (PID: $(cat sistema_completo.pid))"
        ;;
    stop)
        if [ -f sistema_completo.pid ]; then
            echo "🛑 Deteniendo Sistema Completo..."
            kill $(cat sistema_completo.pid)
            rm sistema_completo.pid
            echo "✅ Sistema detenido"
        else
            echo "❌ No hay sistema ejecutándose"
        fi
        ;;
    status)
        if [ -f sistema_completo.pid ] && kill -0 $(cat sistema_completo.pid) 2>/dev/null; then
            echo "✅ Sistema COMPLETO ejecutándose (PID: $(cat sistema_completo.pid))"
            echo "📋 Últimas líneas del log:"
            tail -5 sistema_completo.log
        else
            echo "❌ Sistema completo no está ejecutándose"
        fi
        ;;
    stats)
        echo "📊 ESTADÍSTICAS DEL SISTEMA COMPLETO:"
        echo "======================================"
        sqlite3 sistema_completo.db "SELECT COUNT(*) as 'Registros solares' FROM datos_solares;"
        sqlite3 sistema_completo.db "SELECT COUNT(*) as 'Registros oceánicos' FROM datos_oceanicos;"
        sqlite3 sistema_completo.db "SELECT COUNT(*) as 'Total alertas' FROM alertas;"
        sqlite3 sistema_completo.db "SELECT tipo, nivel, COUNT(*) as cantidad FROM alertas GROUP BY tipo, nivel;"
        ;;
    backup)
        echo "💾 Creando backup completo..."
        backup_file="backups/sistema_completo_$(date +%Y%m%d_%H%M%S).db"
        cp sistema_completo.db "$backup_file"
        cp sistema_completo.log "backups/sistema_completo_$(date +%Y%m%d_%H%M%S).log"
        echo "✅ Backup creado: $backup_file"
        ;;
    logs)
        echo "📋 Log del sistema completo:"
        tail -20 sistema_completo.log
        ;;
    dashboard)
        echo "📊 Mostrando dashboard..."
        source venv_alerta/bin/activate
        python dashboard_simple.py
        ;;
    *)
        echo "Usage: $0 {start|stop|status|stats|backup|logs|dashboard}"
        echo ""
        echo "Comandos disponibles:"
        echo "  start     - Iniciar sistema completo"
        echo "  stop      - Detener sistema"
        echo "  status    - Ver estado del sistema"
        echo "  stats     - Ver estadísticas"
        echo "  backup    - Hacer backup completo"
        echo "  logs      - Ver logs"
        echo "  dashboard - Ver dashboard rápido"
        exit 1
        ;;
esac
