from flask import Flask, request, render_template
import os
from app.transcribe_service import transcribe_audio

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", transcription=None)

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "audio" not in request.files:
        return "Aucun fichier reçu", 400

    audio_file = request.files["audio"]
    if audio_file.filename == "":
        return "Nom de fichier invalide", 400

    temp_path = f"/tmp/{audio_file.filename}"
    audio_file.save(temp_path)

    transcription = transcribe_audio(temp_path)
    os.remove(temp_path)

    return render_template("index.html", transcription=transcription)
