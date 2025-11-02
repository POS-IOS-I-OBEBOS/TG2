"""Entry-point for running the Telegram OCR bot."""

from __future__ import annotations

import asyncio
import logging
import signal
from contextlib import suppress

from telegram.ext import Application

from .config import ConfigError, Settings, load_settings
from .handlers import register

LOGGER = logging.getLogger(__name__)


async def run_bot(settings: Settings) -> None:
    """Configure and start the Telegram bot."""

    application = Application.builder().token(settings.bot_token).build()
    register(application, settings)

    await application.initialize()
    await application.start()

    LOGGER.info("Bot is running. Press Ctrl+C to exit.")

    stop_event = asyncio.Event()

    loop = asyncio.get_running_loop()

    def _handle_signal(signum: int, _frame) -> None:  # pragma: no cover - signal handler
        LOGGER.info("Received signal %s, shutting down...", signum)
        stop_event.set()

    for signame in (signal.SIGINT, signal.SIGTERM):
        with suppress(NotImplementedError):
            loop.add_signal_handler(signame, _handle_signal, signame, None)

    await stop_event.wait()

    await application.stop()
    await application.shutdown()


def main() -> None:
    """Program entry-point."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    try:
        settings = load_settings()
    except ConfigError as exc:
        LOGGER.error("Configuration error: %s", exc)
        raise SystemExit(1) from exc

    asyncio.run(run_bot(settings))


if __name__ == "__main__":
    main()
