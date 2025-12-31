from flask import Flask, request, jsonify, render_template
from flasgger import Swagger
import os

from app.services.transcribe_service import transcribe_audio
from app.services.summary_service import summarize_text
from app.utils.audio_utils import allowed_file, save_temp_file


def create_app():
    app = Flask(__name__)

    Swagger(app, template_file="docs/swagger.yaml")

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route('/transcribe', methods=['POST'])
    def transcribe():
        """
        Cet endpoint reçoit un fichier audio envoyé par l’utilisateur.
        L’API renvoie la transcription du contenu, et peut aussi produire un résumé
        si l’option correspondante est activée.
        """

        if "audio" not in request.files:
            return jsonify({"error": "Aucun fichier audio reçu"}), 400

        audio_file = request.files["audio"]
        model_name = request.args.get("model", "tiny")


        if audio_file.filename == "":
            return jsonify({"error": "Nom de fichier invalide"}), 400

        if not allowed_file(audio_file.filename):
            return jsonify({"error": "Format non supporté"}), 400

        try:
            file_path = save_temp_file(audio_file)

            transcription = transcribe_audio(file_path, model_name)
            generate_summary = request.args.get("summary", "false").lower() == "true"

            result = {"transcription": transcription}

            if generate_summary:
                result["summary"] = summarize_text(transcription)

            return jsonify(result), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            if "file_path" in locals() and os.path.exists(file_path):
                os.remove(file_path)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)