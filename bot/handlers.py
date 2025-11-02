"""Telegram update handlers."""

from __future__ import annotations

import logging
from io import BytesIO

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from .ocr import OCRSpaceError, recognize_excise_stamp

LOGGER = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a greeting message when the bot is started."""

    if update.message is None:
        return

    LOGGER.info("Received /start from chat_id=%s", update.message.chat_id)
    await update.message.reply_text(
        "Здравствуйте! Отправьте фотографию акцизной марки, и я постараюсь распознать текст."  # noqa: E501
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Provide usage information."""

    if update.message is None:
        return

    LOGGER.info("Received /help from chat_id=%s", update.message.chat_id)
    await update.message.reply_text(
        "Просто отправьте фото акцизной марки. Я преобразую изображение в текст, используя OCR.space."
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process an incoming photo and run OCR on it."""

    if update.message is None or not update.message.photo:
        return

    LOGGER.info(
        "Received photo message from chat_id=%s with %d sizes",
        update.message.chat_id,
        len(update.message.photo),
    )
    await update.message.chat.send_action(action=ChatAction.TYPING)

    photo = update.message.photo[-1]
    bot = context.bot
    file = await bot.get_file(photo.file_id)

    buffer = BytesIO()
    await file.download_to_memory(out=buffer)
    image_bytes = buffer.getvalue()
    LOGGER.info(
        "Downloaded photo for chat_id=%s with %d bytes",
        update.message.chat_id,
        len(image_bytes),
    )

    settings = context.application.bot_data["settings"]

    try:
        LOGGER.info(
            "Sending image for OCR: chat_id=%s language=%s",
            update.message.chat_id,
            settings.ocr_language,
        )
        text = await recognize_excise_stamp(
            image_bytes,
            api_key=settings.ocr_api_key,
            language=settings.ocr_language,
        )
    except OCRSpaceError as exc:
        LOGGER.exception("OCR processing error: %s", exc)
        await update.message.reply_text(
            "Не удалось распознать текст: {error}".format(error=exc)
        )
        return
    except Exception as exc:  # noqa: BLE001
        LOGGER.exception("Unexpected error: %s", exc)
        await update.message.reply_text(
            "Произошла неожиданная ошибка при обработке изображения."
        )
        return

    text = text.strip()
    if text:
        LOGGER.info("OCR succeeded for chat_id=%s with %d characters", update.message.chat_id, len(text))
        await update.message.reply_text(
            "Распознанный текст:\n\n{result}".format(result=text)
        )
    else:
        LOGGER.info("OCR returned empty result for chat_id=%s", update.message.chat_id)
        await update.message.reply_text(
            "К сожалению, не удалось распознать текст на изображении. Попробуйте другое фото."
        )
