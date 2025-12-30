from unittest.mock import patch
from app.services.transcribe_service import transcribe_audio


def test_transcribe_audio_returns_text():
    fake_result = {"text": "Bonjour ceci est un test unitaire de transcription"}

    with patch("app.services.transcribe_service.whisper.load_model") as mock_load:
        mock_model = mock_load.return_value
        mock_model.transcribe.return_value = fake_result
        result = transcribe_audio("fake/path/audio.mp3")

        assert isinstance(result, str)
        assert result == "Bonjour ceci est un test unitaire de transcription"
