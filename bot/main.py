"""Entry point for the Telegram excise stamp bot."""

from __future__ import annotations

import logging
from pathlib import Path

from telegram.ext import (
    AIORateLimiter,
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)

from . import config
from .handlers import handle_photo, help_command, start

LOGGER = logging.getLogger(__name__)


def configure_logging(log_file: str) -> None:
    """Configure logging handlers for console and file output."""

    log_path = Path(log_file)
    if log_path.parent:
        log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )


def main() -> None:
    """Synchronously run the bot."""

    settings = config.settings
    configure_logging(settings.log_file)
    LOGGER.info("Starting Telegram bot with polling mode")

    application: Application = (
        ApplicationBuilder()
        .token(settings.bot_token)
        .rate_limiter(AIORateLimiter())
        .build()
    )

    application.bot_data["settings"] = settings

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    application.run_polling()


if __name__ == "__main__":
    main()
