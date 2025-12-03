from flask import Flask, request, jsonify
from flasgger import Swagger
import os

from app.services.transcribe_service import transcribe_audio
from app.services.summary_service import summarize_text

from app.utils.audio_utils import allowed_file, save_temp_file


def create_app():
    app = Flask(__name__)

    swagger = Swagger(app, template_file="app/docs/swagger.yaml")

    @app.route('/transcribe', methods=['POST'])
    def transcribe():
        """
    Cet endpoint reçoit un fichier audio envoyé par l’utilisateur.
    L’API renvoie la transcription du contenu, et peut aussi produire un résumé
    si l’option correspondante est activée.

    ---
    consumes:
    - multipart/form-data

    parameters:
    - name: audio
     in: formData
     type: file
     required: true
     description: Le fichier audio à transcrire.

    - name: summary
        in: query
        type: boolean
     required: false
     description: Activer cette option pour obtenir également un résumé.

    responses:
    200:
     description: Réponse contenant la transcription et éventuellement le résumé.
"""

        if "audio" not in request.files:
            return jsonify({"error": "Aucun fichier audio reçu"}), 400

        audio_file = request.files["audio"]

        if audio_file.filename == "":
            return jsonify({"error": "Le nom du fichier n'est pas valide"}), 400

        if not allowed_file(audio_file.filename):
            return jsonify({"error": "Format non supporté"}), 400

        
        file_path = save_temp_file(audio_file)
        transcription = transcribe_audio(file_path)

        generate_summary = request.args.get("summary", "false").lower() == "true"

        result = {"transcription": transcription}

        if generate_summary:
            result["summary"] = summarize_text(transcription)

        os.remove(file_path)

        return jsonify(result), 200

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
