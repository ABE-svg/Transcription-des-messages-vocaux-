from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from tempfile import NamedTemporaryFile
from pathlib import Path
import whisper
import torch

# Détection du device (GPU si dispo, sinon CPU)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Chargement du modèle Whisper 
model = whisper.load_model("base", device=DEVICE)

app = FastAPI(title="TranscriptoAI", description="API de transcription audio/vidéo", version="1.0.0")

# CORS : à adapter selon où tu héberges le front
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/whisper")
async def transcribe_endpoint(
    file: UploadFile = File(...),
    summary: bool = Form(False),
):
    """
    Endpoint principal :
    - Reçoit un fichier (audio ou vidéo)
    - Option summary=True pour demander un résumé
    - Retourne JSON { filename, transcript, summary }
    """
    # Vérification basique du type de fichier
    if not file.filename:
        raise HTTPException(status_code=400, detail="Aucun fichier reçu.")

    # On accepte tout ce que ffmpeg/whisper sait lire (audio/vidéo)
    try:
        suffix = Path(file.filename).suffix
        if not suffix:
            suffix = ".bin"

        # Écriture dans un fichier temporaire
        with NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            contents = await file.read()
            temp.write(contents)
            temp_path = temp.name

        # Transcription avec Whisper
        result = model.transcribe(temp_path)
        transcript = (result.get("text") or "").strip()

        # summary
        summary_text = None
        if summary and transcript:
            sentences = [s.strip() for s in transcript.split(".") if s.strip()]
            if len(sentences) <= 2:
                summary_text = transcript
            else:
                summary_text = ". ".join(sentences[:2]) + "."

        # Construction de la réponse
        response_data = {
            "filename": file.filename,
            "transcript": transcript,
            "summary": summary_text,
        }
        return JSONResponse(content=response_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur pendant la transcription : {e}")




@app.get("/")
def serve_frontend():
    return FileResponse(Path("frontend/index.html"))

# Servir le frontend (index.html, script.js, style.css) depuis un dossier "frontend"
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
