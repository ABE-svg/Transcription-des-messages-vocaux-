from unittest.mock import patch
from app.services.summary_service import summarize_text


def test_summary_short_text_returns_original():
    text = "Ce texte est court"
    result = summarize_text(text)
    assert result == text


def test_summary_long_text_uses_model():
    long_text = "mot " * 100
    fake_summary = [{"summary_text": "Résumé généré"}]

    with patch("app.services.summary_service.summarizer") as mock_summarizer:
        mock_summarizer.return_value = fake_summary
        result = summarize_text(long_text)

        assert result == "Résumé généré"
