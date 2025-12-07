import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.routes import speech
from src.services.stt import get_stt_service
from src.services.tts import get_tts_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load models on startup
    logger.info("Initializing models...")
    get_stt_service()
    get_tts_service()
    yield
    logger.info("Shutting down...")

app = FastAPI(
    title="Speech API",
    description="API for Speech-to-Text and Text-to-Speech using faster-whisper and neutts-air",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(speech.router)

@app.get("/health")
def health():
    return {"status": "ok"}
