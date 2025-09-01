#!/bin/bash
#
# 🚨 PROTOCOLO DE ALERTA POR OLEAJE PELIGROSO
# Golfo de Cádiz - Sistema de Alertas Tempranas
#

echo "🚨 ACTIVANDO PROTOCOLO DE SEGURIDAD POR OLEAJE"
echo "=============================================="
echo "🌊 Altura de ola detectada: $1 m"
echo "📍 Zona: Golfo de Cádiz"
echo "⏰ Hora: $(date)"
echo ""

# Niveles de alerta
if (( $(echo "$1 > 2.5" | bc -l) )); then
    echo "🔴 ALERTA ROJA: OLEAJE MUY PELIGROSO"
    echo "   ▶️ Evitar TODA actividad acuática"
    echo "   ▶️ Cerrar accesos a playas peligrosas"
    echo "   ▶️ Alertar a servicios de emergencia"
    
elif (( $(echo "$1 > 2.0" | bc -l) )); then
    echo "🟡 ALERTA AMARILLA: OLEAJE PELIGROSO" 
    echo "   ▶️ Precaución extrema en playas"
    echo "   ▶️ No recomendable para bañistas"
    echo "   ▶️ Vigilancia reforzada"
    
elif (( $(echo "$1 > 1.5" | bc -l) )); then
    echo "🟢 ALERTA VERDE: OLEAJE MODERADO"
    echo "   ▶️ Bañistas con precaución"
    echo "   ▶️ Atención a corrientes"
    echo "   ▶️ Vigilancia normal"
fi

echo ""
echo "📞 Contacto emergencias: 112"
echo "🌐 Info meteorológica: AEMET"
echo "=============================================="
