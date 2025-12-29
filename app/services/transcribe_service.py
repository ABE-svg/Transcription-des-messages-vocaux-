import whisper

def transcribe_audio(file_path):
    model = whisper.load_model("base")
    #model = whisper.load_model("small") pour améliorer la transcription, mais attention long temps de traitement
    result = model.transcribe(file_path)
    return result["text"]