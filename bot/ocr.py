"""OCR utilities for recognizing excise stamps."""

from __future__ import annotations

from typing import Any

import httpx


class OCRSpaceError(RuntimeError):
    """Raised when the OCR.space API returns an error."""


async def recognize_excise_stamp(
    image_bytes: bytes,
    api_key: str,
    *,
    language: str = "eng",
    timeout: float = 60.0,
) -> str:
    """Recognize text on an excise stamp using the OCR.space API.

    Args:
        image_bytes: Raw bytes of the image to be recognized.
        api_key: API key for the OCR.space service. Use ``"helloworld"`` for the
            free tier with limited throughput.
        language: Optional OCR language code, defaults to ``"eng"``.
        timeout: Request timeout in seconds.

    Returns:
        Recognized text.

    Raises:
        OCRSpaceError: If the OCR service reports an error.
    """

    headers = {"apikey": api_key}
    data = {"language": language, "isOverlayRequired": False}
    files = {"file": ("excise_stamp.jpg", image_bytes)}

    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout)) as client:
        response = await client.post(
            "https://api.ocr.space/parse/image",
            headers=headers,
            data=data,
            files=files,
        )

    response.raise_for_status()
    payload: dict[str, Any] = response.json()

    if payload.get("IsErroredOnProcessing"):
        error_message = payload.get("ErrorMessage") or payload.get("ErrorDetails")
        raise OCRSpaceError(str(error_message))

    parsed_results = payload.get("ParsedResults") or []
    if not parsed_results:
        return ""

    text_chunks = []
    for result in parsed_results:
        parsed_text = result.get("ParsedText")
        if parsed_text:
            text_chunks.append(parsed_text.strip())

    return "\n".join(chunk for chunk in text_chunks if chunk)
