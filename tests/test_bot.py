import pytest
import asyncio
from unittest.mock import AsyncMock, patch

from bot.main import handle_voice


@pytest.mark.asyncio
async def test_transcription_no_translation():
    update = AsyncMock()
    context = AsyncMock()

    # fake Telegram values
    update.effective_user.language_code = "fr"
    update.message.voice.file_id = "12345"
    update.message.reply_text = AsyncMock()

    context.bot.get_file = AsyncMock(return_value=AsyncMock(download_to_drive=AsyncMock()))

    with patch("bot.main.transcribe_audio", return_value={
        "text": "Bonjour",
        "language": "french"
    }):
        await handle_voice(update, context)

    update.message.reply_text.assert_any_call("Processing voice message...")
    update.message.reply_text.assert_any_call("Language: french\n\nBonjour")


@pytest.mark.asyncio
async def test_translation_triggered():
    update = AsyncMock()
    context = AsyncMock()

    update.effective_user.language_code = "en"
    update.message.voice.file_id = "12345"
    update.message.reply_text = AsyncMock()

    context.bot.get_file = AsyncMock(return_value=AsyncMock(download_to_drive=AsyncMock()))

    with patch("bot.main.transcribe_audio", return_value={
        "text": "Bonjour",
        "language": "french"
    }), patch("bot.main.translator", return_value="Hello"):
        await handle_voice(update, context)

    update.message.reply_text.assert_any_call("Language: french\n\nBonjour")
    update.message.reply_text.assert_any_call("Translated to en:\n\nHello")


@pytest.mark.asyncio
async def test_transcription_failure():
    update = AsyncMock()
    context = AsyncMock()

    update.effective_user.language_code = "en"
    update.message.voice.file_id = "123"

    context.bot.get_file = AsyncMock(return_value=AsyncMock(download_to_drive=AsyncMock()))
    update.message.reply_text = AsyncMock()

    with patch("bot.main.transcribe_audio", side_effect=Exception("API error")):
        await handle_voice(update, context)

    update.message.reply_text.assert_any_call(
        "Transcription service unavailable.\nLikely reason: OpenAI credits exhausted or API error."
    )
