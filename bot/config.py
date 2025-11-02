"""Configuration helpers for the Telegram OCR bot."""

from __future__ import annotations

import os
from dataclasses import dataclass


class ConfigError(RuntimeError):
    """Raised when a required configuration option is missing."""


@dataclass(frozen=True)
class Settings:
    """Application settings resolved from environment variables."""

    bot_token: str
    languages: tuple[str, ...] = ("ru", "en")
    use_gpu: bool = False


def _parse_bool(value: str | None, *, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y"}


def load_settings() -> Settings:
    """Read configuration from environment variables."""

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ConfigError(
            "Environment variable TELEGRAM_BOT_TOKEN must be set to run the bot."
        )

    languages_env = os.getenv("OCR_LANGUAGES", "ru,en")
    languages = tuple(part.strip() for part in languages_env.split(",") if part.strip())
    if not languages:
        languages = ("ru", "en")

    use_gpu = _parse_bool(os.getenv("OCR_USE_GPU"))

    return Settings(bot_token=token, languages=languages, use_gpu=use_gpu)
