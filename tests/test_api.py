import io
from unittest.mock import patch

from app.api import create_app


def test_transcribe_no_file():
    app = create_app()
    client = app.test_client()
    response = client.post("/transcribe")

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_transcribe_success():
    app = create_app()
    client = app.test_client()
    fake_audio = (io.BytesIO(b"fake audio content"), "test.mp3")

    with patch("app.api.transcribe_audio") as mock_transcribe, \
         patch("app.api.summarize_text") as mock_summary, \
         patch("app.api.save_temp_file") as mock_save, \
         patch("app.api.os.remove"):

        mock_save.return_value = "tmp/fake.mp3"
        mock_transcribe.return_value = "Texte transcrit"
        mock_summary.return_value = "Résumé"
        response = client.post(
            "/transcribe?summary=true",
            data={"audio": fake_audio},
            content_type="multipart/form-data"
        )
        data = response.get_json()

        assert response.status_code == 200
        assert data["transcription"] == "Texte transcrit"
        assert data["summary"] == "Résumé"

def test_invalid_audio_format():
    app = create_app()
    client = app.test_client()
    fake_file = (io.BytesIO(b"test"), "test.txt")
    response = client.post(
        "/transcribe",
        data={"audio": fake_file},
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert "Format non supporté" in response.get_json()["error"]
