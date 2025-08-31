#!/usr/bin/env python3
"""
🔐 GESTOR DE TOKENS - Manejo seguro de credenciales
"""

import json
import os
from pathlib import Path


class TokenManager:
    def __init__(self):
        self.config_dir = Path.home() / ".salvemos_vida"
        self.config_file = self.config_dir / "tokens.json"
        self.config_dir.mkdir(exist_ok=True)

        # Configuración por defecto
        self.default_config = {
            "telegram": {
                "bot_token": "8478499112:AAGxqzYm4I-3Zyc9XCXIkE3mLOl8pXFOM00",
                "chat_id": "8350588401",
            },
            "aemet": {"api_key": "modo_simulacion"},
        }

    def _ensure_config_exists(self):
        """Asegurar que el archivo de configuración existe"""
        if not self.config_file.exists():
            with open(self.config_file, "w") as f:
                json.dump(self.default_config, f, indent=4)

    def get_token(self, service, key):
        """Obtener un token específico"""
        self._ensure_config_exists()
        with open(self.config_file, "r") as f:
            config = json.load(f)
        return config.get(service, {}).get(key)

    def set_token(self, service, key, value):
        """Establecer un token"""
        self._ensure_config_exists()

        with open(self.config_file, "r") as f:
            config = json.load(f)

        if service not in config:
            config[service] = {}

        config[service][key] = value

        with open(self.config_file, "w") as f:
            json.dump(config, f, indent=4)

        return True


# Instancia global
token_manager = TokenManager()
