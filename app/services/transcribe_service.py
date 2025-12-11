import whisper

def transcribe_audio(file_path):
    model = whisper.load_model("tiny")
    result = model.transcribe(file_path)
    return result["text"]