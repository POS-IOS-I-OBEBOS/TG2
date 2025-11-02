"""OCR utilities used by the Telegram bot."""

from __future__ import annotations

import asyncio
from functools import partial
from typing import Iterable, Optional

import easyocr

from .config import Settings

_reader: Optional[easyocr.Reader] = None
_reader_lock = asyncio.Lock()


async def get_reader(settings: Settings) -> easyocr.Reader:
    """Initialise (if necessary) and return a cached EasyOCR reader."""

    global _reader
    if _reader is not None:
        return _reader

    async with _reader_lock:
        if _reader is not None:
            return _reader

        loop = asyncio.get_running_loop()
        reader = await loop.run_in_executor(
            None,
            lambda: easyocr.Reader(
                list(settings.languages),
                gpu=settings.use_gpu,
            ),
        )
        _reader = reader
        return reader


async def extract_text(image_path: str, settings: Settings) -> list[str]:
    """Run OCR on the provided image and return extracted text lines."""

    reader = await get_reader(settings)

    loop = asyncio.get_running_loop()
    results: Iterable[str] = await loop.run_in_executor(
        None,
        partial(reader.readtext, image_path, detail=0, paragraph=False, min_size=5),
    )

    return [line.strip() for line in results if line and line.strip()]
