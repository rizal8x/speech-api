from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import shutil
import tempfile
import os
from src.services.stt import get_stt_service, SpeechToTextService
from src.services.tts import get_tts_service, TextToSpeechService

router = APIRouter(prefix="/v1/speech", tags=["Speech"])

class TTSRequest(BaseModel):
    text: str
    voice_id: str | None = None # Future extension

@router.post("/stt")
async def speech_to_text(
    file: UploadFile = File(...),
    model: SpeechToTextService = Depends(get_stt_service)
):
    # Save temp file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
        
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    
    try:
        text, info = model.transcribe(tmp_path)
        return {
            "text": text,
            "language": info.language,
            "probability": info.language_probability
        }
    finally:
        os.unlink(tmp_path)

@router.post("/tts")
async def text_to_speech(
    request: TTSRequest,
    model: TextToSpeechService = Depends(get_tts_service)
):
    try:
        audio_buffer = model.synthesize(request.text)
        return StreamingResponse(
            audio_buffer, 
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=output.wav"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
