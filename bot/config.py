"""Configuration helpers for the Telegram excise stamp bot."""

from __future__ import annotations

import getpass
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    bot_token: str
    ocr_api_key: str
    ocr_language: str = "eng"
    log_file: str = "bot.log.txt"

    @staticmethod
    def from_env() -> "Settings":
        """Load settings from environment variables.

        Returns:
            Settings: Populated settings object.

        Raises:
            RuntimeError: If the bot token is missing.
        """

        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not bot_token:
            bot_token = Settings._prompt_bot_token()

        api_key = os.getenv("OCR_SPACE_API_KEY", "helloworld")
        language = os.getenv("OCR_LANGUAGE", "eng")
        log_file = os.getenv("BOT_LOG_FILE", "bot.log.txt")
        return Settings(
            bot_token=bot_token,
            ocr_api_key=api_key,
            ocr_language=language,
            log_file=log_file,
        )

    @staticmethod
    def _prompt_bot_token() -> str:
        """Prompt the user for a Telegram bot token via the command line."""

        while True:
            token = getpass.getpass("Введите токен Telegram-бота: ").strip()
            if token:
                return token

            print("Токен не может быть пустым. Повторите ввод.")


settings = Settings.from_env()
