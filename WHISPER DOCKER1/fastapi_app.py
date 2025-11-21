from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from typing import List
import whisper
import torch
from tempfile import NamedTemporaryFile

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

model = whisper.load_model("base", device=DEVICE)

app = FastAPI()

@app.post("/whisper")
async def handler(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No file uploaded")

    results = []

    for file in files:
        with NamedTemporaryFile(delete=False, suffix=".wav") as temp:
            # Save uploaded file
            temp.write(await file.read())
            temp.flush()

            # Transcription
            result = model.transcribe(temp.name)

        results.append({
            "filename": file.filename,
            "transcript": result["text"]
        })

    return JSONResponse(content={"results": results})

@app.get("/", response_class=RedirectResponse)
async def redirect_to_docs():
    return "/docs"
