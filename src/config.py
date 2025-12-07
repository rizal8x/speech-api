from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # STT Settings
    STT_MODEL_SIZE: str = "base"  # "tiny", "base", "small", "medium", "large-v3"
    STT_DEVICE: str = "cpu"
    STT_COMPUTE_TYPE: str = "int8"
    
    # TTS Settings
    TTS_BACKBONE_REPO: str = "neuphonic/neutts-air-q4-gguf"
    TTS_DEVICE: str = "cpu" # "cpu" (recommended for GGUF)
    TTS_CODEC_REPO: str = "neuphonic/neucodec"
    TTS_CODEC_DEVICE: str = "cpu"
    
    DEFAULT_VOICE_PATH: str = "src/samples/dave.wav" 

settings = Settings()
