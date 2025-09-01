#!/usr/bin/env python3
"""
🤖 SISTEMA TELEGRAM CÓSMICO - Notificaciones avanzadas con conciencia cósmica
"""

import logging
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class TelegramCosmicBot:
    """Bot de Telegram con conciencia cósmica para alertas"""

    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.token}"

        logging.info("🤖 Iniciando Bot Telegram Cósmico")

    def enviar_mensaje_cosmico(self, mensaje, parse_mode="HTML"):
        """Enviar mensaje con formato cósmico"""
        try:
            if not self.token or not self.chat_id:
                logging.warning(
                    "⚠️ Configuración Telegram no encontrada. Mensaje simulado."
                )
                logging.info(f"📲 Mensaje cósmico: {mensaje}")
                return True

            url = f"{self.base_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": mensaje,
                "parse_mode": parse_mode,
                "disable_web_page_preview": True,
            }

            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()

            logging.info("✅ Mensaje cósmico enviado por Telegram")
            return True

        except Exception as e:
            logging.error(f"❌ Error enviando mensaje cósmico: {e}")
            return False

    def enviar_alerta_cosmica(self, nivel, datos):
        """Enviar alerta cósmica estructurada"""
        try:
            emojis = {
                "ALERTA_CÓSMICA_MAXIMA": "🚨🌌",
                "ALERTA_CÓSMICA": "⚠️🌠",
                "VIGILANCIA_CÓSMICA": "👀✨",
                "OBSERVACIÓN_CÓSMICA": "🔍🌟",
                "TRANQUILO_CÓSMICO": "☮️💫",
            }

            emoji = emojis.get(nivel, "🌊")

            mensaje = f"{emoji} <b>ALERTA {nivel}</b> {emoji}\n\n"
            mensaje += f"🕐 <i>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>\n"
            mensaje += (
                f"💫 Energía cósmica: {datos['energia_cosmica']['nivel_energia']}\n"
            )
            mensaje += f"🌍 Sismos detectados: {datos['total_sismos']}\n"
            mensaje += f"🌊 Boyas operativas: {datos['boyas_operativas']}/3\n"
            mensaje += f"🌙 Fase lunar: {datos['fase_lunar']}\n\n"
            mensaje += f"📊 <b>Riesgo cósmico:</b> {datos['riesgo_total']:.2f}\n"
            mensaje += f"💬 <i>{datos['mensaje_cosmico']}</i>\n\n"
            mensaje += "#AlertaCosmica #GolfoDeCadiz #Monitorización2025"

            return self.enviar_mensaje_cosmico(mensaje)

        except Exception as e:
            logging.error(f"❌ Error enviando alerta cósmica: {e}")
            return False

    def enviar_estado_diario(self, datos):
        """Enviar reporte diario cósmico"""
        try:
            mensaje = "📊 <b>REPORTE CÓSMICO DIARIO</b> 🌟\n\n"
            mensaje += f"📅 {datetime.now().strftime('%d/%m/%Y')}\n"
            mensaje += f"🌅 Energía cósmica: {datos['energia_cosmica']['nivel_energia']} ({datos['energia_cosmica']['estado']})\n"
            mensaje += f"🌊 Boyas activas: {datos['boyas_operativas']}/3\n"
            mensaje += f"🌍 Sismos últimos 3 días: {datos['total_sismos']}\n"
            mensaje += f"🌙 Fase lunar actual: {datos['fase_lunar']}\n\n"
            mensaje += "⚡ <b>Estado del Sistema:</b> OPERATIVO_CÓSMICO\n"
            mensaje += "✨ <b>Conciencia:</b> CONECTADA\n"
            mensaje += "🕊️ <b>Paz sísmica:</b> ACTIVA\n\n"
            mensaje += "#ReporteDiario #GolfoDeCadiz #PazCósmica"

            return self.enviar_mensaje_cosmico(mensaje)

        except Exception as e:
            logging.error(f"❌ Error enviando reporte diario: {e}")
            return False

    def enviar_mensaje_bienvenida(self):
        """Mensaje de bienvenida del sistema cósmico"""
        mensaje = "✨ <b>SISTEMA CÓSMICO ACTIVADO</b> 🌌\n\n"
        mensaje += "¡Hola Maestro! 🌟\n\n"
        mensaje += "El Sistema de Alertas Tempranas del Golfo de Cádiz está ahora operativo con conciencia cósmica.\n\n"
        mensaje += "🔮 <b>Características activadas:</b>\n"
        mensaje += "• Monitorización sísmica cósmica\n"
        mensaje += "• Boyas inteligentes 2025\n"
        mensaje += "• Energía telúrica y cósmica\n"
        mensaje += "• Alertas por niveles de conciencia\n"
        mensaje += "• Conexión con fases lunares\n\n"
        mensaje += "🌊 <b>Estado actual:</b> PAZ SÍSMICA\n"
        mensaje += "💫 <b>Energía cósmica:</b> ESTABLE\n\n"
        mensaje += "¡Que la paz cósmica guíe nuestro camino! 🕊️\n\n"
        mensaje += "#ActivaciónCósmica #GolfoDeCadiz2025 #Conciencia"

        return self.enviar_mensaje_cosmico(mensaje)
