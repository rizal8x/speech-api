import logging
import io
import soundfile as sf
import torch
from src.neuttsair.neutts import NeuTTSAir
from src.config import settings

logger = logging.getLogger(__name__)

class TextToSpeechService:
    def __init__(self):
        logger.info(f"Loading TTS backbone: {settings.TTS_BACKBONE_REPO} on {settings.TTS_DEVICE}...")
        try:
            self.model = NeuTTSAir(
                backbone_repo=settings.TTS_BACKBONE_REPO,
                backbone_device=settings.TTS_DEVICE,
                codec_repo=settings.TTS_CODEC_REPO,
                codec_device=settings.TTS_CODEC_DEVICE
            )
            logger.info("TTS model loaded successfully.")
            
            # Pre-load default reference
            logger.info(f"Loading default reference voice: {settings.DEFAULT_VOICE_PATH}")
            self.default_ref_codes = self.model.encode_reference(settings.DEFAULT_VOICE_PATH)
            
            # Read reference text if available? 
            # Usually neutts-air needs ref_text too for better cloning?
            # From usage example: ref_text = open("samples/dave.txt", "r").read().strip()
            # We'll check if a txt file exists with same name
            ref_txt_path = settings.DEFAULT_VOICE_PATH.replace(".wav", ".txt")
            try:
                with open(ref_txt_path, "r") as f:
                    self.default_ref_text = f.read().strip()
            except FileNotFoundError:
                logger.warning(f"Reference text file not found at {ref_txt_path}. Using empty string (might degrade quality).")
                self.default_ref_text = "This is a reference voice."

        except Exception as e:
            logger.error(f"Failed to load TTS model: {e}")
            raise e

    def synthesize(self, text: str, ref_audio_path: str = None) -> io.BytesIO:
        if ref_audio_path:
            # Handle custom voice cloning
            ref_codes = self.model.encode_reference(ref_audio_path)
            # We might need ref text for custom audio too. 
            # For now assume zero-shot or just pass dummy text? 
            # The API might need to accept ref_text.
            ref_text = "This is a reference voice." # Placeholder
        else:
            ref_codes = self.default_ref_codes
            ref_text = self.default_ref_text

        logger.info(f"Synthesizing text: {text[:50]}...")
        wav = self.model.infer(text, ref_codes, ref_text)
        
        # Convert to bytes
        buffer = io.BytesIO()
        sf.write(buffer, wav, 24000, format='WAV')
        buffer.seek(0)
        return buffer

tts_service = None

def get_tts_service():
    global tts_service
    if tts_service is None:
        tts_service = TextToSpeechService()
    return tts_service
