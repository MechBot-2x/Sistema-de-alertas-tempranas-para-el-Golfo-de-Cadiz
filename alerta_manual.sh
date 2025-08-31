#!/bin/bash
# 🚨 Script para enviar alertas MANUALES inmediatas

TOKEN="8478499112:AAGxqzYm4I-3Zyc9XCXIkE3mLOl8pXFOM00"
CHAT_ID="8350588401"
MENSAJE="$1"

if [ -z "$MENSAJE" ]; then
    echo "Usage: $0 \"Mensaje de alerta\""
    exit 1
fi

# Enviar alerta por Telegram
curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
    -d chat_id="$CHAT_ID" \
    -d text="🚨 ALERTA MANUAL 🚨%0A%0A$MENSAJE%0A%0A🕒 $(date '+%Y-%m-%d %H:%M:%S')" \
    -d parse_mode="HTML"

echo ""
echo "✅ Alerta manual enviada"
