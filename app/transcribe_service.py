import whisper

model = whisper.load_model("tiny") #ou base

def transcribe_audio(file_path: str) -> str:
    result = model.transcribe(file_path)
    return result["text"]
