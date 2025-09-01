#!/usr/bin/env python3
# scripts/alertas/telegram_bot.py

import sys
from datetime import datetime
import requests
from scripts.config.tokens import token_manager


def enviar_alerta_telegram(mensaje):
    """Envía alerta por Telegram (GRATIS)"""
    bot_token = token_manager.get_token("telegram", "8478499112:AAGxqzYm4I-3Zyc9XCXIkE3mLOl8pXFOM00")
    chat_id = token_manager.get_token("telegram", "8350588401")

    if not bot_token or not chat_id:
        print("❌ Telegram no configurado correctamente")
        return False

    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": (
                f"🚨 ALERTA OFICIAL CHIPIONA\n"
                f"📋 Tipo: {mensaje}\n"
                f"⏰ Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"📍 GPS: 36.7366, -6.4373\n"
                f"🌊 Sistema: Salvemos Vidas Chipiona"
            ),
        }

        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Alerta enviada por Telegram")
            return True
        else:
            print(f"❌ Error Telegram: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error enviando a Telegram: {e}")
        return False


def responder_mensajes(mensaje, chat_id):
    """Responde automáticamente a mensajes comunes"""
    respuestas = {
        "/start": "🌊 ¡Hola! Soy el sistema de alertas de Chipiona. Te mantendré informado sobre emergencias.",
        "/help": "❓ Comandos disponibles:\n/start - Iniciar\n/help - Ayuda\n/estado - Estado del sistema\n/alerta - Última alerta",
        "/estado": "✅ Sistema operativo. Monitoreando 24/7 la costa de Cádiz.",
        "hola": "👋 ¡Hola! ¿En qué puedo ayudarte hoy?",
        "gracias": "😊 ¡De nada! Estoy aquí para servir a la comunidad.",
    }

    if mensaje.lower() in respuestas:
        enviar_alerta_telegram(respuestas[mensaje.lower()], chat_id)
    else:
        enviar_alerta_telegram(
            "🤖 No entiendo ese comando. Usa /help para ver opciones.", chat_id
        )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        mensaje = " ".join(sys.argv[1:])
        enviar_alerta_telegram(mensaje)
    else:
        print("💡 Uso: python -m scripts.alertas.telegram_bot 'mensaje'")
