import logging
from faster_whisper import WhisperModel
from src.config import settings

logger = logging.getLogger(__name__)

class SpeechToTextService:
    def __init__(self):
        logger.info(f"Loading STT model: {settings.STT_MODEL_SIZE} on {settings.STT_DEVICE}...")
        self.model = WhisperModel(
            settings.STT_MODEL_SIZE, 
            device=settings.STT_DEVICE, 
            compute_type=settings.STT_COMPUTE_TYPE
        )
        logger.info("STT model loaded successfully.")

    def transcribe(self, audio_file, beam_size=5):
        segments, info = self.model.transcribe(audio_file, beam_size=beam_size)
        text = " ".join([segment.text for segment in segments])
        return text.strip(), info

stt_service = None

def get_stt_service():
    global stt_service
    if stt_service is None:
        stt_service = SpeechToTextService()
    return stt_service
