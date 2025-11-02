"""Telegram update handlers."""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from .config import Settings
from .ocr import extract_text

LOGGER = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""

    assert update.effective_chat
    await update.effective_chat.send_message(
        "Здравствуйте!\n"
        "Отправьте мне фотографию акцизной марки, и я распознаю её текст.",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""

    assert update.effective_chat
    await update.effective_chat.send_message(
        "Отправьте фотографию акцизной марки."
        "\nМожно также указать желаемые языки через переменную OCR_LANGUAGES"
        " (например, 'ru,en').",
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process an incoming photo and respond with OCR results."""

    message = update.effective_message
    if message is None:
        return

    assert context.application is not None
    settings: Settings = context.application.bot_data["settings"]

    photo = message.photo[-1] if message.photo else None
    if not photo:
        await message.reply_text("Не удалось получить фотографию. Попробуйте ещё раз.")
        return

    await message.chat.send_action(action=ChatAction.TYPING)

    telegram_file = await photo.get_file()

    try:
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            tmp_path = Path(tmp_file.name)
        await telegram_file.download_to_drive(str(tmp_path))

        try:
            lines = await extract_text(str(tmp_path), settings)
        finally:
            tmp_path.unlink(missing_ok=True)
    except Exception as exc:  # pragma: no cover - defensive branch
        LOGGER.exception("Failed to process image: %s", exc)
        await message.reply_text(
            "Произошла ошибка при обработке изображения. Попробуйте позже."
        )
        return

    if not lines:
        await message.reply_text("Не удалось распознать текст на изображении.")
        return

    response = "\n".join(f"• {line}" for line in lines)
    await message.reply_text("Распознанный текст:\n" + response)


async def post_init(application: Application) -> None:
    """Store settings in application state for handlers."""

    settings: Settings = application.bot_data["settings"]
    LOGGER.info(
        "Bot initialised with languages: %s (GPU=%s)",
        ",".join(settings.languages),
        settings.use_gpu,
    )


def register(application: Application, settings: Settings) -> None:
    """Register handlers on the provided application."""

    application.bot_data["settings"] = settings
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.post_init.append(post_init)
