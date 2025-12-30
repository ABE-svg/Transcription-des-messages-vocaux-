import whisper

_MODELS = {}

def transcribe_audio(file_path, model_name="tiny"):
    if model_name not in _MODELS:
        _MODELS[model_name] = whisper.load_model(model_name)

    model = _MODELS[model_name]
    result = model.transcribe(file_path)
    return result["text"]